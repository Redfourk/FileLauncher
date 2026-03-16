import wormhole
from twisted.internet import reactor, defer

APPID = "redfourk.com/example"
RELAY_URL = "ws://relay.magic-wormhole.io:4000/v1"

async def send_message():
    w = wormhole.create(APPID, RELAY_URL, reactor)
    w.allocate_code()
    code = await w.get_code()
    print(f"Wormhole code is: {code}")
    w.send_message(b"Yo this message was sent from Redfourk")
    inbound = await w.get_message()
    print(f"Received from peer: {inbound.decode()}")
    await w.close()
    reactor.stop()

defer.ensureDeferred(send_message())
reactor.run()
