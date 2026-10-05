# Email, DNS, and publishing troubleshooting

`reconstructed-from-project-records`. Commands are safe diagnostic equivalents for a new lab. The original reports sometimes record a suspected cause without a complete confirming trace; those cases remain marked unresolved.

## Wrong internal Exchange A record

1. **Symptom:** A client reported an outgoing SMTP server connection failure.
2. **Expected:** The configured Exchange hostname resolves to the Exchange VM and accepts the intended client/mail connection.
3. **Initial hypothesis:** Firewall, mailbox, or internal DNS error.
4. **Checks:** Verify mailbox in Exchange Admin Center; run `Resolve-DnsName exchange.corp.example.test -Server 172.24.25.10`; compare with VM address.
5. **Evidence:** The report records an A record pointing one host address away from the Exchange VM.
6. **Root cause:** Incorrect internal A record.
7. **Change:** Correct the A record to `172.24.25.12` in the example plan.
8. **Retest:** Resolve the name again and retry the client connection.
9. **Final result:** The report records the client error resolved.
10. **Lesson:** Check the hostname the client uses before changing mail services or disabling host protection.

## External-to-internal delivery failure

1. **Symptom:** An external-source message returned undelivered rather than reaching an internal mailbox.
2. **Expected:** MX lookup → Postfix queue → transport map → Exchange receive connector → mailbox.
3. **Initial hypothesis:** MX/A record, relay domain/transport map, firewall TCP 25, or namespace resolution.
4. **Checks:** `dig example.org MX`, `postmap -q example.org hash:/etc/postfix/transport`, `postqueue -p`, `journalctl -u postfix`, DNS resolution from each hop, and firewall pass/drop logs.
5. **Evidence:** The report says MX/A and service/firewall checks looked correct; a cross-namespace lookup failed. It does not preserve the queue ID or exact SMTP rejection code.
6. **Root cause:** Not isolated. DNS resolution was suspected, and relay-domain settings were reviewed, but a confirmed failing hop was not recorded.
7. **Change:** No verified final configuration correction is available for this specific failure.
8. **Retest:** A fresh lab should trace one message ID across Postfix and Exchange after correcting the observed DNS/transport error.
9. **Final result:** The broad conclusion says external delivery remained incomplete; a separate appendix describes one successful external-source filtering test. Treat general delivery as unresolved.
10. **Lesson:** An SMTP bounce needs its status code and per-hop logs, not only service-up checks.

## GTUBE not flagged between internal users

1. **Symptom:** A GTUBE test message between internal users was not marked `[SPAM]`.
2. **Expected:** Messages passing through the Postfix/SpamAssassin path receive a spam marker when the test is active.
3. **Initial hypothesis:** Milter disabled or filter service not restarted.
4. **Checks:** `systemctl status spamassassin spamass-milter postfix`, Postfix milter setting, message route and Postfix logs.
5. **Evidence:** Enabling the milter and restarting services did not change an internal-to-internal test; that path did not use the boundary relay.
6. **Root cause:** The test bypassed Postfix/SpamAssassin.
7. **Change:** Send the controlled GTUBE test through an external-origin route to the relay.
8. **Retest:** Compare an external-source GTUBE message with a benign external-source message, checking Postfix logs and delivered headers.
9. **Final result:** The appendix reports a spam-tagged result on the changed path, though it does not reconcile the broad external-delivery conclusion.
10. **Lesson:** A control is tested only if the test traffic traverses it.

## DNSSEC changes did not appear

1. **Symptom:** Zone edits were absent after a manually signed zone had been published.
2. **Expected:** New records appear in the served signed zone and have current signatures.
3. **Initial hypothesis:** Signed file was stale or the serial was not advanced.
4. **Checks:** Inspect BIND's configured zone file, SOA serial, `dig ... +dnssec`, and signing logs.
5. **Evidence:** Manual re-signing made changes appear but had to be repeated after each update.
6. **Root cause:** BIND served a signed artifact not automatically updated from the edited source zone.
7. **Change:** Enable inline signing for the zone on the lab's BIND version.
8. **Retest:** Edit a harmless record, advance serial, reload, and query the new signed RRset.
9. **Final result:** The report records updates working without repeated manual signing.
10. **Lesson:** Publishing signed data is an operational workflow, not a one-time command.

## External OWA access

1. **Symptom:** OWA worked internally but failed from an external client.
2. **Expected:** Public name resolves to the ADC listener, then HTTPS/443 reaches Exchange through the firewall.
3. **Initial hypothesis:** DNS A record, farm listener, firewall/NAT, or certificate path.
4. **Checks:** `dig owa.example.org A`, `curl -vk https://owa.example.org/owa/` from both sides, ADC farm listener/backend, and pfSense WAN/NAT logs.
5. **Evidence:** The recorded ADC farm used HTTP/80 instead of HTTPS/443. The DNS record existed; correction alone did not immediately close the incident.
6. **Root cause:** The listener protocol/port was wrong; the report does not isolate one additional final cause.
7. **Change:** Correct the farm listener and backend to HTTPS/443; update/reload the zone serial as recorded.
8. **Retest:** Repeat from inside and outside while checking the firewall and ADC path.
9. **Final result:** The report says external OWA access worked after the combined changes, without a single-cause trace.
10. **Lesson:** Test DNS, public listener, translation, and backend separately.
