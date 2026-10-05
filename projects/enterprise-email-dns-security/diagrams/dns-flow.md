# Internal and public DNS flow

`reconstructed-from-project-records`.

```mermaid
flowchart LR
  Client["Internal client"] -->|"corp.example.test query<br/>UDP/TCP 53"| MS["Microsoft DNS<br/>172.24.25.10<br/>inner zone"]
  MS -->|"example.org conditional forward<br/>E-DNS-01"| B1["BIND primary<br/>198.51.100.10<br/>outer zone"]
  B1 -->|"AXFR/IXFR TCP 53<br/>E-DNS-02"| B2["BIND secondary<br/>198.51.100.11"]
  Ext["External resolver"] -->|"MX/A/TXT query<br/>UDP/TCP 53"| B1
```

```mermaid
flowchart LR
  FWD["example.org forward zone"] -->|"mail A"| Mail["198.51.100.12"]
  FWD -->|"MX"| MX["mail.example.org"]
  REV["100.51.198.in-addr.arpa reverse zone"] -->|"12 PTR"| MX
  MS["Internal Microsoft DNS"] -->|"Exchange A"| EX["172.24.25.12"]
```

The external zone supplies public service records. The internal zone supplies directory and Exchange names. A host record in the wrong zone or a stale secondary serial can break the next service even if DNS daemons are running.
