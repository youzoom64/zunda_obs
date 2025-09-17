import asyncio
import websockets
import json

async def test_speech():
    uri = "ws://localhost:8768"
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({
            "action": "speak",
            "text": "新しいテストなのだ"
        }))

asyncio.run(test_speech())