# Network troubleshooting records

`reconstructed-from-project-records`. Commands reflect the recorded method or the direct verification for the stated fault. No console transcript is invented.

## Incorrect MSTP root

1. **Symptom:** Instance 1 selected switch 1, though switch 2 was intended for VLAN 121.
2. **Expected:** `show spanning-tree mst 1` should identify switch 2 as root.
3. **Initial hypothesis:** Priority or MSTP region mismatch.
4. **Checks:** Inspect root ID, bridge priority, region name/revision, and instance VLAN mappings on both switches.
5. **Evidence:** The report records the unintended root; manually entered priority values did not change the election.
6. **Root cause:** The intended root placement was not effective in the observed election. The record does not isolate which prior command failed.
7. **Change:** Apply `spanning-tree mst 1 root primary` on switch 2.
8. **Retest:** Run `show spanning-tree mst 1` on all switches.
9. **Final result:** The report records switch 2 as the correct instance 1 root.
10. **Lesson:** Validate the elected bridge after every MSTP change.

## Triangle switching loop

1. **Symptom:** An incorrectly configured link produced a broadcast loop after MSTP was added.
2. **Expected:** Each instance has a discarding path in the three-switch triangle.
3. **Initial hypothesis:** Incorrect port role/priority on the inter-switch link.
4. **Checks:** `show spanning-tree mst`, interface state and counters on the affected link.
5. **Evidence:** The report says port-state inspection located the bad link.
6. **Root cause:** Port priority/blocking behavior on the link was wrong; exact pre-change port values are not preserved in this public record.
7. **Change:** Correct port priority/blocking state; keep the link disconnected while changing it if a storm is active.
8. **Retest:** Reconnect under observation and verify a discarding port and stable counters.
9. **Final result:** The report records the storm ending after the port correction.
10. **Lesson:** Verify MSTP region consistency and blocked paths before closing a physical loop.

## Missing OSPF coverage

1. **Symptom:** Not all switches/networks could be reached after the routed redesign.
2. **Expected:** Remote private subnets appear in `show ip route ospf` and answer controlled pings.
3. **Initial hypothesis:** OSPF network statements or addressing omitted a connected subnet.
4. **Checks:** `show ip ospf neighbor`, `show ip protocols`, `show ip route`, interface addresses and masks.
5. **Evidence:** The report records missing area 0 interface coverage.
6. **Root cause:** Some OSPF statements did not include the relevant interfaces.
7. **Change:** Correct the area 0 network statements on the affected router.
8. **Retest:** Check route installation and repeat the failed pings.
9. **Final result:** The report records successful pings after correction.
10. **Lesson:** Check control-plane adjacency and installed routes separately.

## Edge NAT failure

1. **Symptom:** Internal hosts reached local networks but not the external test network.
2. **Expected:** `show ip nat translations` gains an entry after outbound traffic.
3. **Initial hypothesis:** Default gateway, NAT ACL, or interface roles were wrong.
4. **Checks:** `show ip route 0.0.0.0`, `show running-config interface GigabitEthernet0/0/0`, `show ip nat statistics`.
5. **Evidence:** The report records a valid default route and a missing NAT outside designation.
6. **Root cause:** Edge WAN was not marked `ip nat outside`.
7. **Change:** Add `ip nat outside` to the WAN interface.
8. **Retest:** Generate outbound traffic and inspect NAT translations and external reachability.
9. **Final result:** Outbound access returned in the report.
10. **Lesson:** A correct route does not create a translation; NAT roles must match traffic direction.

## ACL scope and ICMP

The recorded web restriction initially blocked more outbound traffic than intended when placed after source translation. Moving the source-based ACL to inside interfaces restored the intended distinction between client subnets. A separate ICMP test failed because the permit entry was absent; adding it restored pings. Verify placement with `show running-config interface ...` and rule counters with `show access-lists`. Keep the TFTP `/25` versus `/24` wildcard mismatch visible during a new lab review; the broader recorded mask should not be copied as a precise wireless-only restriction.
