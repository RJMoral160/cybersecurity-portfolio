# Port and subnet plan

`reconstructed-from-project-records`. The switching/MSTP phase and the later routed/OSPF phase are separate configurations. Do not load both phases onto one device without reconciling interface ownership.

## Switching and MSTP phase

| VLAN | Subnet | Gateway role | MST instance | Preferred root |
|---|---|---|---|---|
| 121 | `10.1.12.0/24` | Router 2, `10.1.12.1` | 1 | Cisco switch 2 |
| 122 | `10.2.12.0/24` | Router 1, `10.2.12.1` | 2 | Cisco switch 1 |
| 123 | `10.3.12.0/24` | Router 1, `10.3.12.1` | 2 | Cisco switch 1 |

| Device | Ports | Role | VLAN handling |
|---|---|---|---|
| Cisco switch 1 | `Gi3/0/23`, `Gi3/0/47` | Inter-switch/uplink trunks | Tagged 121,122,123 |
| Cisco switch 2 | `Gi1/0/23`, `Gi1/0/47` | Inter-switch/uplink trunks | Tagged 121,122,123 |
| Aruba switch | `1`, `13`, `15` | Tagged uplinks | Tagged 121,122,123 |
| Aruba switch | `3`, `5`, `7` | Endpoint access | Untagged 121,122,123 respectively |

Exact cable endpoints depend on the physical diagram from the original phase; verify with LLDP/CDP and interface status before using these ports in another lab. The three-switch triangle is what requires MSTP loop prevention.

## Routed and OSPF phase

| Segment | Subnet | Interface/gateway |
|---|---|---|
| Edge WAN | `192.0.2.0/24` | Edge router `192.0.2.254`, example upstream `192.0.2.1` |
| Router transit | `192.168.12.0/30` | Router 1 `.1`, router 2 `.2` |
| Router 1 client VLANs | `10.1.12.0/24`, `10.2.12.0/24`, `10.3.12.0/24` | `.1` on subinterfaces 121–123 |
| Router 2 client VLANs | `10.1.112.0/24`, `10.2.112.0/24`, `10.3.112.0/24` | `.1` on subinterfaces 121–123 |
| VyOS wired transit | `172.30.12.128/25` | Router 1 `.129`, VyOS `.130` |
| VyOS wireless clients | `172.30.12.0/25` | VyOS `172.30.12.1` |

The source report's switch phase also had a second public WAN on router 2. It is omitted from the OSPF excerpt so the two phases are not conflated. Only the public WAN values were replaced; these private subnets and VLAN IDs were retained.
