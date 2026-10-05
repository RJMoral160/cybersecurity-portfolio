# Enterprise Email and DNS Security

## Overview

This project integrated an external BIND namespace, internal AD-integrated Microsoft DNS, an outer-DMZ Postfix/SpamAssassin relay, and inner-DMZ Exchange mailboxes. Later work added DNSSEC, SPF/DKIM/DMARC configuration, S/MIME certificates, and an HTTPS publishing path for OWA. This architecture was implemented in a team laboratory environment, with primary responsibility for configuration, integration, and troubleshooting.

## Objectives

- Provide forward and reverse DNS records for external services and internal directory clients.
- Keep mail transport at the outer boundary while Exchange and directory services stay on an inner segment.
- Add sender-authentication records and sign the authoritative DNS zone.
- Validate each DNS and SMTP hop separately and investigate filtering, host-record, and publishing failures.

## Architecture

Two BIND servers served the outer authoritative zone; the secondary received zone transfers from the primary. Internal Microsoft DNS served `corp.example.test` and forwarded the outer namespace to BIND. Postfix at `198.51.100.12` handled the example boundary relay, and Exchange at `172.24.25.12` handled internal mailboxes. The addresses and names are a consistent documentation reconstruction. [Focused diagrams](diagrams/README.md) separate DNS, mail, authentication, filtering, and HTTPS/OWA flows.

## Implemented Components

| Component | Purpose | Artifact |
|---|---|---|
| BIND primary/secondary | Authoritative records, reverse zone, limited transfer | [primary](configs/named-primary.conf), [secondary](configs/named-secondary.conf), [forward zone](configs/example.org.zone), [reverse zone](configs/100.51.198.in-addr.arpa.zone) |
| Microsoft DNS and Exchange | Internal resolution, mailbox transport, outbound connector | [procedure](configs/WINDOWS_DNS_EXCHANGE.md) |
| Postfix and SpamAssassin | Boundary relay and spam marking | [Postfix](configs/postfix-main.cf), [transport map](configs/postfix-transport), [SpamAssassin](configs/spamassassin-local.cf), [milter setup](configs/SPAMASSASSIN_INTEGRATION.md) |
| OpenDKIM and DNS authentication | Signing selector and published TXT records | [OpenDKIM](configs/opendkim.conf), [table entries](configs/OPENDKIM_TABLES.md), [zone](configs/example.org.zone) |
| DNSSEC | Signed zone and update workflow | [DNSSEC procedure](configs/DNSSEC.md) |
| OWA/HTTPS and proxy | Relianoid publication and Tinyproxy path | [publishing procedure](configs/PUBLISHING_AND_PROXY.md) |

## Configuration

Build the authoritative zone before mail transport. Its MX target must have an A record; the reverse zone should map the mail host back to a name. Internal DNS must resolve Exchange directly and the outer zone through its forwarder. The Postfix transport map selects the internal Exchange hop, while the Exchange send connector selects Postfix for outbound mail. Keep `mynetworks` narrow: the source lab configuration included an overly broad public range, so the [published reference](configs/postfix-main.cf) restricts trusted relay clients to loopback and the example Exchange host.

The zone publishes an SPF policy for the example mail relay and a DMARC monitoring policy. The DKIM selector is a commented template until a new key is generated locally; [OpenDKIM tables](configs/OPENDKIM_TABLES.md) show how the signer and domain map to that key. The [DNSSEC procedure](configs/DNSSEC.md) documents the recorded manual signing step and the later inline-signing change without publishing keys. The example does not imply that publishing TXT records alone verifies receiver authentication.

## Traffic or Data Flow

An external sender resolves the MX record, reaches Postfix on TCP 25, passes through the configured filter path, and is routed to Exchange if the recipient domain and transport are correct. An internal sender uses Exchange, which forwards outbound messages to Postfix. A receiving server can separately evaluate SPF against the connecting IP, DKIM against the signed message and DNS selector, and DMARC against aligned identifiers. Internal-to-internal Exchange messages can bypass the Postfix filter entirely; that distinction caused a failed early GTUBE test. The [mail-flow diagram](diagrams/mail-flow.md) and [authentication diagram](diagrams/authentication.md) show the separate decisions.

## Validation

The [validation runbook](validation/README.md) checks BIND syntax, forward/reverse records, zone transfer, internal forwarding, MX resolution, Postfix maps and relay restrictions, internal mailbox access, GTUBE through the intended path, signed DNS records, and OWA publication. Record message IDs and headers per hop in a fresh lab; a successful DNS lookup or service status alone does not prove delivery.

## Troubleshooting

The [troubleshooting record](troubleshooting/README.md) covers a wrong Exchange A record, external-to-internal delivery failure with unresolved final cause, a GTUBE test that bypassed Postfix, DNSSEC updates requiring re-signing, and an OWA listener/publication problem. It keeps the recorded symptom, checks, correction, and retest distinct.

## Reproduction Guide

1. Use isolated VMs for BIND 9.20.2 primary/secondary and a separate validating resolver, Windows DNS/AD, a supported Exchange Server build, one Linux Postfix/SpamAssassin/OpenDKIM relay, a firewall with outer and inner DMZs, and a client. Record exact package releases. Add Relianoid ADC (the report used 7.7.0), OWA, and Tinyproxy only after core mail works.
2. Assign the example addresses in the [configuration files](configs/) to isolated test interfaces; RFC 5737 addresses are illustrative and cannot serve as Internet-facing deployment addresses. Create the internal namespace independently from the external example zone.
3. Load forward/reverse zones and test syntax, serial change, and transfer. Configure Microsoft DNS forwarding and verify both names before installing mail applications.
4. Configure Postfix transport, relay restrictions, and Exchange connectors. Test local mailbox access, then one controlled message per hop with logs and queue IDs. Add SpamAssassin and repeat with a benign message and a GTUBE test through Postfix.
5. Generate new DKIM and DNSSEC keys locally. Publish only public DNS material, test signing and validation, then add a DMARC monitoring record. Configure HTTPS/OWA publication after DNS, listener, firewall, and certificate checks pass separately.
6. Before major changes, copy known-good zone and service configurations into a private snapshot. For DNS rollback, restore prior **content** with a newly advanced SOA serial, reload, allow inline re-signing and secondary transfer, then recheck validating-resolver results; never restore an older serial unchanged. For a failed connector/listener, disable only the new setting while preserving mail logs for diagnosis.

## Project Completion

The records document BIND/Microsoft DNS, Postfix/Exchange, SpamAssassin, DNSSEC, SPF/DKIM/DMARC configuration, internal mailbox operation, and several corrected faults. They describe a DKIM test header and DNSSEC signed-record query. The mail report's broad conclusion says external delivery remained incomplete, while one troubleshooting entry describes a successful external-source spam test; no complete hop-by-hop trace reconciles them. Receiver-side SPF/DKIM/DMARC alignment and a validating-resolver DNSSEC chain result are not preserved. The public files are edited excerpts and reference implementations, not original server exports. A controlled rebuild with queue IDs, logs, and receiver authentication results would close those gaps.

## Limitations

Postfix milter and map types vary by distribution. DNSSEC options vary by BIND release. Certificates, DKIM private keys, and live domain delegation must be generated and managed in the new lab. The example `.org` zone and documentation addresses are suitable for study and syntax checks, not Internet publication.

## Repository Contents

- [`configs/`](configs/) — BIND, Postfix, SpamAssassin, OpenDKIM, DNSSEC, Windows DNS/Exchange, and publishing examples.
- [`diagrams/`](diagrams/README.md) — DNS, mail, authentication, filtering, and OWA paths.
- [`validation/`](validation/README.md) — commands and expected results.
- [`troubleshooting/`](troubleshooting/README.md) — recorded failure sequences.
