# pfSense rule and NAT tables

`reference-implementation` based on the recorded service objective and WAN VIP. The report's procedure lists the wrong internal target for one 1:1 NAT entry, while its architecture and test narrative identify the DMZ server as the published HTTP/FTP host. This reference uses the DMZ host `192.168.3.10`; it is not an original XML export.

## NAT and VIP

| ID | pfSense area | Original flow | Translation | Purpose |
|---|---|---|---|---|
| P-VIP-01 | Firewall → Virtual IPs | WAN alias | `203.0.113.6/32` on WAN | Dedicated service address |
| P-NAT-01 | Firewall → NAT → 1:1 | Destination `203.0.113.6` | Destination `192.168.3.10` | Inbound DMZ service mapping; filter ports separately |
| P-NAT-02 | Firewall → NAT → Outbound | Source `192.168.1.0/24` leaving WAN | Source `203.0.113.5` with PAT | Private A outbound access |

A 1:1 mapping makes the DMZ host addressable through the VIP. It does not by itself limit the exposed ports. In a fresh build, individual port forwards for TCP 80/21 may be narrower; choose one NAT model and verify state creation. Do not add a second conflicting port-forward rule for the same VIP/port.

## Interface rules

Rule IDs below are documentation IDs, not original pfSense rule numbers. pfSense evaluates interface rules on traffic entering that interface. Match the translated DMZ destination according to the pfSense version's NAT/filter display and verify with packet capture.

| ID | Interface | Action | Source | Destination | Service | Why |
|---|---|---|---|---|---|---|
| P-WAN-01 | WAN | Pass | Isolated test clients | DMZ host via VIP | TCP 80 | Apache site |
| P-WAN-02 | WAN | Pass | Isolated test clients | DMZ host via VIP | TCP 21 | FTP control |
| P-WAN-04 | WAN | Pass after server setup | Isolated test clients | DMZ host via VIP | TCP 30000–30049 | Proposed passive FTP data range; not recorded |
| P-WAN-03 | WAN | Block/log | Isolated test clients | DMZ host via VIP | TCP 22 | SSH not a published service |
| P-LAN-01 | LAN | Pass | `192.168.1.0/24` | Approved DMZ service | TCP 80,21 | Private clients reach service |
| P-LAN-02 | LAN | Pass | `192.168.1.0/24` | Approved upstream | Required outbound traffic | Private A egress through PAT |
| P-DEFAULT | WAN/LAN/DMZ | Block/log | Other new traffic | Any | Any | No implicit cross-zone access |

The source rule table lists WAN TCP 21/80 and LAN/DMZ service allowances, but does not preserve a complete final rule export. `P-WAN-03` and explicit default logging are reference checks to demonstrate a denied path; they are not claimed as original named rules.

## FTP data channel

TCP 21 opens the FTP control channel. Passive FTP also needs a server-defined data-port range and matching firewall/NAT behavior. The source report does not document a passive range. A proposed isolated-lab range is `30000–30049/tcp` in [vsftpd.conf](vsftpd.conf); add it only after the server is bound to that range and test a directory listing/file transfer. Prefer a secure transfer protocol for a production service.
