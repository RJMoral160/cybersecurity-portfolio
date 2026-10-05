# Zones and allowed paths

`reconstructed-from-project-records`.

```mermaid
flowchart LR
  Public["Isolated public test<br/>203.0.113.0/24"] --> PFW["pfSense<br/>WAN .5 / VIP .6"]
  PFW --> PDMZ["DMZ A 192.168.3.0/24<br/>Apache + vsftpd .10"]
  PFW --> PLAN["Private A 192.168.1.0/24<br/>Windows .10"]
  Public --> VFW["VyOS<br/>eth2 .4"]
  VFW -->|"eth1"| VDMZ["DMZ B 172.18.37.0/24<br/>HTTP/FTP/TFTP .10"]
  VFW -->|"eth0"| VLAN["Private B 192.168.2.0/24<br/>Windows .10"]
```

```mermaid
flowchart LR
  Client["Public test client .10"] -->|"VIP .6 TCP 80/21<br/>W10/W20 after DNAT"| PF["pfSense WAN .5<br/>VIP .6"]
  PF -->|"N2 to .3.10"| PS["DMZ A service<br/>192.168.3.10"]
  Client -->|"VyOS rule 40 TCP 21,80<br/>rule 50 UDP 69"| VY["VyOS eth2"]
  VY -->|"routed eth1"| VS["DMZ B service .10"]
```

VyOS's DMZ path needs the isolated upstream route in the [interface plan](../configs/INTERFACES_AND_ZONES.md); it is not direct Internet routing to RFC 1918 space. pfSense rule IDs are reference-document identifiers, not original device rule numbers.
