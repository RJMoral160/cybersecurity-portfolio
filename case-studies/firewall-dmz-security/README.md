# Firewall and DMZ Service Security

## Recruiter summary

I contributed to a team laboratory project that built two segmented firewall environments, one using pfSense and the other VyOS. Each placed a Linux web/file server in a DMZ and a Windows domain controller on a private network. The work used service-specific rules and NAT to make selected services reachable while testing that an unwanted SSH connection was blocked. The available report establishes the team implementation, but does not specify my individual share of every rule or server task.

## Problem or objective

The design needed to provide public HTTP and file-transfer services without placing internal directory systems on the public network. It also needed private clients to reach approved services and the external network. The team built separate WAN, DMZ, and private segments so that each traffic path could be evaluated at a firewall boundary.

## Environment and technologies

The lab used pfSense, VyOS, AlmaLinux with Apache and vsftpd, TFTP on one DMZ server, and Windows Server domain controllers. pfSense used a WAN virtual IP and NAT for one DMZ service host. VyOS used routed access to a different DMZ and source NAT for private clients. The [diagram](../../assets/diagrams/firewall-dmz.md) is a sanitized role reconstruction; addresses are illustrative.

## My contribution and team context

I participated in configuration, integration, testing, and troubleshooting in a team laboratory environment. The current evidence does not assign every firewall rule or service change to a named individual, so this case does not claim sole or majority technical ownership. My stronger owner-provided primary-contributor attribution applies to separate networking and infrastructure courses, not automatically to this one.

## Architecture and implementation

Both firewalls separated a public-facing interface, a DMZ service network, and a private directory/client network. The policy allowed only needed inbound services toward DMZ hosts and handled return traffic for established flows. On VyOS, the forward filter had a default drop action, an established/related allowance, an invalid-state drop, and explicit TCP/UDP service permissions. A source NAT masquerade rule allowed private hosts to use the public interface for outbound traffic. On pfSense, a WAN virtual IP supported translation toward the DMZ server, while outbound NAT handled private-client traffic. The report documents the rule intent and broad outcomes, but its NAT terminology is inconsistent; this account distinguishes inbound service translation from outbound masquerade.

HTTP and FTP were exposed for the DMZ servers, with TFTP only on the VyOS side. FTP requires particular care because its data channel can use separate connections, especially in passive mode. The first lab report does not preserve a detailed passive-port rule audit, so this study does not assert that passive FTP was fully hardened. A production rule set would document the passive range and restrict both control and data paths to the required destinations.

## Validation procedure

The group report records reachability checks among private and DMZ systems, successful access to the required HTTP/FTP services, and a failed public-to-DMZ SSH attempt. VyOS drop logging initially showed no entry for that SSH attempt; logging was enabled and the negative test repeated. The test matrix below summarizes the reported behavior, not a newly executed run.

| Flow | Intended policy | Recorded observation |
|---|---|---|
| Public client → DMZ HTTP/FTP | Permit to service host | Service access reported working |
| Public client → VyOS DMZ TFTP | Permit UDP service | Configured; separate complete transfer evidence is limited |
| Public client → VyOS DMZ SSH | Deny | Connection failed; drop record appeared after logging fix |
| Private client → external network | Permit with source NAT | Internet connectivity reported |
| Public client → private domain controller | Deny by segmentation/policy | Direct exposure was not intended; no complete negative-test artifact preserved |

## Problems, troubleshooting, and resolution

**Missing drop evidence.** A public-side SSH attempt to the VyOS DMZ failed, but the expected log entry was absent. The team repeated the attempt and reviewed the log view. The report identifies disabled default-drop logging; after it was enabled, the repeated blocked connection produced a log entry. The failure of a connection and the logging of a policy decision are separate things to validate.

**Misleading ping result.** A DMZ server could not ping a private Windows system even though the recorded IP settings were correct. The team checked the endpoints and then found that Windows Firewall blocked incoming ICMP. Disabling the endpoint firewall made the test pass in the lab. That was a diagnostic shortcut, not a production recommendation; a narrow ICMP rule or another application-level test would preserve host protection.

**Missing virtual NIC.** A public test VM initially had no usable Ethernet setting. The group checked the virtual device and installed the Nutanix VirtIO driver; the network interface then became available for addressing and tests. This was a host-driver issue rather than a firewall rule issue.

## Security significance and skills demonstrated

The useful security decision was to place publicly reachable services in a DMZ and give each flow a stated reason. The test also showed that a blocked connection without a log may leave an analyst unable to explain the policy outcome. Demonstrated team work includes zone design, pfSense and VyOS policy, NAT, service reachability testing, and distinguishing host, routing, and firewall causes.

## Evidence basis and limitations

A private team report contains topology, rule procedures, test results, configuration appendices, and troubleshooting notes. It does not provide an individual task ledger, a complete rule-by-rule negative test suite, or a production hardening review. The public diagram and table are reconstructions. No original addresses, credentials, screenshots, or configuration exports are published.

## Production improvements

I would replace broad service allowances with source and destination constraints, document pfSense interface versus floating rule behavior, explicitly configure passive FTP data ports or prefer a simpler secure transfer service, retain host firewalls, and send firewall logs to a central collector. I would test each permitted path alongside an adjacent denied path, then record the matching rule and state-table entry.

## Interview talking points

- Explain why a DMZ server and a domain controller belong on different interfaces.
- Trace inbound service translation and outbound private-client masquerade as different flows.
- Explain why allowing FTP control traffic may not be enough for passive data transfers.
- Describe how to tell an endpoint ICMP block from a failed firewall route.
- Show what a denied SSH test proves and what it leaves untested.

## AI assistance

AI helped organize private evidence and write this sanitized reconstruction. The lab work predates this portfolio. See [AI assistance](../../AI_ASSISTANCE.md).
