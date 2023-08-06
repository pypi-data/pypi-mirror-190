import platform
import socket
import subprocess
from contextlib import closing


def run_subprocess(cmd: str):
    return subprocess.Popen(cmd, shell=True)


def check_socket(endpoint: str):
    parse = endpoint.split(":")
    if len(parse) != 2:
        raise ValueError("endpoint is not formatted correctly. host:port")

    host = parse[0]
    port = int(parse[1])
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        return sock.connect_ex((host, port)) == 0


class PlatformDetails(object):
    def __init__(self, architecture: str, num_bits: str, system: str):
        """Wrapper platform details object around the internal platform API

        Args:
            architecture (str): The underlying architecture e.g. arm
            num_bits (str): The number of bits for the system e.g. 32/64
            system (str): The system/OS name e.g. win/darwin/linux
        """
        self._architecture = architecture
        self._num_bits = num_bits
        self._system = system

    def format_name(self) -> str:
        """Gets the formatted name from the system configuration.

        Returns:
            str: formatted name as <system>-<architecture><num bits> e.g. darwin-arm64.
        """
        return "{}-{}{}".format(
            self._system, self._architecture, self._num_bits
        ).lower()


def get_platform_details() -> PlatformDetails:
    """Parses the system platform for a PlatformDetails

    Returns:
        PlatformDetails: The current system platform
    """
    # TODO: Verify for other systems beyond Mac ARM 64
    architecture = platform.processor()
    system = platform.system()
    num_bits = "64"
    if "32" in platform.platform():
        num_bits = "32"
    return PlatformDetails(architecture, num_bits, system)
