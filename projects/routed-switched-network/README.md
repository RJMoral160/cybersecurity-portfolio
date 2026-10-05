# Routed and Switched Enterprise Network

## Overview

This project joined Cisco routers and switches, an Aruba switch, and a VyOS router into segmented networks. The records cover two successive phases: a redundant three-switch topology using MSTP and static routes, then a redesigned multi-router network using OSPF, NAT, DHCP, and ACLs. This architecture was implemented in a team laboratory environment, with primary responsibility for configuration, integration, and troubleshooting.

## Objectives

- Carry VLANs 121–123 over controlled trunks while assigning endpoints to untagged access ports.
- Select different MSTP roots for VLAN 121 and VLANs 122–123; retain redundant links without a forwarding loop.
- Route between private subnets, distribute client addresses, and translate permitted outbound traffic at the edge.
- Test both allowed and blocked web/TFTP traffic and isolate routing, NAT, and ACL faults.

## Architecture

The [port and subnet plan](configs/PORT_AND_SUBNET_PLAN.md) separates the MSTP and OSPF phases. In the switching phase, Cisco switch 2 was the instance 1 root and Cisco switch 1 was the instance 2 root. Aruba carried tagged VLANs on uplinks and untagged traffic to clients. In the routed phase, router 1 faced an example external network, router 2 advertised additional VLAN networks, and VyOS joined a wired transit `/25` to a wireless client `/25`. The [diagrams](diagrams/README.md) show physical roles, VLAN placement, root selection, routed traffic, and the NAT boundary.

## Implemented Components

| Component | Role | File |
|---|---|---|
| MSTP/static phase | Triangle switching, VLANs, and static routes | [Cisco 1](configs/mstp-cisco-switch-1.cfg), [Cisco 2](configs/mstp-cisco-switch-2.cfg), [Aruba](configs/mstp-aruba-switch.cfg), [router 1](configs/mstp-static-router-1.cfg), [router 2](configs/mstp-static-router-2.cfg) |
| OSPF phase switches | Tagged router trunks and untagged VyOS transit | [Cisco switch](configs/ospf-cisco-switch-1.cfg), [Aruba switch](configs/ospf-aruba-switch-2.cfg) |
| OSPF phase routers | Gateways, OSPF, NAT, DHCP, and historical ACLs | [router 1](configs/ospf-cisco-router-1.cfg), [router 2](configs/ospf-cisco-router-2.cfg), [DHCP 1](configs/ospf-dhcp-router-1.cfg), [DHCP 2](configs/ospf-dhcp-router-2.cfg), [VyOS](configs/ospf-vyos-router.conf) |
| Reference tightening | Narrower TFTP ACL, offline lab resolver, wired VyOS option | [ACL](configs/ospf-acl-reference.cfg), [DNS resolver](configs/lab-dnsmasq.conf), [wired VyOS](configs/ospf-vyos-wired-reference.conf) |

## Configuration

VLAN creation precedes port assignment. Trunk allowed lists carry only the expected VLANs. The MSTP region name, revision, and VLAN-to-instance mapping must match on all three switches; a mismatch creates a boundary and can change port selection. Router subinterfaces provide the Layer 3 gateway for tagged traffic. Router 1 marks the WAN as NAT outside and the routed LAN as NAT inside, then overloads selected source networks on the WAN interface.

The [historical IOS ACL excerpt](configs/ospf-cisco-router-1.cfg) retains a recorded TFTP wildcard of `0.0.0.255`, which is broader than the wireless `/25`; it is **not** a hardened template. A separate [reference policy](configs/ospf-acl-reference.cfg) uses `0.0.0.127` and a specific destination for a new lab. The original reports also have minor inconsistencies between phase diagrams and configuration exports; use the phase-specific table rather than merging every command into one device config.

## Traffic or Data Flow

An endpoint sends an untagged frame into its access port. A trunk adds the VLAN tag toward the appropriate gateway. Cross-VLAN traffic reaches a router subinterface and returns through a different tagged VLAN. Outbound traffic follows an OSPF-learned or directly connected route to router 1; if its source matches the NAT ACL, the edge changes the source to the example WAN interface address. Inbound return traffic follows the translation state. [Routed-flow diagrams](diagrams/routed-flows.md) separate the pre-NAT and post-NAT addresses.

## Validation

The [validation runbook](validation/README.md) checks VLAN membership, trunk carriage, MSTP roots and blocked ports, OSPF neighbors/routes, NAT translations, ACL counters, ping, traceroute, and allowed/denied application flows. It states the expected behavior and failure indicators. Device output is intentionally not fabricated.

## Troubleshooting

The [troubleshooting record](troubleshooting/README.md) traces the wrong instance root, accidental loop, missing OSPF network coverage, missing NAT outside role, and ACL placement/permit issues from symptom to retest. The root-bridge and NAT incidents illustrate why the configured command alone is not enough: the elected role and translated traffic have to be observed.

## Reproduction Guide

1. Use isolated IOS-capable routers (the records include a Cisco 1921), Cisco switches, an ArubaOS-S switch, a VyOS router, a DNS VM, and clients. The original IOS releases are not preserved; run `show version` and adapt interface syntax. An emulator must implement MSTP and 802.1Q before it can replace physical switching. The VyOS Wi-Fi phase requires compatible radio hardware; a wired VM substitute is described in [the plan](configs/PORT_AND_SUBNET_PLAN.md).
2. Assign interfaces using [the plan](configs/PORT_AND_SUBNET_PLAN.md). Replace the example external network with an isolated lab uplink; do not send RFC 5737 traffic to the Internet. Record actual port-to-port cables before pasting a config.
3. Build VLANs and trunks, then verify membership before connecting the redundant third switch link. Configure the identical MSTP region on all switches and confirm root/blocked states before closing the triangle.
4. For the **later OSPF phase**, start from reset/isolated devices rather than loading historical MSTP configs. Load [later Cisco](configs/ospf-cisco-switch-1.cfg) and [Aruba](configs/ospf-aruba-switch-2.cfg) assignments, then router trunks and transit. Install dnsmasq on a Linux VM at `10.2.12.53` using [lab-dnsmasq.conf](configs/lab-dnsmasq.conf); verify `lab.test` before enabling [DHCP pools](configs/ospf-dhcp-router-1.cfg). Configure OSPF, then NAT and ACLs. Supply a new local wireless credential if enabling Wi-Fi; none is provided here.
5. Add NAT and policy one layer at a time. Run the [validation checks](validation/README.md) after each layer and preserve a copy of the known-good configuration. For rollback, disconnect the redundant link if a loop appears, remove the most recent ACL from the interface if management is lost, or restore the saved device config from console access.

## Project Completion

The reports record completed VLAN/trunk, MSTP, routing, DHCP, NAT, and ACL configuration and successful reachability or policy checks after several corrections. The files here are sanitized excerpts and reconstructions, not full switch/router backups. No independent failover-time measurement, clean-room rebuild, or complete packet capture is published. A later lab could test link failure, convergence time, and ACL behavior with a repeatable capture set.

## Limitations

Device syntax varies by IOS, ArubaOS-S, and VyOS release. The config excerpts are phase-specific and omit secrets, management settings, and unrelated lines. Some recorded test descriptions show outcomes without raw command output; the validation runbook provides a method to repeat them in a new lab.

## Repository Contents

- [`configs/`](configs/) — device excerpts and port/subnet plan.
- [`diagrams/`](diagrams/README.md) — focused topology, MSTP, and routed-flow views.
- [`validation/`](validation/README.md) — commands and pass/fail criteria.
- [`troubleshooting/`](troubleshooting/README.md) — recorded faults and corrective sequence.
