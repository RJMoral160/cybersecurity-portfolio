# Firewall and DMZ Service Security

## Overview

This project built two separate firewall environments: pfSense and VyOS. Each divided an isolated public test network, a DMZ service host, and a private Windows network. Apache and vsftpd ran in both DMZs; TFTP was configured on the VyOS side. This architecture was implemented in a team laboratory environment.

## Objectives

- Publish required HTTP/FTP services to DMZ hosts while keeping private directory systems off the public path.
- Allow private outbound access through source NAT/PAT and restrict incoming services by interface and port.
- Use a default-drop forward policy and verify an unwanted SSH path fails with a log entry.
- Distinguish firewall faults from endpoint-driver, host-firewall, route, and service failures.

## Architecture

The [interface and route plan](configs/INTERFACES_AND_ZONES.md) shows pfSense WAN/LAN/DMZ and VyOS `eth2`/`eth0`/`eth1` roles. pfSense used a WAN VIP for a NAT mapping toward its DMZ host. VyOS routed to its DMZ in the controlled lab and masqueraded outbound private traffic. [Diagrams](diagrams/README.md) separate the two topologies, NAT directions, service paths, and FTP transfer behavior.

## Implemented Components

| Component | Purpose | Artifact |
|---|---|---|
| pfSense | WAN VIP, service filtering, private outbound NAT | [rule and NAT tables](configs/PFSENSE_RULES.md) |
| VyOS | Default-drop forwarding, state rules, DMZ service allows, source NAT | [command excerpt](configs/vyos-firewall.conf) |
| Apache | HTTP endpoint in each DMZ | [reference vhost](configs/apache-vhost.conf) |
| vsftpd | FTP endpoint and passive-range adaptation | [reference configuration](configs/vsftpd.conf) |
| TFTP | VyOS-side transfer service | [service-port notes](configs/SERVICE_PORTS.md) |

## Configuration

Build and verify interface routes before NAT or firewall policy. On VyOS, rule 10 accepts established/related packets, rule 20 drops invalid packets, rule 30 permits selected private-to-DMZ services, and rules 40/50 permit HTTP/FTP/TFTP toward the DMZ host from the isolated public interface. All other new forward traffic follows the default drop. Source NAT rule 100 masquerades Private B through `eth2`.

On pfSense, the example WAN VIP is `203.0.113.6`; a 1:1 mapping targets the example DMZ host `192.168.3.10`, while WAN filter rules allow only the required service ports. The source report's NAT procedure and architecture disagree about the internal target. The [reference table](configs/PFSENSE_RULES.md) follows the stated DMZ-service architecture and explicitly identifies the discrepancy. The original report did not preserve a passive FTP range; [the proposed range](configs/vsftpd.conf) is for a fresh lab and must be matched by policy.

## Traffic or Data Flow

For pfSense inbound HTTP, the client targets the WAN VIP, NAT selects the DMZ host, the WAN rule permits TCP 80, and return traffic follows state and the reverse translation. Private A outbound traffic uses PAT on the pfSense WAN address. For VyOS, a controlled upstream route targets the DMZ through `eth2`; there is no recorded inbound destination NAT on that side. Private B outbound traffic is source-translated to the VyOS public-test interface. [Flow diagrams](diagrams/nat-flows.md) show original and translated addresses.

## Validation

The [flow test plan](validation/README.md) checks routes, NAT/state entries, HTTP and FTP, a real passive FTP data transfer, TFTP, denied SSH, and firewall logging. It distinguishes recorded lab results from checks proposed for a new build. A failed connection alone is insufficient to prove which firewall rule blocked it.

## Troubleshooting

The [recorded troubleshooting](troubleshooting/README.md) covers a missing virtual NIC driver, Windows Firewall blocking ICMP, and VyOS default-drop logging being disabled. It also gives a diagnostic path for passive FTP and TFTP without inventing a recorded fix for those services.

## Reproduction Guide

1. Create two isolated three-interface firewall VMs, two AlmaLinux DMZ servers, private Windows test systems, and a public-side test client. Do not bridge the example public segment to the Internet.
2. Assign [interface and gateway addresses](configs/INTERFACES_AND_ZONES.md). Verify each host's local gateway, then check firewall route tables. For VyOS routed-DMZ testing, add the lab-only upstream route shown in the plan.
3. Install Apache/vsftpd; configure TFTP only on the VyOS DMZ host. Confirm local service operation before publishing through a firewall. Keep endpoint firewalls enabled and add narrow rules for required tests.
4. On VyOS, apply default drop and state rules first, then service allowances and source NAT. On pfSense, add the VIP, one consistent NAT model, and matching WAN/LAN interface rules. Preserve a copy of the known-good firewall configuration.
5. Run [allowed and blocked flow tests](validation/README.md). Watch rule counters, state tables, and host logs at each hop. If management is lost, use console access to disable the most recent rule or restore the saved configuration; do not open broad temporary WAN rules.

## Project Completion

The report records completed pfSense/VyOS segmentation, Apache/FTP service access, private outbound access, and a blocked SSH attempt after drop logging was enabled. The public VyOS file is a corrected reference implementation based on recorded rule numbers; pfSense tables reconstruct the intended service mapping because the source record conflicts. No full original pfSense export, passive FTP range, end-to-end passive transfer, complete TFTP transfer, or exhaustive deny matrix is preserved. A fresh lab can add those tests and compare firewall logs to server logs.

## Limitations

The VyOS routed DMZ uses an RFC 1918 address and requires an explicit route in this isolated lab. It is not directly routable on the public Internet. pfSense interface rules and NAT display vary by version, and a 1:1 mapping may be broader than required. The reference Apache and vsftpd files are starting points, not production hardening baselines.

## Repository Contents

- [`configs/`](configs/) — interface plan, VyOS excerpt, pfSense rules/NAT, and service examples.
- [`diagrams/`](diagrams/README.md) — zones, NAT, permitted/denied paths, FTP data flow.
- [`validation/`](validation/README.md) — flow matrix and inspection commands.
- [`troubleshooting/`](troubleshooting/README.md) — observed faults and fresh-lab diagnostics.
