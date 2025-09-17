import asyncio, websockets, json

async def test():
    uri = "ws://localhost:8768"   # 外部制御用ポート
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({
            "action": "speak",
            "text": "テスト発話だよ"
        }))

asyncio.run(test())

