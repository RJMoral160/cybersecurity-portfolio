# Interfaces, zones, and routes

`reconstructed-from-project-records`. These are two separate firewall environments. The public network has been replaced by RFC 5737 documentation addressing; private lab subnets remain RFC 1918 examples.

| Environment | Interface | Zone | Address | Attached host |
|---|---|---|---|---|
| pfSense | WAN | Public test | `203.0.113.5/24` | Test client `203.0.113.10` |
| pfSense | WAN VIP | Public service address | `203.0.113.6/32` | Mapped to DMZ service host |
| pfSense | DMZ | Public service segment | `192.168.3.1/24` | Apache/vsftpd `192.168.3.10` |
| pfSense | LAN | Private A | `192.168.1.1/24` | Windows server `192.168.1.10` |
| VyOS | `eth2` | Public test | `203.0.113.4/24` | Example upstream `.1` |
| VyOS | `eth1` | DMZ | `172.18.37.1/24` | Apache/vsftpd/TFTP `172.18.37.10` |
| VyOS | `eth0` | Private B | `192.168.2.1/24` | Windows server `192.168.2.10` |

| Route | Next hop | Purpose |
|---|---|---|
| pfSense/VyOS default `0.0.0.0/0` | `203.0.113.1` | Isolated upstream test segment |
| Upstream `172.18.37.0/24` | `203.0.113.4` | Lab-only routed reachability to VyOS DMZ |
| DMZ host default | Its firewall DMZ address | Return traffic through policy boundary |

The VyOS source report used routed access to its RFC 1918 DMZ, not a recorded inbound DNAT mapping. An upstream route makes that possible only in a controlled lab. A real Internet-facing design would need a public mapping or proxy and a separate security review.
