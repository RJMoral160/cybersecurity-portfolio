# SpamAssassin and Postfix integration

`reference-implementation`. The project record shows Postfix, SpamAssassin, and `spamass-milter`, but one appended config points a Postfix milter at port `783`, normally used by `spamd` rather than by a milter. This reference gives the milter its own loopback endpoint at `8893`; confirm the service's socket syntax on the installed distribution.

1. Install `spamassassin` and `spamass-milter`; configure the filter threshold in [spamassassin-local.cf](spamassassin-local.cf).
2. Start `spamd` locally and configure `spamass-milter` to accept Postfix connections on `inet:8893@127.0.0.1`. Keep `spamd`'s own endpoint separate.
3. Add `inet:127.0.0.1:8893` to `smtpd_milters` alongside OpenDKIM's `8891`, as shown in [postfix-main.cf](postfix-main.cf). Reload Postfix only after both endpoints are listening.
4. Check service state with `systemctl status spamassassin spamass-milter postfix`, inspect listeners with `ss -lntp`, and submit a benign control message followed by a GTUBE test through Postfix.

An internal Exchange-to-Exchange message can bypass this boundary filter. The recorded GTUBE failure used that path; switching to an external-source path reached the filter in the troubleshooting appendix. The broad mail-delivery conclusion remains unresolved, so use queue IDs and delivered headers in any new validation.
