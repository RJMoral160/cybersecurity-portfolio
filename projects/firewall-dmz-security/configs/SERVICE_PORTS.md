# DMZ service ports

`reconstructed-from-project-records` for HTTP, FTP control, and TFTP; `reference-implementation` for passive FTP range.

| Service | Server | Port/path | Boundary note |
|---|---|---|---|
| Apache HTTP | Both DMZ hosts | TCP 80 | Allow only to DMZ host; validate status and page content |
| vsftpd control | Both DMZ hosts | TCP 21 | Control success does not prove data transfer |
| pfSense vsftpd passive data | DMZ `192.168.3.10` | TCP 50000–50100 | Owner-supplied range for reference; WAN 1:1 and L10 permits |
| VyOS vsftpd passive data | DMZ `172.18.37.10` | TCP 30000–30100 | Owner-supplied range for reference; rules 35/45 |
| TFTP | VyOS DMZ host only | UDP 69 request plus negotiated transfer IDs | Requires appropriate state/conntrack behavior; restrict clients |
| SSH | Neither public DMZ path | TCP 22 blocked from public test client | Keep management on a separate trusted path |

For SELinux or a host firewall, inspect service labels and active rules before disabling the control. For TFTP, verify a file transfer rather than only reaching UDP 69; for passive FTP, verify a directory listing and download rather than only a TCP 21 connection.

Neither passive range was found in the text of the available firewall report. They are provided by the repository owner and are used here as **reference settings**, not asserted as recovered original configuration. The pfSense path uses explicit WAN and LAN data-port permits. The VyOS path uses explicit forward rules 35/45; `conntrack modules tftp` is retained for TFTP's negotiated transfer port, not as a substitute for the FTP data rules.
