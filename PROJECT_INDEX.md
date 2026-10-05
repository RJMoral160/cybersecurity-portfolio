# Technical project index

The index points to implementations and their validation methods. Status describes the published artifact, not a production deployment.

| Technology | Implementation | File | Validation | Status |
|---|---|---|---|---|
| Cisco IOS VLAN/MSTP | Earlier static-routing phase | [switch 1](projects/routed-switched-network/configs/mstp-cisco-switch-1.cfg), [switch 2](projects/routed-switched-network/configs/mstp-cisco-switch-2.cfg) | [`show vlan`, trunk, MSTP checks](projects/routed-switched-network/validation/README.md) | Original-sanitized excerpts |
| ArubaOS-S VLAN/MSTP | Tagged and untagged ports, instance mapping | [Aruba config](projects/routed-switched-network/configs/mstp-aruba-switch.cfg) | [Port/MSTP checks](projects/routed-switched-network/validation/README.md) | Original-sanitized excerpt |
| Cisco/VyOS routing | Later OSPF phase | [router 1](projects/routed-switched-network/configs/ospf-cisco-router-1.cfg), [router 2](projects/routed-switched-network/configs/ospf-cisco-router-2.cfg), [VyOS](projects/routed-switched-network/configs/ospf-vyos-router.conf) | [Route/NAT/ACL checks](projects/routed-switched-network/validation/README.md) | Edited excerpts |
| BIND | Forward/reverse zones and primary/secondary config | [zone](projects/enterprise-email-dns-security/configs/example.org.zone), [primary](projects/enterprise-email-dns-security/configs/named-primary.conf) | [`named-checkzone`, `dig`](projects/enterprise-email-dns-security/validation/README.md) | Reconstruction/reference |
| Postfix/SpamAssassin/OpenDKIM | Relay, transport, filtering, signing paths | [Postfix](projects/enterprise-email-dns-security/configs/postfix-main.cf), [filter](projects/enterprise-email-dns-security/configs/spamassassin-local.cf), [OpenDKIM](projects/enterprise-email-dns-security/configs/opendkim.conf) | [Mail-flow and GTUBE checks](projects/enterprise-email-dns-security/validation/README.md) | Excerpt/reference |
| pfSense | VIP, 1:1 and outbound NAT, interface rules | [NAT/rule tables](projects/firewall-dmz-security/configs/PFSENSE_RULES.md) | [Allowed/denied flow tests](projects/firewall-dmz-security/validation/README.md) | Reference mapping |
| VyOS firewall | Default drop, state rules, service permits, NAT | [VyOS rules](projects/firewall-dmz-security/configs/vyos-firewall.conf) | [Firewall and NAT checks](projects/firewall-dmz-security/validation/README.md) | Reference implementation |
| Python | Lifecycle validation and advisory comparison | [source](projects/cef-001/src/), [tests](projects/cef-001/tests/), [fixtures](projects/cef-001/data/synthetic/) | [22 unit tests](projects/cef-001/validation/README.md) | Active, executable |
