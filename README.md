# zonefilegen
A simple tool to generate synchronized forward and reverse DNS zone files based on an input text file.

The intended use case is where a local authoritative DNS server is used to serve
lookups for hosts confined within a single forward DNS zone. Thus, only a single
forward zone is supported in order to simplify the input file.

Reverse zones will be generated for specified subnets, and they will be automatically populated
with PTR records corresponding to the first `A` and `AAAA` records found in the input file for a certain host.

Zone serial numbers will automatically be incremented when the input file has changed.

## Installation
Install via pip: 
```
pip install zonefilegen
```

## Usage
The package installs a command line tool `zonefilegen` which generates zone files 
in a specified directory based on an input file:
```
zonefilegen input.toml output_folder
```

This will parse `input.toml` and generate one forward zone file and zero and more 
reverse zone files in `output_dir`.


## Input file format
The input file is written in the [TOML](https://toml.io) format which is easy to read
by both humans and machines.

For an example file, see `docs/sample.toml`.

### Required entries
The following entries are required in the input file:
- `origin`: The FQDN of the forward DNS zone. `$ORIGIN` in the zone file.
- `default_ttl`: Default TTL for resource records if they have none set. `$TTL` in the zone file.
- `[soa]`: Contains the entries to put in the `SOA` record, except for the serial number:
    - `mname`
    - `rname`
    - `refresh`
    - `retry`
    - `expire`
    - `negative_caching_ttl`

- One or more `[[rrset]]` with entries for the forward records. Each `[[rrset]]` entry
  contains one or more records with the same name, type and ttl value:
    - `name`: `@`, unqualified name or FQDN.
    - `type`: The record type like `A` or `MX`.
    - `ttl`: Optional TTL value.
    - `data`: A string or a list of strings with the record data. A separate record will be created for every string in the list.

Optionally, one can also supply a `networks` entry, which should contain a list
of networks in CIDR notation (ipv4 or ipv6) for which reverse zones should be created. 
The networks must end on whole-octet (ipv4) or whole-nibble edges (ipv6). So only `/16`, `/24` etc in
the ipv4 case and `/48`, `/52`, `/56` etc for ipv6.


