# Physical and logical topology

`reconstructed-from-project-records`. The first diagram represents the three-switch MSTP phase. Port labels identify recorded trunk ports, but the exact cable endpoint for each port should be confirmed on actual equipment.

```mermaid
flowchart TB
  R1["Cisco router 1<br/>VLAN 122/123 gateway"] --> S1["Cisco switch 1<br/>Gi3/0/23 and Gi3/0/47 trunks"]
  R2["Cisco router 2<br/>VLAN 121 gateway"] --> S2["Cisco switch 2<br/>Gi1/0/23 and Gi1/0/47 trunks"]
  S1 ---|"802.1Q: 121,122,123"| S2
  S1 ---|"802.1Q: 121,122,123"| A["Aruba switch<br/>tagged 1,13,15"]
  S2 ---|"802.1Q: 121,122,123"| A
  A -->|"untagged 3"| C121["VLAN 121 client"]
  A -->|"untagged 5"| C122["VLAN 122 client"]
  A -->|"untagged 7"| C123["VLAN 123 client"]
```

The logical view shows VLANs as separate broadcast domains even though they share trunk cables.

```mermaid
flowchart LR
  V121["VLAN 121<br/>10.1.12.0/24"] -->|"gateway 10.1.12.1"| R2["Router 2"]
  V122["VLAN 122<br/>10.2.12.0/24"] -->|"gateway 10.2.12.1"| R1["Router 1"]
  V123["VLAN 123<br/>10.3.12.0/24"] -->|"gateway 10.3.12.1"| R1
  R2 <-->|"recorded static inter-router paths"| R1
```
