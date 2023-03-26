import asyncio
import websockets
import os
import signal
connected = set()


async def echo(websocket, path):

    print(websocket.server_header)
    connected.add(websocket)

    try:

        async for message in websocket:
            for mess in connected:
                if mess != websocket:

                    print(message)

                    await mess.send(message)
    finally:
        connected.remove(websocket)


async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    port = int(os.environ.get("PORT", "8001"))

    async with websockets.serve(echo, "", port):

        await stop  # run forever

asyncio.run(main())
