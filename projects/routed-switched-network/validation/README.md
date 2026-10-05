# Network validation runbook

`reconstructed-from-project-records`. Run in an isolated lab after each configuration layer. The “expected” column is a criterion, not original device output.

Run MSTP checks on the **earlier triangle** only. Run OSPF/DHCP/NAT checks on the **later reset-and-rebuilt topology** only; do not infer that both phases were active at once. The [phase files](../README.md#implemented-components) and [reference cable map](../configs/PORT_AND_SUBNET_PLAN.md) identify each build.

| Layer | Command or test | Expected behavior | Failure indicator / first check |
|---|---|---|---|
| VLANs | `show vlan brief` (Cisco); `show vlans` (Aruba) | 121–123 exist; access ports belong to one intended VLAN | Missing VLAN or access-port assignment |
| Trunks | `show interfaces trunk`; Aruba VLAN tagged-port view | Only 121–123 carried on switching-phase uplinks | VLAN absent from allowed list or one end untagged |
| MSTP | `show spanning-tree mst` on both Cisco switches; Aruba spanning-tree view | Instance 1 root is switch 2, instance 2 root is switch 1; one alternate path discards | Region mismatch, unexpected root ID, all triangle links forwarding |
| Gateways | `show ip interface brief`; `ping 10.1.12.1` from VLAN 121 client | Gateway reachable in its own VLAN | Wrong client mask/gateway, trunk tag, or subinterface |
| DHCP | `show ip dhcp pool`, `show ip dhcp binding`, `show running-config`; renew a client lease | Later-phase clients receive `.100–.200`, correct gateway and `10.2.12.53` resolver | Exclusion/pool mismatch, wrong VLAN, missing DNS VM |
| Lab DNS | `dig @10.2.12.53 lab.test A` from router-1 VLAN 122 and router-2 VLAN clients | Local-only A response for `10.2.12.53` | DNS VM interface, gateway, OSPF route, host firewall |
| Routing | `show ip ospf neighbor`, `show ip route ospf`, `show ip route` | Expected neighbor reaches FULL and each remote subnet appears | Missing `network` statement, wrong area, link mismatch |
| NAT | `show ip nat statistics`, `show ip nat translations`, then outbound ping/HTTP | Matching private source gets translation on edge interface | Missing `ip nat inside/outside`, NAT ACL, or default route |
| Policy | `show access-lists WEBSITES`, `show access-lists TFTP` plus allowed and blocked clients | Allowed flow works; denied flow fails; relevant counter changes | Wrong interface/direction, rule order, overbroad wildcard |
| Path | `traceroute 198.51.100.20` or isolated external test host | Hops follow internal gateway then edge | TTL expired repeatedly suggests loop or bad route |

Before OSPF testing, check the later-phase switch-1 trunk allows VLAN 172 and its VyOS port is **access** VLAN 172. `show interfaces trunk`, `show vlan brief`, `show ip ospf neighbor`, and `show ip route 172.30.12.0` must agree. A VM using the wired VyOS alternative is not evidence that wireless radio/association was tested.

Use a controlled test matrix with one host in each VLAN. For web policy, test TCP 80/443 from a permitted client and a restricted client; a successful ICMP echo alone does not validate web access. For TFTP, send a test file from wireless and non-wireless subnets and compare the server log. The recorded lab permitted the wireless path and denied the other path, but the published runbook is for a fresh retest.

Do not interpret a populated OSPF route table as proof that NAT works. Capture the pre-translation source on the inside and the translated source at the edge when possible. Preserve timestamps and the exact rule counters for each test.
