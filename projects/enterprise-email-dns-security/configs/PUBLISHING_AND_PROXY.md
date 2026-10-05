# OWA publishing and outbound proxy

`reconstructed-from-project-records`. A later service phase placed Relianoid in the outer DMZ and configured a farm for Exchange OWA in the inner DMZ. Another farm balanced two Apache web servers. Tinyproxy handled outbound HTTP requests from internal clients.

| Listener or service | Original destination | Backend or translated destination | Port | Required boundary rule |
|---|---|---|---|---|
| OWA HTTPS | `owa.example.org` → `198.51.100.13` | WAN DNAT → ADC `172.24.24.20:443` → routed Exchange `172.24.25.12:443` | TCP 443 | E-WEB-01 and E-WEB-02 |
| Web farm | `www.example.org` → `198.51.100.13` | WAN DNAT → ADC `172.24.24.20:8443` → routed Web1 `.13:80` / Web2 `.14:80` in `172.24.25.0/24` | TCP 8443 | Separate WAN rule and inner-DMZ HTTP backend rules |

The web-farm test URL must include the nondefault port: `https://www.example.org:8443/`. DNS only selects the address; it does not redirect HTTPS from 443 to 8443.
| Forward proxy | Internal client explicit proxy | Tinyproxy `172.24.25.20:8888` | TCP 8888 | Client→proxy, proxy→approved destination |

The report records an OWA farm initially configured with HTTP/80 instead of HTTPS/443. Correcting the listener and reviewing DNS helped; the troubleshooting section does not isolate one final cause for the external-access failure. A second HTTPS web farm later conflicted with the existing VIP/443 listener; the web farm moved to a different HTTPS port. A recreation must check the WAN NAT rule separately rather than assume the listener correction also fixes publication.

For a new lab, use [the explicit Tinyproxy reference](tinyproxy.conf) and [the farm table](RELIANOID_FARMS.md). Set clients' HTTP/HTTPS proxy to `172.24.25.20:8888`, allow only those client subnets, and verify access logs. The original procedure redirected HTTP through pfSense to Tinyproxy port 8888, but a firewall redirect by itself does not prove every HTTPS or HTTP request was handled correctly. Keep endpoint firewalls enabled with narrow rules. For OWA, `curl -k` can isolate a TLS trust problem but is **not** a successful security test; validate `curl --cacert /path/to/local-ca.crt --resolve owa.example.org:443:198.51.100.13 https://owa.example.org/owa/` with a trusted local CA and hostname match in the isolated lab.
