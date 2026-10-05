# Firewall and DMZ troubleshooting

`reconstructed-from-project-records` for the three recorded incidents. The service diagnostics at the end are a `reference-implementation` for a new lab.

## No network interface on public test VM

1. **Symptom:** The Windows test VM had no Ethernet setting, so no address or ping test could be run.
2. **Expected:** A virtual NIC appears and accepts the example public-test address.
3. **Initial hypothesis:** Missing virtual driver or VM NIC assignment.
4. **Checks:** Hypervisor NIC attachment, Windows Device Manager, adapter list, and VirtIO driver status.
5. **Evidence:** Restarting alone did not reveal an adapter; the report records the interface after VirtIO installation.
6. **Root cause:** Required virtual network driver was not present.
7. **Change:** Install the matching Nutanix VirtIO driver in the VM.
8. **Retest:** Confirm adapter appears, assign address/gateway, and ping the local firewall interface.
9. **Final result:** The test VM could be addressed and used for connectivity tests.
10. **Lesson:** Confirm endpoint link and driver state before debugging firewall policy.

## DMZ-to-Windows ping failure

1. **Symptom:** The pfSense DMZ server could not ping the private Windows host.
2. **Expected:** Diagnostic ICMP should reach the host if allowed at both firewall and endpoint.
3. **Initial hypothesis:** Wrong IP/gateway, pfSense rule, or Windows Firewall.
4. **Checks:** Compare `ip route` and `ipconfig /all`, inspect pfSense state/logs, then Windows inbound ICMP rules.
5. **Evidence:** Addresses were correct; disabling Windows Firewall made ping succeed.
6. **Root cause:** Windows Firewall blocked inbound ICMP echo.
7. **Change:** The recorded lab disabled Windows Firewall to diagnose. In a new lab, create a narrow inbound ICMP rule instead.
8. **Retest:** Ping again and verify only the intended diagnostic source is permitted.
9. **Final result:** Ping passed after the lab change.
10. **Lesson:** A firewall path can be correct while the destination host rejects the probe.

## Blocked SSH produced no log

1. **Symptom:** Public-side SSH to VyOS DMZ failed, but no VyOS drop entry appeared.
2. **Expected:** Default-drop policy blocks the flow and logs the matching packet.
3. **Initial hypothesis:** Log filter hid the entry or default-drop logging was disabled.
4. **Checks:** Repeat `nc -vz 172.18.37.10 22`, inspect VyOS forward-filter configuration and logs without a narrow display filter.
5. **Evidence:** Repeating the attempt and changing the view did not show a record; default logging was disabled.
6. **Root cause:** Missing `default-log` on the IPv4 forward filter.
7. **Change:** `set firewall ipv4 forward filter default-log`, then commit and save.
8. **Retest:** Repeat SSH attempt and inspect a fresh timestamped drop.
9. **Final result:** The report records both failed SSH and a corresponding drop log.
10. **Lesson:** Test policy action and observability separately.

## Fresh-lab service diagnostics

If FTP connects on TCP 21 but a listing stalls, compare `pasv_min_port`/`pasv_max_port` with WAN NAT/filter rules, server listen ports, and host firewall/SELinux logs. If TFTP fails, verify the initial UDP 69 packet, negotiated transfer-port traffic, state tracking, and the server's file permissions. If a pfSense login page appears instead of Apache, compare the requested VIP/port with pfSense GUI listener binding and NAT rule precedence. These are diagnostic procedures, not claimed incidents from the preserved report.
