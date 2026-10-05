# Firewall and DMZ role diagram

> Sanitized reconstruction based on a collaborative team laboratory environment.

The source report describes two separate lab environments; they are displayed side by side below. All addresses are illustrative RFC 1918 or RFC 5737 examples.

```mermaid
flowchart LR
  Public[Public test network<br/>203.0.113.0/24] --> PF[pfSense<br/>WAN virtual IP + rules]
  Public --> VY[VyOS<br/>forward filter + NAT]
  PF --> PDMZ[DMZ A<br/>Apache + vsftpd<br/>10.20.10.0/24]
  PF --> PLAN[Private A<br/>Windows directory<br/>10.20.20.0/24]
  VY --> VDMZ[DMZ B<br/>Apache + vsftpd + TFTP<br/>10.30.10.0/24]
  VY --> VLAN[Private B<br/>Windows directory<br/>10.30.20.0/24]
```

Permitted inbound service traffic terminates in the DMZ. Private networks use outbound source NAT. The drawing does not imply that public clients can reach private directory services.
