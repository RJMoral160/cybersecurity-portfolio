# Denied management and FTP data paths

`reconstructed-from-project-records` for blocked **DMZ server** SSH; `reference-implementation` for bounded management and owner-supplied passive ranges.

## Denied SSH

```mermaid
flowchart LR
  C["Public test client<br/>203.0.113.10"] -->|"TCP 22 to 172.18.37.10"| VY["VyOS eth2<br/>default drop + default-log"]
  VY -.->|"no forward permit"| S["DMZ B server"]
  VY --> L["Drop log entry"]
```

The recorded test first showed a failed SSH connection without a log. Enabling `default-log` produced the drop record. That test does **not** test router-local management. The VyOS reference separately restricts IPv4 input SSH to `192.168.2.20` on `eth0` and drops other router-local traffic. IPv6 input/forward default-drop is an explicit reference boundary, not historical test evidence.

## FTP control and passive data

```mermaid
flowchart LR
  C["FTP client"] -->|"TCP 21 control"| F["Firewall / optional NAT"]
  F -->|"TCP 21"| S["vsftpd DMZ host"]
  S -.->|"PASV reply: selected port<br/>server listens"| F
  F -.->|"control reply via state"| C
  C -->|"NEW TCP data connection<br/>VIP:50000-50100 or routed DMZ:30000-30100"| F
  F -->|"explicit passive permit<br/>and NAT where needed"| S
  S -->|"download bytes / upload ACKs<br/>same TCP state"| F
  F -->|"return data through state"| C
```

The two ranges are reference settings in [pfSense vsftpd](../configs/vsftpd-pfsense.conf) and [VyOS vsftpd](../configs/vsftpd.conf). The report documents FTP service access but does not preserve those ranges or a complete passive transfer trace. Test listing, download, and read-only upload denial while inspecting firewall state and server logs.
