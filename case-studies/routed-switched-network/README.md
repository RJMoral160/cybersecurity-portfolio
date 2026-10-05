# Routed and Switched Enterprise Network

## Recruiter summary

I served as the primary technical contributor and informal technical lead in a team laboratory environment that joined Cisco, Aruba, and VyOS devices into a segmented enterprise network. The work covered VLANs and trunks, inter-VLAN routing, DHCP, redundant switching with MSTP, dynamic routing with OSPF, NAT, and access controls. The most useful evidence is the troubleshooting: a wrong spanning-tree root, a switching loop, missing OSPF coverage, and a missing NAT outside designation were diagnosed and corrected in the lab records.

## Problem or objective

The network needed separate broadcast domains for different client groups, a predictable route between them, controlled external access, and redundant switching links without a loop. Later work expanded the network to multiple routers and added policies for web and TFTP traffic. Each new layer depended on the previous one: an ACL result is meaningful only after addressing, VLAN carriage, routing, and NAT are known to work.

## Environment and technologies

Team laboratory hardware included Cisco switches and routers, an Aruba switch, and a VyOS router. The work used IEEE 802.1Q VLAN tagging, router subinterfaces, DHCP, source NAT/PAT, MSTP, OSPF, Cisco ACLs, SSH management, and connectivity tests. The [diagram](../../assets/diagrams/routed-network.md) is a sanitized reconstruction; the displayed networks and labels are illustrative.

## My contribution and team context

I led configuration, integration, validation, and troubleshooting as the primary technical contributor. I guided teammates through routing and switching problems. The project was completed in a team laboratory environment; I do not claim sole authorship of the full environment or its group reports.

## Architecture and implementation

Access ports placed endpoints in one VLAN, while tagged trunk links carried multiple VLANs between switches and toward the router. Router subinterfaces supplied a gateway per VLAN, and DHCP pools supplied client addressing. VLANs reduced broadcast scope and created separate policy points; they were not, by themselves, a firewall. The lab also used both Cisco and VyOS routing configurations at different stages, so the public diagram shows device roles without pretending that every documented stage ran simultaneously.

Redundant switch links required a loop prevention mechanism. MSTP grouped VLAN traffic into instances and assigned different preferred roots, allowing a planned forwarding path while retaining an alternate link. In the later multi-router design, OSPF advertised connected networks and a default route; the edge router applied source NAT for permitted outbound traffic. ACLs then limited selected web and TFTP flows. Rule placement mattered because applying a source-based restriction after NAT could hide the original client subnet.

## Validation procedure

The group records describe checking VLAN membership and trunk carriage, testing gateway and cross-VLAN reachability, inspecting spanning-tree role and port state, testing OSPF reachability, and checking outbound connectivity after NAT. They also record allowed and denied web/TFTP cases. These are laboratory results; no packet captures or command output are reproduced here.

| Question | Recorded check | Result supported by the reports |
|---|---|---|
| Did MSTP select the intended root? | Inspect per-instance spanning-tree state | Wrong root first; corrected election later |
| Did routing cover the connected segments? | Review OSPF statements and ping between devices | Missing area coverage corrected; pings then worked |
| Did outbound translation work? | Check default gateway and NAT interface roles, then retry | Missing outside designation added; external access returned |
| Did restrictions preserve intended access? | Try permitted and blocked web/TFTP paths | Reports record differentiated outcomes; exact lab addresses withheld |

## Problems, troubleshooting, and resolution

**Wrong MSTP root.** The observed root for one VLAN instance was on the unintended switch. The team inspected spanning-tree state and tried manual priorities. The recorded correction used the root-primary command for that instance; a subsequent check showed the intended root. The lesson is to verify the elected bridge, not merely the configured priority.

**Switching loop.** An incorrectly configured inter-switch link created a loop. Port-state inspection pointed to the affected path. Port priority and blocking behavior were corrected, then the reported storm stopped. A production change would include a controlled rollback and interface counters before reconnecting a suspect link.

**Routing and external access.** Some devices could not reach one another because OSPF statements omitted interfaces from area 0. After those statements were corrected, ping tests passed. At the edge, internal hosts still could not reach outside networks even with the default gateway present. Review found a missing NAT outside designation; adding it restored the recorded outbound access. These were separate failures at separate layers.

## Security significance and skills demonstrated

The case shows practical separation of Layer 2 forwarding, Layer 3 reachability, address translation, and policy enforcement. It also shows why a successful ping alone does not prove an ACL, NAT rule, or application flow is correct. Demonstrated skills include mixed-vendor switch integration, VLAN/trunk configuration, MSTP path selection, OSPF troubleshooting, NAT, and allowed/denied traffic testing.

## Evidence basis and limitations

Private team reports contain procedures, topology figures, configuration appendices, test tables, and problem-solving records for the routing and switching phases. The diagram and descriptions here are reconstructed and sanitized. No original device output, complete configuration, failover timing, performance measurement, or independent production deployment is claimed. Some group report explanations simplify protocol behavior; this case study describes the supported behavior rather than treating every sentence as a verified protocol analysis.

## Production improvements

I would keep an address and VLAN register, back up known-good configurations, review trunk allowed lists, restrict management access, and run a repeatable change test for both permitted and denied flows. I would also test a link failure deliberately and record convergence and application impact before describing the design as resilient.

## Interview talking points

- Explain why tagged trunks are needed and where an endpoint should see untagged frames.
- Draw the route from a host in one VLAN to a host in another, then to an external network.
- Explain how an MSTP root is elected and how to verify a blocked link.
- Distinguish an OSPF route omission from a NAT interface error using observed traffic.
- Show where an ACL should be applied if it must distinguish original client subnets.

## AI assistance

AI helped organize private evidence and write this sanitized reconstruction. The lab work predates this portfolio. See [AI assistance](../../AI_ASSISTANCE.md).
