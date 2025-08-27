```
ZeroTier Controller CLI
------------------------------------------------------------------------------
status                                      :   Show controller status
network     [<network_id>]                  :   List all networks or show specific network details
member       <network_id>   [<member_id>]   :   List all members of a network or show specific member details
authorize    <network_id>   [<member_id>]   :   Authorize a member in a network
deauthorize  <network_id>   [<member_id>]   :   Deauthorize a member in a network
delete:      <network_id>    <member_id>    :   Delete a member from a network
------------------------------------------------------------------------------
--host <host>                               :   ZeroTier API host (default: localhost)
--port <port>                               :   ZeroTier API port (default: 9993)
--authtoken <token>                         :   ZeroTier authentication token
--authtoken_path <path>                     :   Path to ZeroTier authentication token file
------------------------------------------------------------------------------
```
