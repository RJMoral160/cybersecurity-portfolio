# Windows DNS and Exchange procedure

`reconstructed-from-project-records`. The internal domain controller used AD-integrated Microsoft DNS. Exchange ran in the inner DMZ at the example private address `172.24.25.12`.

1. Install the AD DS and DNS Server roles, create the internal namespace `corp.example.test`, and add an internal host record for Exchange. Check the A record from a client before configuring mail applications.
2. In DNS Manager, open server **Properties → Forwarders** and set approved upstream resolvers. The later web-service phase also used **Conditional Forwarders → New Conditional Forwarder** for the outer example namespace. In a recreation, use `example.org` with master `198.51.100.10` and verify the firewall allows DNS to that server.
3. In Exchange Admin Center, create a send connector for outbound Internet mail that routes through the Postfix relay at `198.51.100.12`. Set the connector scope and permitted source servers explicitly. Keep inbound SMTP from Postfix limited to the Exchange transport endpoint.
4. Verify mailbox access on the internal client, then test a controlled message through each hop. OWA publishing used a Relianoid HTTPS listener in the later phase; see [publishing procedure](PUBLISHING_AND_PROXY.md).

Useful PowerShell checks in a fresh lab:

```powershell
Resolve-DnsName exchange.corp.example.test -Server 172.24.25.10
Resolve-DnsName mail.example.org -Server 172.24.25.10
Get-SendConnector | Format-Table Name,AddressSpaces,SmartHosts
Get-ReceiveConnector | Format-Table Name,Bindings,RemoteIPRanges
```

The commands inspect the environment; their output depends on the local build. The report's internal client failure was corrected by fixing an Exchange A record with the wrong address.
