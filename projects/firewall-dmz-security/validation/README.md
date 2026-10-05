# Firewall and DMZ validation

This is a **new-lab test plan**, not recorded command output. Use a disconnected `203.0.113.0/24` test segment and one benign `hello.txt` fixture. The source report records HTTP/FTP/TFTP goals and some successful access, but not complete passive-data traces or the reference rules added here.

| Test | Initiator → destination | Command / interface | Success criterion | Failure starting point |
|---|---|---|---|---|
| pfSense inbound HTTP | `.10` → VIP `.6:80` | `curl -v http://203.0.113.6/`; pfSense Diagnostics → States | Apache content from `.3.10`, W10 state, reverse VIP response | VIP ARP, N2 1:1, WAN post-NAT destination, DMZ gateway |
| pfSense private egress | `192.168.1.10` → `.20:80` | `curl -v http://203.0.113.20/`; state/NAT view | L20 then N3 source `.5`; return reaches client | Hybrid mode, route, L20 order |
| VyOS private egress | `192.168.2.10` → `.20:80` | `show firewall ipv4 forward filter`; `show nat source translations`; `curl -v` | Rule 70 matches, rule 100 translates to `.4`, return succeeds | No forward permit, missing NAT, upstream route |
| pfSense FTP | `.10` → VIP `.6:21` then passive `.6:50000-50100` | passive FTP client `ls` and `get hello.txt`; pfSense state view | Client opens second TCP connection, W20/W30 pass, file matches server | Advertised PASV IP, W30, host firewalld/SELinux |
| pfSense internal FTP | `192.168.1.10` → direct `192.168.3.10:21` and data range | EPSV-capable client `ls` and `get hello.txt`; L10 state | Client reuses `.3.10` for EPSV data; no VIP reflection | PASV advertised VIP to private client, L10, host port range |
| VyOS FTP | `.10` → routed `.37.10:21` then `.37.10:30000-30100` | passive FTP client `ls` and `get hello.txt`; `show firewall` | Rule 40/45 (public) or 30/35 (Private B) passes data | Upstream route, rule/interface, host port range |
| TFTP | Isolated client → `172.18.37.10:69` | request `hello.txt`, compare contents and daemon log | Negotiated transfer completes; only approved source succeeds | TFTP helper, firewall state, server root/permissions |
| DMZ SSH denial | `.10` → either DMZ host `:22` | `nc -vz -w 3` plus firewall log | Blocked and logged; server SSH not reached | Wrong rule order or state |
| Router-local management | `.10` → VyOS `.4:22`, then `.2.20` → `.2.1:22` | SSH connection and input-rule counters | Public denied; management host allowed after SSH service configuration | Input vs forward filter, daemon binding |
| IPv6 bypass | Test IPv6-capable client → VyOS | `show firewall ipv6 input filter`; `show firewall ipv6 forward filter` | New IPv6 path denied in reference | IPv6 interface assignment/policy |

The reference outbound tests intentionally target a locally built `.20` service. `203.0.113.0/24` is documentation space, not a routable public Internet target. State/counter checks are device-level criteria for a future lab; they were not executed by this repository repair.

`reference-implementation`. Run from an isolated test client and record timestamp, source/destination, rule/state ID, and server-side observation. The first three recorded results below come from team lab reporting; other entries are new-lab criteria.

| Flow | Test | Expected behavior | Record status / failure clue |
|---|---|---|---|
| Public → pfSense VIP HTTP | `curl -I http://203.0.113.6/` | Apache response from `192.168.3.10`, not pfSense GUI | HTTP access reported; inspect NAT and vhost if GUI appears |
| Public → pfSense VIP FTP control | `nc -vz 203.0.113.6 21` | TCP 21 accepted by DMZ server | FTP access reported; control channel only |
| Public → pfSense VIP passive data | FTP directory listing/download | Data connection succeeds on configured passive range | Not preserved in source; inspect vsftpd range, NAT, firewall, SELinux |
| Public → VyOS DMZ HTTP | `curl -I http://172.18.37.10/` from routed lab client | TCP 80 reaches Apache via `eth2`→`eth1` | HTTP access reported; confirm upstream static route |
| Public → VyOS DMZ FTP | FTP login plus file listing | Control and data paths both work | General FTP access reported; complete passive transfer not retained |
| Public → VyOS DMZ TFTP | Fetch a known harmless file | UDP transfer completes | Service configured; complete transfer evidence limited |
| Public → VyOS DMZ SSH | `nc -vz 172.18.37.10 22` | Connection denied and VyOS drop log increments | Failed SSH and log after fix recorded |
| Private B → isolated upstream web host | `curl -v http://203.0.113.20/`; inspect VyOS NAT state | Rule 70 allows TCP 80 and source NAT uses `.4` | Historical Internet connectivity was reported; this narrower new-lab rule does not permit ICMP or general Internet access |
| Public → private controller | Try TCP 3389/445 from isolated client | No state or service reachability | Proposed negative check; not fully recorded |

On VyOS inspect `show firewall ipv4 forward filter`, `show nat source rules`, `show ip route`, and system logs around each attempt. On pfSense inspect **Diagnostics → States**, **Firewall → Rules**, **Firewall → NAT**, **Status → System Logs → Firewall**, and packet capture on WAN and DMZ. On Linux inspect `ss -lntup`, `journalctl -u httpd -u vsftpd`, and `firewall-cmd --list-all` where applicable. For a negative test, confirm a matching drop record or capture; a failed client connection can also be a DNS, route, host-firewall, or service problem.
