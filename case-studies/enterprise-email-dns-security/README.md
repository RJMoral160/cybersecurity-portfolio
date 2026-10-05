# Enterprise Email and DNS Security

## Recruiter summary

I served as the primary technical contributor and informal technical lead in a team laboratory environment that integrated BIND and Microsoft DNS with Postfix, SpamAssassin, and Microsoft Exchange. A later phase configured DNSSEC and published SPF, DKIM, and DMARC records. The records support the configuration work and several troubleshooting events. They do not provide a clean, independent proof of full external mail delivery or receiver-side DMARC alignment.

## Problem or objective

The team needed internal directory-based name resolution, an external authoritative namespace, and mail service without exposing the internal mailbox server directly. We placed the relay role in an outer DMZ and Exchange in an inner DMZ, then added mail authentication records and DNS signing. DNS was a dependency, not a side task: a wrong host record or unresolved destination could interrupt mail routing even when both mail services were running.

## Environment and technologies

The lab used AlmaLinux with BIND, Postfix, SpamAssassin, and OpenDKIM; Windows Server with Active Directory-integrated Microsoft DNS and Exchange; pfSense segmentation; and DNSSEC zone signing. The [diagram](../../assets/diagrams/email-dns.md) uses an illustrative `example.org` namespace and documentation addresses.

## My contribution and team context

I led substantial architecture, configuration, integration, validation, and troubleshooting work and guided team members through service problems. The project was completed by a team. The reports establish the environment and technical events; they are not presented as my personal prose.

## Architecture and implementation

Two BIND servers handled the external authoritative namespace and forward/reverse records. Internal Microsoft DNS served the Active Directory namespace and used forwarders for names outside it. This separation gave internal clients the records needed for directory services while allowing mail and public service names to be resolved through the external zone. The source procedures describe BIND zone transfers and reverse lookups, but the public diagram omits the lab’s exact domains and addressing.

Exchange hosted internal mailboxes. A Postfix relay in the outer DMZ handled the boundary with external mail and was integrated with SpamAssassin; an Exchange send connector directed outbound mail toward Postfix. Firewall rules controlled SMTP between the zones. Later configuration published an SPF TXT record, a DKIM public key, and a DMARC `p=none` record; OpenDKIM signing was connected to Postfix through milter settings. The report also describes a signed DNS zone with inline signing. A DMARC record in monitoring mode does not reject spoofed mail, and a DKIM signature observed in one message header does not establish full receiver-side alignment.

## Validation procedure

The reports record DNS queries, internal mailbox access, an attempt to send test mail through the relay, a GTUBE spam-filter test, a DNSSEC query for signed records, a DMARC TXT query, and inspection of a DKIM test message header. They do not preserve a complete, consistent external mail-flow trace from submission through final delivery and receiver authentication results.

| Check | Evidence-supported result | Limit |
|---|---|---|
| BIND and Microsoft DNS records | Forward/reverse zone and forwarder configuration documented | Raw query outputs are private |
| Internal Exchange mail | Lab conclusion reports internal functionality | Does not prove external delivery |
| SPF and DMARC | TXT records documented, DMARC set to `p=none` | No receiver alignment report preserved |
| DKIM | OpenDKIM/Postfix integration and header inspection described | No complete cross-provider verification preserved |
| DNSSEC | Signed-record query and inline-signing change described | No independent chain-validation artifact published |

## Problems, troubleshooting, and resolution

**Mail routing.** External-to-internal messages generated a delivery failure. The team checked the MX/A relationship, firewall SMTP rules, and Postfix configuration. A DNS lookup across the namespaces failed, but the report did not isolate a final root cause. Another section states only internal mail worked, while a problem appendix describes a later externally sourced spam test as successful. I therefore leave end-to-end external delivery unresolved in this public account.

**Internal host record.** A client’s outgoing-server connection failed despite a running Exchange service and mailboxes. The team checked the mailbox setup and internal DNS. The report records an incorrect Exchange A record; correcting the address restored that client connection. The lesson is to verify the hostname the client actually uses before changing the mail service.

**Spam test path.** An internal-to-internal GTUBE message was not tagged as spam. The team checked the filtering service and then changed the test source so the message would traverse the Postfix/SpamAssassin path. The appendix reports a tagged result after that change, though it conflicts with the broader mail conclusion. The important diagnostic point is that a filtering test must pass through the component being tested.

**DNSSEC updates.** Manually signed zone data did not reflect later changes without re-signing. The team moved to inline signing, which the report says removed that repeated manual step. This is an operational improvement, but a production implementation would separately verify the full trust chain and renewal behavior.

## Security significance and skills demonstrated

Mail security depends on routing, DNS, filtering, authentication, and certificates working together. This case demonstrates service integration and careful validation boundaries: publishing SPF/DKIM/DMARC data is different from proving receiver enforcement; signing DNS records is different from verifying every resolver’s trust chain. Skills include BIND, Microsoft DNS, Exchange/Postfix mail flow, OpenDKIM, SpamAssassin test design, DNSSEC, and layered troubleshooting.

## Evidence basis and limitations

Private team reports include procedures, DNS zones, Postfix/OpenDKIM settings, diagrams, and problem records. The appendices include sensitive material and are not published. No raw message header, key, certificate, complete mail log, or original screenshot appears here. The external-delivery conflict and lack of preserved receiver-side SPF/DKIM/DMARC results are substantive limits. No production deployment is claimed.

## Production improvements

I would use dedicated split DNS zones, tightly limit BIND recursion and transfers, document the permitted SMTP paths, protect and rotate signing keys, and record a message ID through each hop. I would test SPF, DKIM, and DMARC alignment at a controlled receiver before moving DMARC beyond monitoring mode. For DNSSEC, I would capture authenticated validation from a validating resolver and rehearse key rollover.

## Interview talking points

- Trace an inbound message from public MX lookup to the Postfix relay and Exchange mailbox.
- Explain why an internal message might bypass a boundary spam filter.
- Separate SPF authorization, DKIM signature verification, and DMARC alignment.
- Describe how an incorrect A record can look like an SMTP service failure.
- Explain what inline DNSSEC signing changes and what still needs validation.

## AI assistance

AI helped organize private evidence and write this sanitized reconstruction. The lab work predates this portfolio. See [AI assistance](../../AI_ASSISTANCE.md).
