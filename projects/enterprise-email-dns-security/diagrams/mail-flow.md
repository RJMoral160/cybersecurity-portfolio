# SMTP relay and Exchange interaction

`reconstructed-from-project-records`.

```mermaid
flowchart LR
  Sender["External sender"] -->|"MX→198.51.100.12<br/>TCP 25, E-MAIL-01"| PF["Postfix<br/>outer DMZ"]
  PF -->|"transport map<br/>TCP 25, E-MAIL-02"| EX["Exchange<br/>172.24.25.12<br/>inner DMZ"]
  EX --> Box["Internal mailbox"]
```

```mermaid
flowchart LR
  Client["Internal mail client"] --> EX["Exchange<br/>inner DMZ"]
  EX -->|"send connector<br/>TCP 25, E-MAIL-03"| PF["Postfix<br/>198.51.100.12"]
  PF -->|"SMTP to isolated test peer"| Outside["External mail test"]
```

The Postfix transport map and Exchange connector point in opposite directions. Each requires a separate firewall rule and log check. The records do not include a complete external-delivery trace; see [Project Completion](../README.md#project-completion).
