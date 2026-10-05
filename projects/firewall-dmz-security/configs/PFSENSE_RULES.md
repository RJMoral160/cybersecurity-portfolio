# pfSense NAT and ingress policy

`reference-implementation`, not a pfSense XML export. The report's NAT procedure names `192.168.1.10` while its architecture and service results place the published Apache/FTP server in the DMZ. This reference maps the VIP to `192.168.3.10`; verify the source system before treating that as a historical correction. Rule IDs here are documentation IDs.

## Address aliases and NAT

| Alias | Value | Role |
|---|---|---|
| `TEST_CLIENT` | `203.0.113.10/32` | Isolated WAN-side client |
| `WAN_VIP_FTP_WEB` | `203.0.113.6/32` | pfSense IP-alias VIP on WAN |
| `DMZ_FTP_WEB` | `192.168.3.10/32` | Apache and vsftpd server |
| `PRIVATE_A` | `192.168.1.0/24` | Private A clients |
| `TEST_UPSTREAM` | `203.0.113.20/32` | Disconnected HTTP/DNS test service |
| `FTP_PASSIVE_PF` | `50000:50100` | TCP passive-data range, supplied for this reference by repository owner; not found in report text |

| ID/order | GUI area | Interface/direction | Match | Translation | Return path |
|---|---|---|---|---|---|
| N1 | Firewall → Virtual IPs | WAN | `203.0.113.6/32` | IP Alias, no translation by itself | VIP receives ARP on test WAN |
| N2 | Firewall → NAT → 1:1 | WAN, bidirectional | External `203.0.113.6/32` ↔ internal `192.168.3.10/32` | New inbound destination → DMZ host; new outbound DMZ-host source → VIP | Server gateway `192.168.3.1`; state reverses inbound translation |
| N3 | Firewall → NAT → Outbound, Hybrid mode | WAN outbound | Source `192.168.1.0/24`, destination `203.0.113.20/32`, TCP 80/443 or UDP/TCP 53 | Interface address `203.0.113.5` with PAT | Return to `.5` is matched to state and de-translated |

1:1 NAT has **both** directions. It does not authorize traffic; interface firewall rules still do. It normally takes precedence over outbound NAT for the DMZ host. Do not create an overlapping port-forward for the VIP. The test client must route to the WAN network; internal clients use `192.168.3.10` directly, avoiding unconfigured NAT reflection. See [Netgate 1:1 NAT](https://docs.netgate.com/pfsense/en/latest/nat/1-1.html) and [processing order](https://docs.netgate.com/pfsense/en/latest/nat/process-order.html).

## Ordered ingress rules

pfSense processes the interface tab where a packet **enters**. Inbound NAT occurs before WAN filtering, so WAN rule destinations below are the translated DMZ address, not the VIP. Source ports are ephemeral unless specified. Default block is last. Create aliases first, choose Hybrid outbound NAT, then enter rules top-to-bottom and inspect states/logs. A fresh pfSense install commonly includes a broad default LAN-pass rule; remove or disable that rule **only after** console management and the narrower LAN/management rules are verified, otherwise this table's default-deny claim would be false.

| Order/ID | Ingress | Action | Source | Filter destination | Protocol/destination port | Intent |
|---|---|---|---|---|---|---|
| 1 / W10 | WAN | Pass/log | `TEST_CLIENT` | `DMZ_FTP_WEB` | TCP 80 | Public test HTTP via VIP |
| 2 / W20 | WAN | Pass/log | `TEST_CLIENT` | `DMZ_FTP_WEB` | TCP 21 | FTP control via VIP |
| 3 / W30 | WAN | Pass/log | `TEST_CLIENT` | `DMZ_FTP_WEB` | TCP `50000:50100` | Client-initiated passive data via VIP |
| 4 / W40 | WAN | Block/log | `TEST_CLIENT` | `DMZ_FTP_WEB` | TCP 22 | Deny server SSH, **not** proof of firewall-management policy |
| 1 / L10 | LAN | Pass/log | `PRIVATE_A` | `DMZ_FTP_WEB` | TCP 80,21,`50000:50100` | Direct internal service and passive data access |
| 2 / L20 | LAN | Pass/log | `PRIVATE_A` | `TEST_UPSTREAM` | TCP 80,443 | Bounded outbound web test; NAT N3 |
| 3 / L30 | LAN | Pass/log | `PRIVATE_A` | `TEST_UPSTREAM` | TCP/UDP 53 | Bounded resolver test; NAT N3 |
| last | WAN/LAN/DMZ | Block/log | Any other new source | Any | Any | No other cross-zone access in this reference |

Established return packets use state; do not add unrestricted reverse passes. GUI access to pfSense itself must be constrained separately under Firewall → Rules on the ingress interface and webConfigurator settings. A blocked TCP 22 connection to the DMZ host does not demonstrate this. For this IPv4-only isolated reproduction, leave IPv6 interfaces unassigned; if enabled, create and test IPv6 rules separately rather than assuming IPv4 policy applies.

## FTP behavior

The [pfSense vsftpd reference](vsftpd-pfsense.conf) advertises the VIP in a PASV reply and listens on `50000–50100/tcp`. The **WAN** client connects to the VIP and uses PASV or EPSV. The **Private A** client connects directly to `192.168.3.10` and must use **EPSV**, which supplies only a port and reuses that direct host address; ordinary PASV may tell the private client to use the VIP and fail without NAT reflection/split DNS. Test the private client mode explicitly. Both paths use explicit data-port permits, **not** an assumed FTP helper. The server selects/listens on a passive port; the client initiates the second TCP connection; file bytes can then move either way. Netgate [requires control and passive range allowances with 1:1 NAT](https://docs.netgate.com/pfsense/en/latest/nat/compatibility.html). Plain FTP is for an isolated legacy-service lab only; use a protected alternative for real deployments.
