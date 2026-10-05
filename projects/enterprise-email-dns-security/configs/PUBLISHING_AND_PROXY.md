# OWA publishing and outbound proxy

`reconstructed-from-project-records`. A later service phase placed Relianoid in the outer DMZ and configured a farm for Exchange OWA in the inner DMZ. Another farm balanced two Apache web servers. Tinyproxy handled outbound HTTP requests from internal clients.

| Listener or service | Original destination | Backend or translated destination | Port | Required boundary rule |
|---|---|---|---|---|
| OWA HTTPS | `owa.example.org` → `198.51.100.13` | Relianoid listener → Exchange `172.24.25.12` | TCP 443 | WAN→ADC 443, ADC→Exchange 443 |
| Web farm | `www.example.org` → `198.51.100.13` | Relianoid listener → two inner-DMZ Apache servers | TCP 80 or separate HTTPS listener | WAN→ADC and ADC→backends |
| Forward proxy | Internal client HTTP | Tinyproxy in inner zone | TCP 8888 | Client→proxy, proxy→approved destination |

The report records an OWA farm initially configured with HTTP/80 instead of HTTPS/443. Correcting the listener and reviewing DNS helped; the troubleshooting section does not isolate one final cause for the external-access failure. A second HTTPS web farm later conflicted with the existing VIP/443 listener; the web farm moved to a different HTTPS port. A recreation must check the WAN NAT rule separately rather than assume the listener correction also fixes publication.

For a new lab, prefer an explicit client proxy configuration unless the proxy supports the intended transparent mode and the firewall translation is tested. The original procedure redirected HTTP through pfSense to Tinyproxy port 8888, but a firewall redirect by itself does not prove every HTTPS or HTTP request was handled correctly. Verify proxy access logs and keep endpoint firewalls enabled with narrow rules.
