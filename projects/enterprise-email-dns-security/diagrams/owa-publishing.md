# External HTTPS and OWA publishing

`reconstructed-from-project-records`. The NAT mapping is a reference flow to test in a new lab; the report records the ADC listener/backend and an external-access troubleshooting event but does not provide a complete original pfSense export.

```mermaid
flowchart LR
  Browser["External browser"] -->|"owa.example.org resolves<br/>to 198.51.100.13:443"| WAN["pfSense WAN<br/>VIP/NAT check"]
  WAN -->|"E-WEB-01<br/>translated to ADC listener:443"| ADC["Relianoid ADC<br/>outer DMZ"]
  ADC -->|"E-WEB-02<br/>HTTPS 443"| EX["Exchange OWA<br/>172.24.25.12"]
```

The troubleshooting record found an HTTP/80 farm where an HTTPS/443 OWA listener was intended. Check the public DNS answer, WAN translation, firewall pass rule, ADC listener, backend health, and certificate chain separately. A second web farm cannot share the same VIP and listener port without an appropriate host-routing design; the recorded lab used a distinct HTTPS port.
