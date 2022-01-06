import ipaddress
import hashlib
import ipaddress
import logging
import pathlib
from typing import List, Tuple

import toml
import zonefilegen
import zonefilegen.core
import zonefilegen.generation

def get_rev_zone_name(network) -> str:
    """
    Cuts off the first few blocks of a reverse pointer for a network address
    to create a suitable reverse zone name for a certain prefix length.
    """
    if type(network) is ipaddress.IPv4Network:
        divisor = 8
        address_len = 32
    elif type(network) is ipaddress.IPv6Network:
        divisor = 4
        address_len = 128
    else:
        raise Exception(f"Invalid network type: {network}")

    blocks_to_cut = int((address_len - network.prefixlen) / divisor)
    return '.'.join(network.network_address.reverse_pointer.split('.')[blocks_to_cut:None]) + '.'

def get_rev_ptr_name(address, prefix_len) -> str:
    """
    Cuts off the last few blocks of a reverse pointer for an address
    to create a suitable reverse pointer name for a certain prefix length.
    """
    if type(address) is ipaddress.IPv4Address:
        divisor = 8
        address_len = 32
    elif type(address) is ipaddress.IPv6Address:
        divisor = 4
        address_len = 128
    else:
        raise Exception(f"Invalid address type: {address}")

    blocks_to_cut = int(((address_len - prefix_len) / divisor))
    return '.'.join(address.reverse_pointer.split('.')[None:blocks_to_cut])

def parse_toml_file(input_file_path: pathlib.Path) -> Tuple[zonefilegen.core.Zone, List[zonefilegen.core.Zone], dict, str]:
    """
    Parses a toml file with DNS records and generates one forward zone and one or 
    more reverse zones. Additionally, a dict with info about the SOA record and a digest of the source file is returned for embedding 
    in the generated files, to detect when serial number needs to be updated.
    """
    with open(input_file_path, 'r') as f:
        data = toml.load(f)
        f.seek(0)
        file_digest = hashlib.sha1(f.read().encode()).hexdigest()
    
    fwd_zone = zonefilegen.generation.build_fwd_zone(data['origin'], data['rrset'], data['default_ttl'])

    ipv4_ptr_candidates = []
    ipv6_ptr_candidates = []

    for rec in fwd_zone.records:
        if rec.record_type == 'A':
            ipv4_ptr_candidates.append((rec.name, rec.ttl, ipaddress.IPv4Address(rec.data)))
        elif rec.record_type == 'AAAA':
            ipv6_ptr_candidates.append((rec.name, rec.ttl, ipaddress.IPv6Address(rec.data)))

    reverse_zones = []
    for network_str in data['networks']:
        network = ipaddress.ip_network(network_str, strict=True)
        if type(network) is ipaddress.IPv4Network:
            reverse_zones.append(zonefilegen.generation.build_reverse_zone(network, ipv4_ptr_candidates, data['default_ttl']))
            if network.prefixlen % 8 != 0:
                logging.fatal("IPv4 network prefix must be divisible by 8")
                exit(1)

        elif type(network) is ipaddress.IPv6Network:
            reverse_zones.append(zonefilegen.generation.build_reverse_zone(network, ipv6_ptr_candidates, data['default_ttl']))
            if network.prefixlen % 4 != 0:
                logging.fatal("IPv6 network prefix must be divisible by 4")
                exit(1)

    return (fwd_zone, reverse_zones, data['soa'], file_digest)