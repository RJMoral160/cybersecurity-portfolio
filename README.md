# Cybersecurity Portfolio

Technical project records for routed networks, enterprise mail and DNS, DMZ firewalls, and a local vulnerability-evidence pipeline. Each project keeps its architecture, configuration excerpts, validation steps, and troubleshooting near the implementation.

## Projects

| Project | Objective | Major technologies | Implementation artifacts | Status |
|---|---|---|---|---|
| [Routed and switched network](projects/routed-switched-network/README.md) | Segment client networks, control redundant paths, and route traffic through an edge | Cisco IOS, ArubaOS-S, VyOS, VLANs, MSTP, OSPF, NAT | [device configurations](projects/routed-switched-network/configs/), [validation](projects/routed-switched-network/validation/README.md), [diagrams](projects/routed-switched-network/diagrams/README.md) | Reconstructed and documented |
| [Enterprise email and DNS](projects/enterprise-email-dns-security/README.md) | Integrate internal/external DNS and a filtered mail relay | BIND, Microsoft DNS, Postfix, Exchange, SpamAssassin, DNSSEC, OpenDKIM | [zone/configuration files](projects/enterprise-email-dns-security/configs/), [validation](projects/enterprise-email-dns-security/validation/README.md), [diagrams](projects/enterprise-email-dns-security/diagrams/README.md) | Reconstructed and documented |
| [Firewall and DMZ security](projects/firewall-dmz-security/README.md) | Isolate public services from private networks and validate allowed/blocked paths | pfSense, VyOS, Apache, vsftpd, TFTP, NAT | [rules and service configs](projects/firewall-dmz-security/configs/), [flow tests](projects/firewall-dmz-security/validation/README.md), [diagrams](projects/firewall-dmz-security/diagrams/README.md) | Reconstructed and documented |
| [Vulnerability evidence pipeline](projects/cef-001/README.md) | Separate discovery, advisory correlation, applicability, remediation, and retest records | Python 3, JSON, unittest | [source](projects/cef-001/src/), [tests](projects/cef-001/tests/), [synthetic data](projects/cef-001/data/synthetic/), [sample output](projects/cef-001/examples/sample_report.md) | Active |

## Project Architecture

The network project supplies VLAN, routing, and edge-policy examples. The email/DNS project builds services across internal and outer namespaces. The firewall project documents separate public, DMZ, and private zones. The Python project is an independent offline workflow for structured vulnerability records.

## Implementations

- Network: [Cisco/Aruba/VyOS configuration set](projects/routed-switched-network/configs/), [port and subnet plan](projects/routed-switched-network/configs/PORT_AND_SUBNET_PLAN.md), [validation commands](projects/routed-switched-network/validation/README.md), [troubleshooting](projects/routed-switched-network/troubleshooting/README.md), [reproduction](projects/routed-switched-network/README.md#reproduction-guide).
- Email/DNS: [BIND zone](projects/enterprise-email-dns-security/configs/example.org.zone), [Postfix relay](projects/enterprise-email-dns-security/configs/postfix-main.cf), [mail/DNS checks](projects/enterprise-email-dns-security/validation/README.md), [troubleshooting](projects/enterprise-email-dns-security/troubleshooting/README.md), [reproduction](projects/enterprise-email-dns-security/README.md#reproduction-guide).
- Firewall/DMZ: [VyOS policy](projects/firewall-dmz-security/configs/vyos-firewall.conf), [pfSense rule/NAT tables](projects/firewall-dmz-security/configs/PFSENSE_RULES.md), [flow validation](projects/firewall-dmz-security/validation/README.md), [troubleshooting](projects/firewall-dmz-security/troubleshooting/README.md), [reproduction](projects/firewall-dmz-security/README.md#reproduction-guide).
- Python pipeline: [source and tests](projects/cef-001/README.md#repository-contents), [run instructions](projects/cef-001/README.md#reproduction-guide), [sample report](projects/cef-001/examples/sample_report.md).

## Project Status

The network records include tested VLAN/MSTP and later routing/NAT work; the public phase configs have not been rebuilt on the original devices. Email/DNS records include internal mail and service integration, but a complete external-delivery trace and validating-resolver result are not preserved. Firewall records include segmentation and selected service/deny tests; the added passive-FTP and management policies are untested reference settings. CEF-001 runs offline with synthetic data and remains active. Artifact labels are defined in the [Artifact Guide](ARTIFACT_GUIDE.md).

## Repository Structure

`projects/<name>/configs/` holds device and service settings; `diagrams/` holds traffic and architecture views; `validation/` holds checks and expected behavior; `troubleshooting/` records faults and corrections. The Python project also has `src/`, `tests/`, `data/`, and `examples/`. [PROJECT_INDEX.md](PROJECT_INDEX.md) links technologies to specific files and tests. [REPOSITORY_NOTES.md](REPOSITORY_NOTES.md) explains the committed ignore rules.

Run `python3 tools/check_repo.py` for offline links, JSON, address, secret-pattern, and diagram-fence checks. `python3 -m unittest discover -s projects/cef-001/tests -v` runs the Python tests. Diagram **rendering** requires Mermaid CLI and is a separate CI step; static checks do not substitute for it.
