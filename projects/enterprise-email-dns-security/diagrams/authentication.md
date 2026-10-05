# Authentication and filtering paths

`reconstructed-from-project-records`.

```mermaid
flowchart LR
  Msg["Received message"] --> SPF["SPF<br/>connecting IP vs TXT"]
  Msg --> DKIM["DKIM<br/>signature vs selector TXT"]
  SPF --> DMARC["DMARC<br/>identifier alignment<br/>p=none"]
  DKIM --> DMARC
  DMARC --> Result["Receiver result/report"]
```

```mermaid
flowchart LR
  External["External test message<br/>benign or GTUBE"] -->|"TCP 25"| Postfix["Postfix relay"]
  Postfix -->|"milter/filter path"| SA["SpamAssassin"]
  SA -->|"tag or normal delivery"| Exchange["Exchange mailbox"]
  Internal["Internal-to-internal mail"] -->|"stays inside Exchange"| Exchange
```

The original failed GTUBE test used the lower path and bypassed the filter. A receiver's DMARC result requires alignment evidence; a published `p=none` TXT value alone is a monitoring policy, not enforcement.
