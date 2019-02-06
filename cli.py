import asyncio
import json

from connectrum import ElectrumErrorResponse
from connectrum.client import StratumClient
from connectrum.svr_info import ServerInfo
from pycoin.services import spendables_for_address
from pycoin.tx.tx_utils import create_tx, sign_tx
import bitcoin


async def interact(conn, svr, connector, method, args, verbose=False):
    try:
        await connector
    except Exception as e:
        print("Unable to connect to server: %s" % e)
        return -1

    print("\nConnected to: %s\n" % svr)

    if verbose:
        donate = await conn.RPC("server.donation_address")
        if donate:
            print("Donations: " + donate)

        motd = await conn.RPC("server.banner")
        print("\n---\n%s\n---" % motd)

    # XXX TODO do a simple REPL here

    if method:
        print("\nMethod: %s" % method)

    # risky type cocerce here
    args = [(int(i) if i.isdigit() else i) for i in args]

    try:
        rv = await conn.RPC(method, *args)
        print(json.dumps(rv, indent=1))
    except ElectrumErrorResponse as e:
        print(e)

    conn.close()


def main():
    c = Bitcoin(testnet=True)

    return 0

    spendables = spendables_for_address(address)
    tx = create_tx(spendables, [send_all_to])
    print('TX created:', repr(tx))
    sign_tx(tx, [private_key.wif(False), private_key.wif(True)])
    print('Final TX:', tx)

    exit()
    loop = asyncio.get_event_loop()
    svr = ServerInfo("5.9.227.226", "5.9.227.226", ports="s50002")
    conn = StratumClient()
    connector = conn.connect(svr, "s", use_tor=svr.is_onion, disable_cert_verify=True)

    loop.run_until_complete(
        interact(
            conn,
            svr,
            connector,
            "blockchain.address.get_balance",
            ["mhLJkjCasdkGs2VXcap2ub77yQXWGvCMzi"],
        )
    )

    loop.close()

    # print("OK")


if __name__ == "__main__":
    main()
