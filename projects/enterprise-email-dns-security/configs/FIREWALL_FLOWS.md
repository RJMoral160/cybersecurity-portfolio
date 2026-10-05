# Service-flow rules

`reference-implementation`. Identifiers below are documentation IDs for a new lab, not original pfSense rule numbers. Apply rules on the interface where the source traffic enters and verify the matching state/NAT entry.

| ID | Source | Destination | Service | Reason |
|---|---|---|---|---|
| E-DNS-01 | Internal DNS `172.24.25.10` | BIND primary/secondary `198.51.100.10/.11` | UDP/TCP 53 | Forward outer-namespace queries |
| E-DNS-02 | Secondary BIND `.11` | Primary BIND `.10` | TCP 53 | Zone transfer |
| E-MAIL-01 | Isolated external sender | Postfix `198.51.100.12` | TCP 25 | Inbound SMTP to boundary relay |
| E-MAIL-02 | Postfix `.12` | Exchange `172.24.25.12` | TCP 25 | Controlled inner delivery |
| E-MAIL-03 | Exchange `172.24.25.12` | Postfix `.12` | TCP 25 | Outbound send connector |
| E-WEB-01 | External HTTPS client | ADC example VIP `198.51.100.13` | TCP 443 | OWA listener |
| E-WEB-02 | ADC inner-side address | Exchange `172.24.25.12` | TCP 443 | OWA backend |

Inbound DNS query access to the authoritative server and external SMTP delivery need separate WAN rules. Return traffic should be governed by firewall state. This table does not authorize broad access from the outer to inner DMZ.
