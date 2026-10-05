# Relianoid farm reference

`reference-implementation` using the recorded HTTP/HTTPS listener purposes. Relianoid ADC 7.7.0 was named in the source procedure, but the public addressing and health-check settings below are a new isolated-lab model, not an export.

| Farm | Listener on outer-DMZ ADC `172.24.24.20` | Backend(s), routed via firewall | Health check | Certificate / boundary |
|---|---|---|---|---|
| `exchange` | HTTPS `:443`, host `owa.example.org` | Exchange `172.24.25.12:443` | HTTPS GET `/owa/` with expected healthy status; verify Exchange-specific redirect/auth response | ADC certificate for `owa.example.org`; verify backend TLS certificate/hostname, E-WEB-02 |
| `web` | HTTPS `:8443`, host `www.example.org` | Web1 `172.24.25.13:80`, Web2 `172.24.25.14:80` | HTTP GET `/` returning 200 from each backend after a test index page is installed | ADC certificate for `www.example.org`; TCP 8443 WAN mapping needs a separate rule |

In LSLB → Farms, create each listener with its unique virtual port, add the service and backends, attach the locally issued test certificate, then apply/restart. Bind management GUI only to a separate trusted interface or strict management source; the report's GUI port `444` is not the OWA service port. Confirm health checks through ADC status and a direct backend check before testing the WAN. If inner-DMZ plaintext HTTP is unacceptable, enable backend TLS with verified certificates rather than treating the outer listener's HTTPS as end-to-end encryption. The historical web farm moved to 8443 after a 443 collision with OWA.
