import asyncio
import websockets
import json
import random

# 接続中のブラウザ (OBS表示用)
browser_clients = set()

# ========== ブラウザ用 (8767) ==========
async def browser_handler(websocket):
    browser_clients.add(websocket)
    try:
        async for msg in websocket:
            print("[ブラウザから受信]", msg)
    finally:
        browser_clients.remove(websocket)

async def broadcast_to_browser(data: dict):
    if browser_clients:
        msg = json.dumps(data)
        print(f"[送信] {msg} -> {len(browser_clients)} browser clients")
        await asyncio.gather(*[ws.send(msg) for ws in browser_clients])
    else:
        print("[送信失敗] 接続中のブラウザなし")


# ========== 外部制御用 (8768) ==========
async def control_handler(websocket):
    async for msg in websocket:
        print("[外部から指令]", msg)
        try:
            data = json.loads(msg)
            # 受け取った指令をブラウザに送信
            await broadcast_to_browser(data)
        except Exception as e:
            print("JSON decode error:", e)

# ========== アイドル動作 ==========
async def idle_loop():
    while True:
        await asyncio.sleep(random.uniform(3, 7))
        await broadcast_to_browser({"action": "blink"})
        if random.random() < 0.3:  # 30%で独り言
            await asyncio.sleep(random.uniform(2, 4))
            await broadcast_to_browser({"action": "monologue", "text": "……ふぅ"})

# ========== メイン ==========
async def main():
    server_browser = await websockets.serve(browser_handler, "localhost", 8767)
    server_control = await websockets.serve(control_handler, "localhost", 8768)
    print("✅ ブラウザ用 WebSocket: ws://localhost:8767")
    print("✅ 外部制御用 WebSocket: ws://localhost:8768")

    await asyncio.gather(
        idle_loop(),
        server_browser.wait_closed(),
        server_control.wait_closed()
    )

if __name__ == "__main__":
    asyncio.run(main())
