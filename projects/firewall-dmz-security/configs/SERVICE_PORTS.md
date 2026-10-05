# DMZ service ports

`reconstructed-from-project-records` for HTTP, FTP control, and TFTP; `reference-implementation` for passive FTP range.

| Service | Server | Port/path | Boundary note |
|---|---|---|---|
| Apache HTTP | Both DMZ hosts | TCP 80 | Allow only to DMZ host; validate status and page content |
| vsftpd control | Both DMZ hosts | TCP 21 | Control success does not prove data transfer |
| vsftpd passive data | Optional new-lab setting | TCP 30000–30049 | Range was not recorded; configure server and firewall together |
| TFTP | VyOS DMZ host only | UDP 69 request plus negotiated transfer IDs | Requires appropriate state/conntrack behavior; restrict clients |
| SSH | Neither public DMZ path | TCP 22 blocked from public test client | Keep management on a separate trusted path |

For SELinux or a host firewall, inspect service labels and active rules before disabling the control. For TFTP, verify a file transfer rather than only reaching UDP 69; for passive FTP, verify a directory listing and download rather than only a TCP 21 connection.
