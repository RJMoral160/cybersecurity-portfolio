# SpamAssassin and Postfix integration

`reference-implementation`. The project record shows Postfix, SpamAssassin, and `spamass-milter`, but one appended config points a Postfix milter at port `783`, normally used by `spamd` rather than by a milter. This reference gives the milter its own loopback endpoint at `8893`; confirm the service's socket syntax on the installed distribution.

1. On the relay VM, install distribution-packaged Postfix, SpamAssassin, and `spamass-milter`. Record `postconf mail_version`, `spamassassin --version`, and the milter package version; service names and socket flags vary by distribution. Place [spamassassin-local.cf](spamassassin-local.cf) under the distribution's SpamAssassin config directory (commonly `/etc/mail/spamassassin/local.cf`) as root-owned, readable by the service.
2. Start `spamd` locally and configure `spamass-milter` to accept Postfix connections on `inet:8893@127.0.0.1`. Keep `spamd`'s own endpoint separate.
3. Add `inet:127.0.0.1:8893` to `smtpd_milters` alongside OpenDKIM's `8891`, as shown in [postfix-main.cf](postfix-main.cf). Reload Postfix only after both endpoints are listening.
4. Check service state with `systemctl status spamassassin spamass-milter postfix`, inspect listeners with `ss -lntp`, and submit a benign control message followed by a GTUBE test through Postfix.

Install [postfix-main.cf](postfix-main.cf) parameters in `/etc/postfix/main.cf` and [postfix-transport](postfix-transport) at `/etc/postfix/transport`; run `postmap /etc/postfix/transport` before `postfix check` and `systemctl reload postfix`. Keep both files root-owned and avoid exposing them through a web root. Confirm `postmap -q example.org hash:/etc/postfix/transport` returns the expected Exchange next hop. The published `milter_default_action = accept` is **fail-open**: mail can continue without filtering/signing when a milter is unavailable. A fail-closed `tempfail` setting would protect enforcement but defer mail during filter outages. Choose after testing alerting, queue behavior, and recovery.

An internal Exchange-to-Exchange message can bypass this boundary filter. The recorded GTUBE failure used that path; switching to an external-source path reached the filter in the troubleshooting appendix. The broad mail-delivery conclusion remains unresolved, so use queue IDs and delivered headers in any new validation.
