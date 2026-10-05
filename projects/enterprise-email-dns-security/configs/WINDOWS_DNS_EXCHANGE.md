# Windows DNS and Exchange procedure

`reconstructed-from-project-records`. The internal domain controller used AD-integrated Microsoft DNS. Exchange ran in the inner DMZ at the example private address `172.24.25.12`.

1. Install the AD DS and DNS Server roles, create the internal namespace `corp.example.test`, and add an internal host record for Exchange. Check the A record from a client before configuring mail applications.
2. In DNS Manager, open server **Properties → Forwarders** and set approved upstream resolvers. The later web-service phase also used **Conditional Forwarders → New Conditional Forwarder** for the outer example namespace. In a recreation, use `example.org` with master `198.51.100.10` and verify the firewall allows DNS to that server.
3. Install a supported Exchange Server release in the isolated AD forest and assign Exchange `172.24.25.12/24` with internal DNS `172.24.25.10`. Create authoritative accepted domain `example.org` and one test mailbox with an `@example.org` SMTP address. This is a reference mailbox assumption, not a preserved original account. The mailbox's address must be verified before testing Postfix transport into Exchange.
4. In Exchange Management Shell, configure a **constrained** receive connector on `172.24.25.12:25` for only the Postfix relay `198.51.100.12/32`, with `AnonymousUsers` permission to deliver to accepted-domain recipients. Do **not** grant anonymous relay to arbitrary domains. Check for overlap with the built-in Front End connector bindings and remote ranges before creation. A reference command (replace the local Exchange server identity) is:

```powershell
New-AcceptedDomain -Name "Lab Mail" -DomainName example.org -DomainType Authoritative
New-ReceiveConnector -Name "Postfix Inbound" -Server EX01 -TransportRole FrontendTransport -Usage Custom -Bindings 172.24.25.12:25 -RemoteIPRanges 198.51.100.12 -PermissionGroups AnonymousUsers
```

5. Create a send connector with address space `*`, source transport server `EX01`, Postfix smart host `198.51.100.12`, and DNS routing disabled. Exchange must resolve internal AD and mailbox names through Microsoft DNS; the Postfix relay must resolve or directly reach the Exchange transport target. Firewall rules E-MAIL-02 and E-MAIL-03 are separate. Microsoft documents the [receive connector binding/range model](https://learn.microsoft.com/en-us/exchange/mail-flow/connectors/receive-connectors) and [smart-host send connector](https://learn.microsoft.com/en-us/powershell/module/exchangepowershell/new-sendconnector).

```powershell
New-SendConnector -Name "Via Postfix Lab Relay" -Usage Internet -AddressSpaces '*' -SmartHosts 198.51.100.12 -DNSRoutingEnabled $false -SourceTransportServers EX01
```

6. Verify mailbox access on the internal client, then test a controlled message through each hop with message tracking and Postfix queue IDs. Do not treat an internal-only Exchange message as a Postfix filter test. OWA publishing used a Relianoid HTTPS listener in the later phase; see [publishing procedure](PUBLISHING_AND_PROXY.md).

Useful PowerShell checks in a fresh lab:

```powershell
Resolve-DnsName exchange.corp.example.test -Server 172.24.25.10
Resolve-DnsName mail.example.org -Server 172.24.25.10
Get-SendConnector | Format-Table Name,AddressSpaces,SmartHosts
Get-ReceiveConnector | Format-Table Name,Bindings,RemoteIPRanges
Get-AcceptedDomain | Format-Table Name,DomainName,DomainType
Get-MessageTrackingLog -Start (Get-Date).AddHours(-1) | Select-Object Timestamp,EventId,Recipients,MessageId
```

The commands inspect the environment; their output depends on the local build. The report's internal client failure was corrected by fixing an Exchange A record with the wrong address.
