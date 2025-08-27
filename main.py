import json
import platform
from argparse import ArgumentParser
from urllib.request import Request, urlopen

OS_TYPE = platform.system().lower()

if OS_TYPE == "windows":
    AUTHTOKEN_PATH = "C:\\ProgramData\\ZeroTier\\One\\authtoken.secret"
elif OS_TYPE == "linux":
    AUTHTOKEN_PATH = "/var/lib/zerotier-one/authtoken.secret"
elif OS_TYPE == "darwin":
    AUTHTOKEN_PATH = "/Library/Application Support/ZeroTier/One/authtoken.secret"
else:
    raise Exception("Unsupported OS type: {}".format(OS_TYPE))


def read_authtoken(authtoken: str):
    with open(authtoken, "r") as file:
        return file.read().strip()


def status(api_url: str, authtoken: str):
    req = Request(f"{api_url}/status", headers={"X-ZT1-AUTH": authtoken})
    with urlopen(req) as response:
        text = response.read().decode("utf-8")
    return json.loads(text)


def list_networks(api_url: str, authtoken: str):
    req = Request(f"{api_url}/controller/network", headers={"X-ZT1-AUTH": authtoken})
    with urlopen(req) as response:
        text = response.read().decode("utf-8")
    return json.loads(text)


def show_network(api_url: str, authtoken: str, network_id: str):
    req = Request(
        f"{api_url}/controller/network/{network_id}", headers={"X-ZT1-AUTH": authtoken}
    )
    with urlopen(req) as response:
        text = response.read().decode("utf-8")
    return json.loads(text)


def list_members(api_url: str, authtoken: str, network_id: str):
    req = Request(
        f"{api_url}/controller/network/{network_id}/member",
        headers={"X-ZT1-AUTH": authtoken},
    )
    with urlopen(req) as response:
        text = response.read().decode("utf-8")
    return json.loads(text)


def show_member(api_url: str, authtoken: str, network_id: str, member_id: str):
    req = Request(
        f"{api_url}/controller/network/{network_id}/member/{member_id}",
        headers={"X-ZT1-AUTH": authtoken},
    )
    with urlopen(req) as response:
        text = response.read().decode("utf-8")
    return json.loads(text)


def delete_member(api_url: str, authtoken: str, network_id: str, member_id: str):
    req = Request(
        f"{api_url}/controller/network/{network_id}/member/{member_id}",
        method="DELETE",
        headers={"X-ZT1-AUTH": authtoken},
    )
    with urlopen(req) as response:
        text = response.read().decode("utf-8")
    return json.loads(text)


def authorize_member(
    api_url: str, authtoken: str, network_id: str, member_id: str, enable: bool = True
):
    data = {"authorized": enable}
    req = Request(
        f"{api_url}/controller/network/{network_id}/member/{member_id}",
        data=json.dumps(data).encode("ascii"),  # type: ignore
        headers={"X-ZT1-AUTH": authtoken},
        method="POST",
    )
    with urlopen(req) as response:
        text = response.read().decode("utf-8")
    return json.loads(text)


if __name__ == "__main__":
    desc = """
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
    """
    parser = ArgumentParser(description=desc)
    parser.add_argument(
        "argv", nargs="*", help="Command line arguments for ZeroTier CLI"
    )
    parser.add_argument(
        "--host", type=str, default="localhost", help="ZeroTier API URL"
    )
    parser.add_argument("--port", type=int, default=9993, help="ZeroTier API port")
    parser.add_argument(
        "--authtoken", type=str, default=None, help="ZeroTier authentication token"
    )
    parser.add_argument(
        "--authtoken_path",
        type=str,
        default=None,
        help="Path to ZeroTier authentication token file",
    )
    args = parser.parse_args()
    argv = args.argv

    api_url = f"http://{args.host}:{args.port}"
    authtoken = args.authtoken or read_authtoken(args.authtoken_path or AUTHTOKEN_PATH)

    cmd = argv[0] if argv else "status"

    if cmd == "status":
        print(json.dumps(status(api_url, authtoken), indent=2))
    elif cmd == "network":
        if len(argv) == 1:
            print(json.dumps(list_networks(api_url, authtoken), indent=2))
        elif len(argv) == 2:
            network_id = argv[1]
            print(json.dumps(show_network(api_url, authtoken, network_id), indent=2))
        else:
            print("Usage: network [<network_id>]")
    elif cmd == "member":
        if len(argv) == 2:
            network_id = argv[1]
            print(json.dumps(list_members(api_url, authtoken, network_id), indent=2))
        elif len(argv) == 3:
            network_id = argv[1]
            member_id = argv[2]
            print(
                json.dumps(
                    authorize_member(api_url, authtoken, network_id, member_id, True),
                    indent=2,
                )
            )
        else:
            print("Usage: member <network_id> [<member_id>]")
    elif cmd == "authorize":
        if len(argv) == 3:
            network_id = argv[1]
            member_id = argv[2]
            print(
                json.dumps(
                    authorize_member(api_url, authtoken, network_id, member_id, True),
                    indent=2,
                )
            )
        else:
            print("Usage: authorize <network_id> <member_id>")
    elif cmd == "deauthorize":
        if len(argv) == 3:
            network_id = argv[1]
            member_id = argv[2]
            print(
                json.dumps(
                    authorize_member(api_url, authtoken, network_id, member_id, False),
                    indent=2,
                )
            )
        else:
            print("Usage: deauthorize <network_id> <member_id>")

    elif cmd == "delete":
        if len(argv) == 3:
            network_id = argv[1]
            member_id = argv[2]
            print(
                json.dumps(
                    delete_member(api_url, authtoken, network_id, member_id), indent=2
                )
            )
        else:
            print("Usage: member <network_id> <member_id>")
    else:
        print(f"Unknown command: {cmd}")
        print(
            "Available commands: status, network, member, authorize, deauthorize, delete"
        )
        print(desc)
    exit(0)
