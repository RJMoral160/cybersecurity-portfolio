# Routed path and NAT boundary

`reconstructed-from-project-records`. These diagrams represent the later OSPF phase, separate from the MSTP-phase router placement.

## Inter-router traffic

```mermaid
flowchart LR
  Client["VLAN 121 client<br/>10.1.112.0/24"] -->|"gateway 10.1.112.1"| R2["Router 2<br/>OSPF area 0"]
  R2 -->|"192.168.12.2 → 192.168.12.1<br/>transit /30"| R1["Router 1<br/>OSPF area 0"]
  R1 --> Dst["VLAN 122<br/>10.2.12.0/24"]
```

## Outbound NAT

```mermaid
flowchart LR
  Host["Client source<br/>10.1.112.100"] -->|"pre-NAT source 10.1.112.100"| Edge["Router 1<br/>NAT ACL + overload<br/>Gi0/0/0 outside"]
  Edge -->|"post-NAT source 192.0.2.254"| Up["Isolated upstream<br/>192.0.2.1"]
  Up --> Ext["External test service<br/>192.0.2.20"]
```

`192.0.2.0/24` is a documentation network. It illustrates the translation boundary; use a real isolated uplink in a recreation. Verify both the OSPF route and a NAT translation entry before interpreting a failed application request as an ACL issue.
