import asyncio
import json

from connectrum import ElectrumErrorResponse
from connectrum.client import StratumClient
from connectrum.svr_info import ServerInfo
from cprint import cprint


async def interact(conn, svr, connector, method, args, verbose=False):
    try:
        await connector
    except Exception as e:
        print("Unable to connect to server: %s" % e)
        return -1

    cprint.info("\nConnected to: %s\n" % svr)

    if verbose:
        donate = await conn.RPC('server.donation_address')
        if donate:
            cprint.info("Donations: " + donate)

        motd = await conn.RPC('server.banner')
        cprint.info("\n---\n%s\n---" % motd)

    # XXX TODO do a simple REPL here

    if method:
        cprint.warn("\nMethod: %s" % method)

    # risky type cocerce here
    args = [(int(i) if i.isdigit() else i) for i in args]

    try:
        rv = await conn.RPC(method, *args)
        cprint.ok(json.dumps(rv, indent=1))
    except ElectrumErrorResponse as e:
        cprint.err(e)

    conn.close()


def main():
    svr = ServerInfo("test-net", "testnet.hsmiths.com", ports="s50002")
    loop = asyncio.get_event_loop()
    conn = StratumClient()
    connector = conn.connect(svr, disable_cert_verify=True)
    loop.run_until_complete(
        interact(conn, svr, connector, "blockchain.address.get_balance", ["3KF9nXowQ4asSGxRRzeiTpDjMuwM2nypAN"]))
    loop.close()


if __name__ == "__main__":
    main()
