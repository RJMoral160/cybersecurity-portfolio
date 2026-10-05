# Service-flow rules

`reference-implementation`. Identifiers below are documentation IDs for a new lab, not original pfSense rule numbers. Apply rules on the interface where the source traffic enters and verify the matching state/NAT entry.

| ID | Source | Destination | Service | Reason |
|---|---|---|---|---|
| E-DNS-01 | Internal DNS `172.24.25.10` | BIND primary/secondary `198.51.100.10/.11` | UDP/TCP 53 | Forward outer-namespace queries |
| E-DNS-02 | Secondary BIND `198.51.100.11` | Primary BIND `198.51.100.10` | TCP 53 | Secondary-initiated AXFR/IXFR after NOTIFY or refresh; transfer data returns primary→secondary |
| E-MAIL-01 | Isolated external sender | Postfix `198.51.100.12` | TCP 25 | Inbound SMTP to boundary relay |
| E-MAIL-02 | Postfix `.12` | Exchange `172.24.25.12` | TCP 25 | Controlled inner delivery |
| E-MAIL-03 | Exchange `172.24.25.12` | Postfix `.12` | TCP 25 | Outbound send connector |
| E-WEB-01 | Isolated external HTTPS client `198.51.100.30` | Original VIP `198.51.100.13:443`; DNAT to ADC `172.24.24.20:443` | TCP 443 | WAN ingress rule matches translated ADC address |
| E-WEB-02 | ADC source `172.24.24.20` | Exchange `172.24.25.12:443` | TCP 443 | Routed outer→inner DMZ; no second DNAT |

Inbound DNS query access to the authoritative server and external SMTP delivery need separate WAN rules. Return traffic should be governed by firewall state. This table does not authorize broad access from the outer to inner DMZ.

For E-WEB-01, the ADC uses the outer-DMZ firewall `172.24.24.1` as its gateway. Exchange uses the inner-DMZ firewall `172.24.25.1`. The firewall applies DNAT once at WAN ingress, then routes the ADC→Exchange connection through E-WEB-02. TLS must be configured and validated on both legs if the ADC terminates and re-encrypts HTTPS. This is a new reference mapping; the report does not preserve a complete original NAT export.
