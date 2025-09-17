import asyncio
import websockets
import json
import random
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import os

browser_clients = set()

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

async def control_handler(websocket):
    async for msg in websocket:
        print("[外部から指令]", msg)
        try:
            data = json.loads(msg)
            await broadcast_to_browser(data)
        except Exception as e:
            print("JSON decode error:", e)

def start_http_server():
    # カレントディレクトリをプロジェクトルートに変更
    original_dir = os.getcwd()
    project_root = os.path.dirname(os.path.dirname(__file__))
    os.chdir(project_root)
    print(f"✅ HTTPサーバー ディレクトリ: {os.getcwd()}")
    
    server = HTTPServer(('localhost', 5000), SimpleHTTPRequestHandler)
    print("✅ HTTPサーバー起動: http://localhost:5000")
    server.serve_forever()

async def idle_loop():
    while True:
        await asyncio.sleep(random.uniform(3, 7))
        await broadcast_to_browser({"action": "blink"})
        if random.random() < 0.3:
            await asyncio.sleep(random.uniform(2, 4))
            await broadcast_to_browser({"action": "monologue", "text": "……ふぅ"})

async def main():
    http_thread = threading.Thread(target=start_http_server, daemon=True)
    http_thread.start()
    
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