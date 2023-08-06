# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ipaddr_range']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ipaddr-range',
    'version': '0.0.1',
    'description': 'Generating a list of IP addresses of IPv4 and IPv6 versions.',
    'long_description': "# ipaddr_range\n\nThis code provides a simple implementation of generating a list of IP addresses of IPv4 and IPv6 versions. \n\n### Usage\n\nThe code defines three classes:\n\n* `IPAddressRange`: This is a data class that holds the start and end IP addresses.\n* `IPv4AddressRange` and `IPv6AddressRange`: These classes inherit from `IPAddressRange` and represent IP ranges for IPv4 and IPv6 addresses respectively.\n* `IPAddressGenerator`: This is an abstract class that provides an interface for generating IP addresses.\n* `IPv4AddressGenerator` and `IPv6AddressGenerator`: These classes inherit from `IPAddressGenerator` and provide the implementation for generating IPv4 and IPv6 addresses respectively.\n\nTo generate a list of IP addresses, you need to create an instance of `IPv4AddressGenerator` or `IPv6AddressGenerator` and then call the generate method with the start and end IP addresses.\n\nThe generate method returns an object of type `IPAddressRange`, which can be used to traverse through the generated IP addresses.\n\n### Example\n\n```python\nif __name__ == '__main__':\n    start_ip, end_ip = '192.168.2.1', '192.168.2.10'\n\n    generator = IPv4AddressGenerator()\n    ip_range = generator.generate(start_ip, end_ip)\n\n    for ip in ip_range:\n        logging.info(ip)\n```\n\nThis code generates a list of IP addresses of the IPv4 version and logs the generated IP addresses.\n",
    'author': 'Ivan Migunov',
    'author_email': 'im@fckg.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
