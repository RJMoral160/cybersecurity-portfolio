# External HTTPS and OWA publishing

`reconstructed-from-project-records`. The NAT mapping is a reference flow to test in a new lab; the report records the ADC listener/backend and an external-access troubleshooting event but does not provide a complete original pfSense export.

```mermaid
flowchart LR
  Browser["Isolated client<br/>198.51.100.30"] -->|"owa.example.org<br/>198.51.100.13:443"| WAN["Firewall WAN<br/>DNAT E-WEB-01"]
  WAN -->|"translated destination<br/>172.24.24.20:443"| ADC["Relianoid listener<br/>outer DMZ 172.24.24.20"]
  ADC -->|"routed E-WEB-02<br/>source .20 to :443"| EX["Exchange OWA<br/>inner DMZ 172.24.25.12"]
  EX -->|"return via inner gateway<br/>172.24.25.1"| ADC
  ADC -->|"stateful return via<br/>outer gateway 172.24.24.1"| WAN
  WAN -->|"reverse DNAT as<br/>198.51.100.13"| Browser
```

The troubleshooting record found an HTTP/80 farm where an HTTPS/443 OWA listener was intended. Check the public DNS answer, WAN translation, firewall pass rule, ADC listener, backend health, and certificate chain separately. A second web farm cannot share the same VIP and listener port without an appropriate host-routing design; the recorded lab used a distinct HTTPS port.
