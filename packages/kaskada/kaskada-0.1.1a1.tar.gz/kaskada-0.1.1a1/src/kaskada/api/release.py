import functools
import os
import shutil
from pathlib import Path
from typing import Dict, MutableMapping, Tuple

import requests
from tqdm.auto import tqdm

from . import utils


class ReleaseClient(object):
    ORGANIZATION = "riptano"
    REPO_NAME = "kaskada"
    LATEST_RELEASE_API_ENDPOINT = (
        "https://api.github.com/repos/{}/{}/releases/latest".format(
            ORGANIZATION, REPO_NAME
        )
    )
    ASSETS_API_ENDPOINT = "https://api.github.com/repos/{}/{}/releases/assets".format(
        ORGANIZATION, REPO_NAME
    )
    # In case the repository is private, an authorized access token is required.
    GITHUB_ACCESS_TOKEN_ENV = "GITHUB_ACCESS_TOKEN"

    def __init__(self):
        self._platform_details = utils.get_platform_details()

    def download_latest_release(
        self, download_path: Path, manager_bin_name: str, engine_bin_name: str
    ) -> Tuple[Path, Path]:
        """Downloads the latest version of the kaskada-manager and kaskada-engine.

        Args:
            download_path (Path): The local download path
            manager_bin_name (str): The name of the manager binary to save in download path
            engine_bin_name (str): The name of the engine binary to save in download path

        Raises:
            RuntimeError: unable to get release assets

        Returns:
            Tuple[str, str]: manager path and engine path
        """
        manager_name = "kaskada-manager-{}".format(self._platform_details.format_name())
        engine_name = "kaskada-engine-{}".format(self._platform_details.format_name())

        headers: MutableMapping = {"Accept": "application/vnd.github+json"}
        # Create a session for subsequent requests to contain the same headers e.g. authorization
        session = requests.Session()
        # Private repository access
        access_token = os.getenv(self.GITHUB_ACCESS_TOKEN_ENV)
        if access_token is not None:
            headers["Authorization"] = f"token {access_token}"
        session.headers = headers
        r = session.request("GET", self.LATEST_RELEASE_API_ENDPOINT)
        if r.status_code != 200:
            raise RuntimeError(
                "unable to get the latest release assets. set GITHUB_ACCESS_TOKEN if repo is private"
            )

        contents = r.json()
        if "assets" in contents:
            assets = contents["assets"]
            for asset in assets:
                if "name" in asset and "id" in asset and "size" in asset:
                    name = asset["name"]
                    id = asset["id"]
                    size = int(asset["size"])
                    url = f"{self.ASSETS_API_ENDPOINT}/{id}"
                    if name == manager_name:
                        manager_path = self.__download(
                            session,
                            url,
                            download_path / manager_bin_name,
                            name,
                            file_size=size,
                        )
                    elif name == engine_name:
                        engine_path = self.__download(
                            session,
                            url,
                            download_path / engine_bin_name,
                            name,
                            file_size=size,
                        )
                else:
                    raise RuntimeError("unable to get name/url from assets")
        else:
            raise RuntimeError("unable to get assets from latest release")

        if manager_path is None:
            raise RuntimeError(f"unable to download manager binary: {manager_name}")
        if engine_path is None:
            raise RuntimeError(f"unable to download engine binary: {engine_name}")
        return manager_path, engine_path

    def __download(
        self,
        r: requests.Session,
        url: str,
        download_path: Path,
        description: str,
        file_size: int = 0,
    ) -> Path:
        """Downloads a URL as an application/octet-stream

        Args:
            r (requests.Session): The request session
            url (str): The targget URL
            download_path (Path): The local path to stream write the file
            description (str): The description to render during download
            file_size (int, optional): The file size if known ahead of time. Defaults to response content size or 0.

        Raises:
            RuntimeError: Unable to download the target URL due to non 200 error code.

        Returns:
            Path: The local download path
        """
        # Request header to get the binary
        r.headers["Accept"] = "application/octet-stream"
        response = r.get(url, stream=True, allow_redirects=True)
        if response.status_code != 200:
            response.raise_for_status()  # If there was an HTTP error, raise that first otherwise generic error.
            raise RuntimeError(
                f"request to download binary failed with status code: {response.status_code}"
            )
        if (
            file_size == 0
        ):  # The file size is only used for the progress bar visualization.
            file_size = int(r.headers.get("Content-Length", 0))
        desc = "(Unknown total file size)" if file_size == 0 else description
        response.raw.read = functools.partial(
            response.raw.read, decode_content=True
        )  # Decompress if needed
        with tqdm.wrapattr(
            response.raw, "read", total=file_size, desc=desc
        ) as r_raw:  # Define the progress bar
            with download_path.open(
                "wb"
            ) as f:  # Start downloading the raw response as the binary
                shutil.copyfileobj(r_raw, f)
        return download_path
