# Pipeline validation

`synthetic-example`. The tests are executable checks for local program behavior.

| Area | Test method | Expected behavior |
|---|---|---|
| Lifecycle fields | `python3 -m unittest discover -s tests -v` | Missing state-required evidence is rejected |
| Collection integrity | Same suite | Empty, duplicate-ID, non-object, and malformed collections are rejected |
| Report rendering | Same suite | Stable sorted rows and escaped Markdown delimiters |
| Advisory comparison | Same suite | Product/version/condition mismatch is not applicable; missing condition is insufficient evidence |
| Synthetic boundary | Same suite | Non-synthetic observations are not accepted for this startup workflow |

Use the [README commands](../README.md#validation) to regenerate the two sample reports. Check the command exit status and inspect the report contents. The unit suite measures behavior of the implementation; it does not measure scanner accuracy, advisory completeness, remediation effectiveness, or security impact on a real system.
