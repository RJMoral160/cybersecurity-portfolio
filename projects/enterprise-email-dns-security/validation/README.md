# Email and DNS validation runbook

`reference-implementation`. Commands are for a new isolated lab. No output below is represented as original execution output.

| Check | Command or interface | Expected result | Failure starting point |
|---|---|---|---|
| BIND syntax | `named-checkconf` and `named-checkzone example.org /var/named/example.org.zone` | Configuration and zone parse cleanly | Missing dot, record syntax, wrong file path |
| Forward/reverse | `dig @198.51.100.10 mail.example.org A`; `dig @198.51.100.10 -x 198.51.100.12` | A and PTR name the example mail host | Zone serial/reload, firewall TCP/UDP 53 |
| MX | `dig @198.51.100.10 example.org MX` | MX points to `mail.example.org`, whose A resolves | Missing A or stale secondary zone |
| Secondary | Query same records at `198.51.100.11`; inspect SOA serial | Secondary serial and answers match primary | Transfer ACL, TCP 53, serial not incremented |
| Internal forwarding | `Resolve-DnsName mail.example.org -Server 172.24.25.10` | Internal client receives outer-zone answer | Conditional forwarder, route, DNS firewall rule |
| Exchange host | `Resolve-DnsName exchange.corp.example.test -Server 172.24.25.10` | Internal A record equals actual Exchange address | Wrong A record before SMTP troubleshooting |
| Postfix config/map | `postfix check`; `postmap -q example.org hash:/etc/postfix/transport` | Check succeeds and map selects Exchange hop | Wrong map type/path or missing `postmap` build |
| Relay path | `postqueue -p`; `journalctl -u postfix`; controlled message with unique subject | Queue ID advances to Exchange; delivery status recorded | Recipient restriction, transport, firewall TCP 25, DNS |
| Filter | `systemctl status spamassassin spamass-milter`; controlled external-source GTUBE and benign message | GTUBE tagged on Postfix path; benign message not tagged | Message bypassed relay, milter disabled, log mismatch |
| SPF/DMARC | `dig @198.51.100.10 example.org TXT`; `dig @198.51.100.10 _dmarc.example.org TXT` | Published values match intended policy | Stale zone or wrong owner name |
| DKIM | `opendkim-testkey -d example.org -s default -vvv`; inspect receiver header | Public selector available; signed test message verified by receiver | Key mismatch, milter/socket, header alteration |
| DNSSEC | `dig @198.51.100.10 example.org DNSKEY +dnssec`; then query a validating resolver | RRSIG/DNSKEY present, validated chain succeeds where delegation exists | Unsigned update, DS mismatch, stale keys |
| OWA | `curl -vk https://owa.example.org/owa/` from inside and isolated outside clients | TLS listener and upstream Exchange response | DNS, VIP/NAT, firewall 443, ADC farm, certificate |

Record both successful and failed paths. For external mail, preserve a message ID and timestamps at the sender, Postfix, Exchange, and recipient. GTUBE must traverse Postfix to test the deployed SpamAssassin path. Use a benign message as a negative control. Do not move DMARC to quarantine/reject based only on a DNS TXT query.
