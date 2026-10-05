# VLAN ports and MSTP

`reconstructed-from-project-records`.

## Trunk and access placement

```mermaid
flowchart LR
  C1["Cisco switch 1<br/>Gi3/0/23, Gi3/0/47<br/>allowed 121,122,123"] <-->|"tagged VLANs"| A["Aruba<br/>tagged 1,13,15"]
  C2["Cisco switch 2<br/>Gi1/0/23, Gi1/0/47<br/>allowed 121,122,123"] <-->|"tagged VLANs"| A
  A -->|"port 3 untagged"| V121["VLAN 121 host"]
  A -->|"port 5 untagged"| V122["VLAN 122 host"]
  A -->|"port 7 untagged"| V123["VLAN 123 host"]
```

## Instance and root selection

```mermaid
flowchart TB
  I1["MST instance 1<br/>VLAN 121"] --> S2["Cisco switch 2<br/>root primary"]
  I2["MST instance 2<br/>VLAN 122,123"] --> S1["Cisco switch 1<br/>root primary"]
  S1 ---|"alternate link"| A["Aruba non-root"]
  S2 ---|"alternate link"| A
  S1 --- S2
```

MSTP decides which redundant port discards per instance. A particular blocked port depends on bridge IDs and path cost; confirm it with `show spanning-tree mst` rather than assuming this drawing fixes the port role. Region name `portfolio-region`, revision `1`, and mappings must match on every switch. The actual lab used a different region label, replaced here consistently.
