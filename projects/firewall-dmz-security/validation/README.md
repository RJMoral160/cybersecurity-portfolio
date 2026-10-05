# Firewall and DMZ validation

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
| Private B → external test host | `ping 203.0.113.20`; inspect VyOS NAT state | Outbound masquerade uses `.4` | Internet connectivity reported; compare pre/post source |
| Public → private controller | Try TCP 3389/445 from isolated client | No state or service reachability | Proposed negative check; not fully recorded |

On VyOS inspect `show firewall ipv4 forward filter`, `show nat source rules`, `show ip route`, and system logs around each attempt. On pfSense inspect **Diagnostics → States**, **Firewall → Rules**, **Firewall → NAT**, **Status → System Logs → Firewall**, and packet capture on WAN and DMZ. On Linux inspect `ss -lntup`, `journalctl -u httpd -u vsftpd`, and `firewall-cmd --list-all` where applicable. For a negative test, confirm a matching drop record or capture; a failed client connection can also be a DNS, route, host-firewall, or service problem.
