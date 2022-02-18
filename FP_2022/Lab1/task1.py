"""
ip_calc.py
"""

import re


def main(raw_address: str):
    """
    >>> main('91.124.230.205/30')
    IP address: 91.124.230.205
    Network Address: 91.124.230.204
    Broadcast Address: 91.124.230.207
    Binary Subnet Mask: 11111111.11111111.11111111.11111100
    First usable host IP: 91.124.230.205
    Penultimate usable host IP: 91.124.230.205
    Number of usable Hosts: 2
    IP class: A
    IP type private: False
    >>> main('test')
    Error
    >>> main('91.124.230.205')
    Missing prefix
    """

    regex = re.compile(r'^(\d{1,3})\.(\d{1,3})\.'
                       r'(\d{1,3})\.(\d{1,3})')
    if regex.match(raw_address) is None:
        print('Error')
        return

    if '/' not in raw_address:
        print('Missing prefix')
        return
    functions = [get_ip_from_raw_address,
                 get_network_address_from_raw_address,
                 get_broadcast_address_from_raw_address,
                 get_binary_mask_from_raw_address,
                 get_first_usable_ip_address_from_raw_address,
                 get_penultimate_usable_ip_address_from_raw_address,
                 get_number_of_usable_hosts_from_raw_address,
                 get_ip_class_from_raw_address,
                 check_private_ip_address_from_raw_address]
    strings = ['IP address: ',
               'Network Address: ',
               'Broadcast Address: ',
               'Binary Subnet Mask: ',
               'First usable host IP: ',
               'Penultimate usable host IP: ',
               'Number of usable Hosts: ',
               'IP class: ',
               'IP type private: ']
    for fun, string in zip(functions, strings):
        print(f'{string}{fun(raw_address)}')


def get_ip_from_raw_address(raw_address: str) -> str:
    """
    Returns IP-address from raw IP-address
    >>> get_ip_from_raw_address('255.255.255.255/30')
    '255.255.255.255'
    """
    return raw_address.split('/')[0]


def get_network_address_from_raw_address(raw_address: str) -> str:
    """
    Returns network address from raw address
    >>> get_network_address_from_raw_address('91.124.230.205/30')
    '91.124.230.204'
    """
    mask = get_binary_mask_from_raw_address(raw_address)
    if mask is None:
        return None
    mask = list(map(lambda x: int(x, base=2), mask.split('.')))
    ip_address = get_ip_from_raw_address(raw_address)
    ip_address = list(map(int, ip_address.split('.')))
    answer = ''
    for mask_part, ip_part in zip(mask, ip_address):
        answer += str(mask_part & ip_part) + '.'
    return answer[:-1]


def get_broadcast_address_from_raw_address(raw_address: str) -> str:
    """
    Returns broadcast address from raw address
    >>> get_broadcast_address_from_raw_address('91.124.230.205/30')
    '91.124.230.207'
    """
    mask = get_binary_mask_from_raw_address(raw_address)
    if mask is None:
        return None
    time = ''
    for char in mask:
        if char == '1':
            time += '0'
        elif char == '0':
            time += '1'
        else:
            time += char
    mask = time
    mask = list(map(lambda x: int(x, base=2), mask.split('.')))
    ip_address = get_ip_from_raw_address(raw_address)
    ip_address = list(map(int, ip_address.split('.')))
    answer = ''
    for mask_part, ip_part in zip(mask, ip_address):
        answer += str(mask_part | ip_part) + '.'
    return answer[:-1]


def get_binary_mask_from_raw_address(raw_address: str) -> str:
    """
    Returns network binary mask from raw IP-address
    >>> get_binary_mask_from_raw_address('255.255.255.255/30')
    '11111111.11111111.11111111.11111100'
    >>> get_binary_mask_from_raw_address('255.255.255.255/12')
    '11111111.11110000.00000000.00000000'
    >>> get_binary_mask_from_raw_address('255.255.255.255/40')
    """
    mask_length = int(raw_address.split('/')[1])
    if mask_length > 32:
        return None
    answer = mask_length * '1' + (32 - mask_length) * '0'
    return (answer[:8] + '.' + answer[8:16] + '.' +
            answer[16:24] + '.' + answer[24:])


def get_first_usable_ip_address_from_raw_address(raw_address: str) -> str:
    """
    Returns first avaliable IP-address from raw address
    >>> get_first_usable_ip_address_from_raw_address('91.124.230.205/30')
    '91.124.230.205'
    """
    network = get_network_address_from_raw_address(raw_address)
    if network is None:
        return None
    return transform_to_ip(transform_to_number(network) + 1)


def get_penultimate_usable_ip_address_from_raw_address(raw_address: str) -> str:
    """
    Returns penultimate usable ip address from raw address
    >>> get_penultimate_usable_ip_address_from_raw_address('91.124.230.205/30')
    '91.124.230.205'
    """
    usable_hosts = get_number_of_usable_hosts_from_raw_address(raw_address)
    if usable_hosts is None:
        return None
    network = get_network_address_from_raw_address(raw_address)
    if network is None:
        return None
    return transform_to_ip(transform_to_number(network) + usable_hosts - 1)


def get_number_of_usable_hosts_from_raw_address(raw_address: str) -> int:
    """
    Returns number of usable hosts from raw address
    >>> get_number_of_usable_hosts_from_raw_address('91.124.230.205/30')
    2
    """
    network = get_binary_mask_from_raw_address(raw_address)
    zeros = network.count('0')
    if zeros < 2:
        return None
    return 2 ** zeros - 2


def get_ip_class_from_raw_address(raw_address: str) -> str:
    """
    Returns IP-class from raw address
    >>> get_ip_class_from_raw_address('91.124.230.205/30')
    'A'
    """
    network = get_network_address_from_raw_address(raw_address)
    if network is None:
        return None
    first_network_part = int(network.split('.')[0])
    if first_network_part <= 126:
        return 'A'
    if 128 <= first_network_part <= 191:
        return 'B'
    if 192 <= first_network_part <= 223:
        return 'C'
    if 224 <= first_network_part <= 239:
        return 'D'
    if 240 <= first_network_part:
        return 'E'
    return None


def check_private_ip_address_from_raw_address(raw_address: str) -> bool:
    """
    Checks if IP-address is private
    >>> check_private_ip_address_from_raw_address('91.124.230.205/30')
    False
    """
    network = get_network_address_from_raw_address(raw_address)
    if network is None:
        return None
    first_network_part = network.split('.')[0]
    second_network_part = network.split('.')[1]
    return (first_network_part == '127' or
            (first_network_part == '192' and second_network_part == '168'))


def transform_to_number(ip_str: str) -> int:
    """
    >>> transform_to_number('230.250.33.233')
    3875152361
    """
    ip_parts = list(map(int, ip_str.split('.')))
    return (ip_parts[0] * 256 ** 3 + ip_parts[1] * 256 ** 2 +
            ip_parts[2] * 256 + ip_parts[3])


def transform_to_ip(number: int) -> str:
    """
    >>> transform_to_ip(3875152361)
    '230.250.33.233'
    """
    first, number = divmod(number, 256 ** 3)
    second, number = divmod(number, 256 ** 2)
    third, number = divmod(number, 256)
    forth, number = divmod(number, 1)
    return f'{first}.{second}.{third}.{forth}'


if __name__ == '__main__':
    main(input())
