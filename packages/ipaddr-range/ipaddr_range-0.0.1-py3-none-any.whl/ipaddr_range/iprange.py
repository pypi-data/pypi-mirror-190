import logging
from dataclasses import dataclass
from ipaddress import IPv4Address, IPv6Address, ip_address

from abc import ABC, abstractmethod

logging.basicConfig(level=logging.INFO)

IPAddress = str | IPv4Address | IPv6Address


@dataclass
class IPAddressRange:
    start: IPAddress
    end: IPAddress

    def __post_init__(self):
        self.start = ip_address(self.start)
        self.end = ip_address(self.end)

    def __iter__(self):
        current = self.start
        while current <= self.end:
            yield current
            current += 1


@dataclass
class IPv4AddressRange(IPAddressRange):
    pass


@dataclass
class IPv6AddressRange(IPAddressRange):
    pass


class IPAddressGenerator(ABC):
    """
    Abstract class that provides an interface for generating ip addresses.
    """

    @abstractmethod
    def generate(self, start: str, end: str) -> IPAddressRange:
        """
        Method to be implemented in subclasses.
        """
        pass


class IPv4AddressGenerator(IPAddressGenerator):
    """
    Class that generates a list of ip addresses of the IPv4 version.
    """

    def generate(self, start: str, end: str) -> IPv4AddressRange:
        return IPv4AddressRange(start=start, end=end)


class IPv6AddressGenerator(IPAddressGenerator):
    """
    Class that generates a list of ip addresses of the IPv6 version.
    """

    def generate(self, start: str, end: str) -> IPv6AddressRange:
        return IPv6AddressRange(start=start, end=end)


if __name__ == '__main__':
    start_ip, end_ip = '192.168.2.1', '192.168.2.10'

    generator = IPv4AddressGenerator()
    ip_range = generator.generate(start_ip, end_ip)

    for ip in ip_range:
        logging.info(ip)
