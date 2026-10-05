# Email and DNS architecture

> Sanitized reconstruction based on a team laboratory environment in which I served as the primary technical contributor.

All names and addresses below are illustrative. `example.org` is a reserved example domain; `198.51.100.0/24` is an RFC 5737 documentation network.

```mermaid
flowchart LR
  External[External mail test host<br/>198.51.100.20] -->|SMTP| PF[Postfix + SpamAssassin<br/>Outer DMZ]
  PF -->|Controlled SMTP| EX[Exchange<br/>Inner DMZ]
  Client[Internal client] -->|Mailbox access| EX
  EX -->|Outbound send connector| PF
  Client --> MSDNS[Microsoft DNS<br/>Internal AD namespace]
  MSDNS -->|Forward unresolved names| BIND[BIND authoritative DNS<br/>example.org]
  External -->|MX, SPF, DKIM, DMARC queries| BIND
  BIND --> BIND2[Secondary BIND<br/>Zone transfer]
```

The arrows represent intended service paths and documented configuration. The private reports do not consistently prove final external-to-internal delivery.
