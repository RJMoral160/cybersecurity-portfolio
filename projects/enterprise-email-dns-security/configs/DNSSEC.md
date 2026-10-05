# DNSSEC signing procedure

`reconstructed-from-project-records`. The project generated zone-signing and key-signing keys for the outer BIND zone, uploaded a DS record to a parent DNS service, and later moved from repeated manual re-signing to inline signing.

```sh
# Run in an isolated lab with a real delegated test zone, never against example.org.
dnssec-keygen -a RSASHA256 -b 2048 -n ZONE example.org
dnssec-keygen -a RSASHA256 -b 4096 -f KSK -n ZONE example.org
dnssec-signzone -o example.org example.org.zone
dnssec-dsfromkey Kexample.org.+008+<key-id>.key
dig @198.51.100.10 example.org DNSKEY +dnssec
dig @198.51.100.10 mail.example.org A +dnssec
```

The command list reflects the recorded method, with the key ID left as a placeholder. BIND's inline-signing syntax depends on its release; use the version's documented directive and confirm new zone changes produce updated signed records. Seeing `RRSIG` records on the authoritative server is not the same as validating the parent-to-child chain from a validating resolver. Keep signing keys and trust-anchor files outside the repository.
