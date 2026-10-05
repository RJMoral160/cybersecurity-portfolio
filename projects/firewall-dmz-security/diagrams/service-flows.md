# Denied management and FTP data paths

`reconstructed-from-project-records` for blocked SSH; `reference-implementation` for a proposed passive FTP range.

## Denied SSH

```mermaid
flowchart LR
  C["Public test client<br/>203.0.113.10"] -->|"TCP 22 to 172.18.37.10"| VY["VyOS eth2<br/>default drop + default-log"]
  VY -.->|"no forward permit"| S["DMZ B server"]
  VY --> L["Drop log entry"]
```

The recorded test first showed a failed SSH connection without a log. Enabling `default-log` produced the drop record. A failed connection without that record would not, by itself, identify the blocking device.

## FTP control and passive data

```mermaid
flowchart LR
  C["FTP client"] -->|"TCP 21 control<br/>recorded allowance"| F["Firewall + NAT"]
  F -->|"TCP 21"| S["vsftpd DMZ host"]
  S -.->|"passive range proposal<br/>TCP 30000–30049"| F
  F -.->|"data connection to chosen port"| C
```

The passive range is a proposed new-lab configuration in [vsftpd.conf](../configs/vsftpd.conf). The source report documents FTP service access but not this range or a complete passive transfer. Test a directory listing and file download while inspecting both firewall state and server logs.
