# OpenDKIM table entries

`reconstructed-from-project-records`. Create a new signing key on the local mail VM; do not use a course or portfolio key. Example content after generation:

```text
# /etc/opendkim/KeyTable
default._domainkey.example.org example.org:default:/etc/opendkim/keys/example.org/default.private

# /etc/opendkim/SigningTable
*@example.org default._domainkey.example.org

# /etc/opendkim/TrustedHosts
127.0.0.1
172.24.25.12
```

Generate a selector with `opendkim-genkey -D /etc/opendkim/keys/example.org -d example.org -s default`, then publish only the `p=` public-key value from `default.txt` in the authoritative zone. The private `default.private` file stays on the mail server with restricted ownership and permissions. The recorded project configured a selector and Postfix milter, then described a test-message header inspection. A receiver-side SPF/DKIM/DMARC alignment result is not retained.
