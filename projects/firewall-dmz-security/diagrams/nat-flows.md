# Inbound and outbound NAT

`reference-implementation` for pfSense target mapping; `reconstructed-from-project-records` for the VyOS source-NAT role.

## Inbound pfSense VIP

```mermaid
flowchart LR
  C["Public client<br/>203.0.113.10"] -->|"original destination<br/>203.0.113.6:80"| PF["pfSense WAN VIP<br/>P-VIP-01"]
  PF -->|"P-NAT-01 destination map<br/>P-WAN-01 allow"| S["DMZ Apache<br/>192.168.3.10:80"]
  S -->|"stateful reply/reverse mapping"| C
```

## Outbound private-client PAT

```mermaid
flowchart LR
  A["Private A<br/>192.168.1.10"] -->|"pre-NAT source .10"| PF["pfSense P-NAT-02"]
  PF -->|"post-NAT source<br/>203.0.113.5"| Up["Isolated upstream"]
  B["Private B<br/>192.168.2.10"] -->|"pre-NAT source .10"| VY["VyOS source rule 100<br/>eth2"]
  VY -->|"post-NAT source<br/>203.0.113.4"| Up
```

Inbound destination mapping and outbound source masquerade solve different routing problems. The report's VyOS DMZ path was routed; no original VyOS destination-NAT command is claimed.
