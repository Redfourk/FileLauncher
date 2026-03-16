import wormhole
from twisted.internet import reactor, defer

APPID = "redfourk.com/example"
RELAY_URL = "ws://relay.magic-wormhole.io:4000/v1"


async def receive_message():
    code = input("Enter the wormhole code: ")
    w = wormhole.create(APPID, RELAY_URL, reactor)

    # 1. Set the code provided by the sender
    w.set_code(code)
    # 2. Wait for the encrypted message
    inbound = await w.get_message()
    print(f"Decrypted message: {inbound.decode()}")

    # 3. Send a confirmation back
    w.send_message(b"Message received!")
    await w.close()
    reactor.stop()


defer.ensureDeferred(receive_message())
reactor.run()
