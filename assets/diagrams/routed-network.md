# Routed network diagram

> Sanitized reconstruction based on a team laboratory environment in which I served as the primary technical contributor.

The diagrams separate the redundant switching phase from the later routed-policy phase. Network labels and addresses are illustrative RFC 1918 or RFC 5737 examples; neither drawing is an original wiring record.

```mermaid
flowchart LR
  Gateway[Router gateway role<br/>VLAN subinterfaces + DHCP] --> SW1[Cisco switch A<br/>MSTP root, instance 2]
  Gateway --> SW2[Cisco switch B<br/>MSTP root, instance 1]
  SW1 --- SW2
  SW1 --- Aruba[Aruba switch]
  SW2 --- Aruba
  SW1 --> V10[VLAN 10 clients<br/>10.10.10.0/24]
  SW2 --> V20[VLAN 20 clients<br/>10.10.20.0/24]
  Aruba --> V30[VLAN 30 clients<br/>10.10.30.0/24]
```

MSTP blocks a redundant forwarding path per instance to avoid a Layer 2 loop. Router subinterfaces provide the VLAN gateways in the documented switching phase.

```mermaid
flowchart LR
  V10[Segmented client network<br/>10.10.10.0/24] --> Internal[Internal routers<br/>OSPF]
  Internal --> Edge[Edge router<br/>NAT + ACLs]
  Edge --> TestNet[External test network<br/>198.51.100.0/24]
```

The later phase added dynamic routing, edge translation, and access controls. These are role drawings, not executable configurations.
