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

These are recorded *port roles*, not a verified end-to-end cable ledger. The original report refers to a physical table, but the public reconstruction does not assert the exact peer at each triangle port. For a new lab, connect one router and one inter-switch link at a time, record both endpoints with LLDP/CDP and interface status, then close the triangle only after MSTP regions and root placements match.

## Routed and OSPF phase

| Segment | Subnet | Interface/gateway |
|---|---|---|
| Edge WAN | `192.0.2.0/24` | Edge router `192.0.2.254`, example upstream `192.0.2.1` |
| Router transit | `192.168.12.0/30` | Router 1 `.1`, router 2 `.2` |
| Router 1 client VLANs | `10.1.12.0/24`, `10.2.12.0/24`, `10.3.12.0/24` | `.1` on subinterfaces 121–123 |
| Router 2 client VLANs | `10.1.112.0/24`, `10.2.112.0/24`, `10.3.112.0/24` | `.1` on subinterfaces 121–123 |
| VyOS wired transit | `172.30.12.128/25` | Router 1 `.129`, VyOS `.130` |
| VyOS wireless clients | `172.30.12.0/25` | VyOS `172.30.12.1` |

| Reference cable | Endpoint A | Endpoint B | Tagging |
|---|---|---|---|
| O1 | Router 1 `Gi0/0/1` | Cisco switch 1 `Gi3/0/1` | 121,122,123,172 tagged |
| O2 | Cisco switch 1 `Gi3/0/3` | VyOS `eth0` | VLAN 172 untagged at switch; no VyOS VIF |
| O3 | Router 1 `Gi0/0/2` | Router 2 `Gi0/0` | Routed `/30`, no VLAN |
| O4 | Router 2 `Gi0/1` | Aruba switch 2 port `1` | 121,122,123 tagged |

The O1–O4 pairings are a **reference port map**, not preserved evidence of individual physical cable endpoints. Router 1's transit subinterface `Gi0/0/1.172` reaches VyOS `eth0` through the access port. Check router-1 and switch trunks both carry 172. The older MSTP triangle does not belong to this later phase.

DHCP uses the isolated resolver VM at `10.2.12.53` in [lab-dnsmasq.conf](lab-dnsmasq.conf), hosted on Cisco switch 1 VLAN 122. Install and start dnsmasq on that VM, set its static IP/gateway `10.2.12.53/24` and `10.2.12.1`, then verify `dig @10.2.12.53 lab.test A` before issuing DHCP leases. It intentionally does not resolve the public Internet.

The recorded VyOS `wlan0` design requires a compatible Wi-Fi adapter/PHY and radio support; a typical virtual NIC cannot become an access point. In a fully wired VM lab, use [the separate wired reference](ospf-vyos-wired-reference.conf) on a second Ethernet interface and treat it as a **wired client subnet** rather than claiming Wi-Fi validation. Keep `eth0` as the `172.30.12.128/25` transit link. Do not run the historical wireless command excerpt unmodified on a VM without radio hardware.

The source report's switch phase also had a second public WAN on router 2. It is omitted from the OSPF excerpt so the two phases are not conflated. Only the public WAN values were replaced; these private subnets and VLAN IDs were retained.
