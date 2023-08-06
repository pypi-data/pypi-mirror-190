# ipaddr_range

This code provides a simple implementation of generating a list of IP addresses of IPv4 and IPv6 versions. 

### Usage

The code defines three classes:

* `IPAddressRange`: This is a data class that holds the start and end IP addresses.
* `IPv4AddressRange` and `IPv6AddressRange`: These classes inherit from `IPAddressRange` and represent IP ranges for IPv4 and IPv6 addresses respectively.
* `IPAddressGenerator`: This is an abstract class that provides an interface for generating IP addresses.
* `IPv4AddressGenerator` and `IPv6AddressGenerator`: These classes inherit from `IPAddressGenerator` and provide the implementation for generating IPv4 and IPv6 addresses respectively.

To generate a list of IP addresses, you need to create an instance of `IPv4AddressGenerator` or `IPv6AddressGenerator` and then call the generate method with the start and end IP addresses.

The generate method returns an object of type `IPAddressRange`, which can be used to traverse through the generated IP addresses.

### Example

```python
if __name__ == '__main__':
    start_ip, end_ip = '192.168.2.1', '192.168.2.10'

    generator = IPv4AddressGenerator()
    ip_range = generator.generate(start_ip, end_ip)

    for ip in ip_range:
        logging.info(ip)
```

This code generates a list of IP addresses of the IPv4 version and logs the generated IP addresses.
