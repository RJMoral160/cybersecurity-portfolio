# Inbound and outbound NAT

`reference-implementation` for pfSense target mapping; `reconstructed-from-project-records` for the VyOS source-NAT role.

## Inbound pfSense VIP

```mermaid
flowchart LR
  C["Public client<br/>203.0.113.10"] -->|"original destination<br/>203.0.113.6:80"| PF["pfSense WAN VIP<br/>N1"]
  PF -->|"N2 DNAT to .3.10:80<br/>W10 pass after NAT"| S["DMZ Apache<br/>192.168.3.10:80"]
  S -->|"reply via 192.168.3.1"| PF
  PF -->|"state reverse translation<br/>source VIP .6"| C
```

## Outbound private-client PAT

```mermaid
flowchart LR
  A["Private A<br/>192.168.1.10"] -->|"L20/L30 permitted<br/>pre-NAT source .10"| PF["pfSense N3 PAT"]
  PF -->|"post-NAT source .5"| Up["Isolated upstream<br/>203.0.113.20"]
  Up -->|"return to .5"| PF
  PF -->|"state restores .1.10"| A
  B["Private B<br/>192.168.2.10"] -->|"VyOS rules 70/71<br/>pre-NAT source .10"| VY["VyOS source rule 100<br/>eth2"]
  VY -->|"post-NAT source .4"| Up
  Up -->|"return to .4"| VY
  VY -->|"state restores .2.10"| B
```

Inbound destination mapping and outbound source masquerade solve different routing problems. The report's VyOS DMZ path was routed; no original VyOS destination-NAT command is claimed.
