from typing import List

RECORD_CLASSES = [
    'IN',
    'CH',
    'HS',
]

RECORD_TYPES =  [
    'A',
    'NS',
    'MD',
    'MF',
    'CNAME',
    'SOA',
    'WKS',
    'PTR',
    'HINFO',
    'MINFO',
    'MX',
    'TXT',
    'RP',
    'AFSDB',
    'X25',
    'ISDN',
    'RT',
    'NSAP',
    'NSAP-PTR',
    'SIG',
    'KEY',
    'PX',
    'GPOS',
    'AAAA',
    'LOC',
    'NXT',
    'EID',
    'NIMLOC',
    'SRV',
    'ATMA',
    'NAPTR',
    'KX',
    'CERT',
    'A6',
    'DNAME',
    'SINK',
    'OPT',
    'APL',
    'DS',
    'SSHFP',
    'IPSECKEY',
    'RRSIG',
    'NSEC',
    'DNSKEY',
    'DHCID',
    'NSEC3',
    'NSEC3PARAM',
    'TLSA',
    'SMIMEA',
    'HIP',
    'NINFO',
    'RKEY',
    'TALINK',
    'CDS',
    'CDNSKEY',
    'OPENPGPKEY',
    'CSYNC',
    'ZONEMD',
    'VCB',
    'SVCB',
    'HTTPS',
    'SPF',
    'UINFO',
    'UID',
    'GID',
    'UNSPEC',
    'NID',
    'L32',
    'L64',
    'LP',
    'EUI48',
    'EUI64',
    'TKEY',
    'TSIG',
    'IXFR',
    'AXFR',
    'MAILB',
    'MAILA',
    '*',
    'URI',
    'CAA',
    'AVC',
    'DOA',
    'AMTRELAY',
    'TA',
    'DLV',
]

class ResourceRecord():
    def __init__(self):
        self.name = None
        self.ttl = None
        self.record_class = None
        self.record_type = None
        self.data = None
    
    def to_line(self):
        ttl_str = str(self.ttl) if self.ttl else ''
        record_class_str = str(self.record_class) if self.record_class else ''
        return f"{self.name} {ttl_str} {record_class_str} {self.record_type} {self.data}"


class Zone():
    def __init__(self, name: str, default_ttl: int):
        self.name = name
        self.default_ttl = default_ttl
        self.records = []
    
    def generate_origin(self):
        return f"$ORIGIN {self.name}"

    def generate_ttl(self):
        return f"$TTL {self.default_ttl}"
