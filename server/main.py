import asyncio
import websockets
import json
import random
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import os
import queue
from voicevox_client import VoicevoxClient
from audio_analyzer import AudioPlayer

browser_clients = set()
voicevox = VoicevoxClient()
volume_queue = queue.Queue()

async def browser_handler(websocket):
    browser_clients.add(websocket)
    try:
        async for msg in websocket:
            print("[ブラウザから受信]", msg)
            try:
                data = json.loads(msg)
                if data.get("action") == "speak_text":
                    await handle_speech_request(data.get("text", ""))
            except Exception as e:
                print("ブラウザメッセージ処理エラー:", e)
    finally:
        browser_clients.remove(websocket)

def volume_callback_sync(volume_level):
    """スレッドセーフな音量コールバック"""
    volume_queue.put(volume_level)

async def process_volume_queue():
    """音量キューを処理してブラウザに送信"""
    while True:
        try:
            volume_level = volume_queue.get_nowait()
            await broadcast_to_browser({
                "action": "volume_level",
                "level": volume_level
            })
        except queue.Empty:
            await asyncio.sleep(0.01)

async def handle_speech_request(text: str):
    print(f"[音声合成要求] {text}")
    
    # VOICEVOX で音声ファイル生成
    audio_file = await voicevox.synthesize_speech(text)
    
    if audio_file:
        # 発話開始をブラウザに通知
        await broadcast_to_browser({
            "action": "speech_start",
            "text": text
        })
        
        # 音声再生を別スレッドで実行
        player = AudioPlayer(callback=volume_callback_sync)
        
        def play_audio():
            try:
                player.play_with_analysis(audio_file)
                # 再生終了をキューに追加
                volume_queue.put("END")
            except Exception as e:
                print(f"音声再生エラー: {e}")
                volume_queue.put("END")
        
        audio_thread = threading.Thread(target=play_audio, daemon=True)
        audio_thread.start()
    else:
        print("音声合成失敗")

async def broadcast_to_browser(data: dict):
    if browser_clients:
        msg = json.dumps(data)
        await asyncio.gather(*[ws.send(msg) for ws in browser_clients])

async def control_handler(websocket):
    async for msg in websocket:
        print("[外部から指令]", msg)
        try:
            data = json.loads(msg)
            if data.get("action") == "speak":
                await handle_speech_request(data.get("text", ""))
            else:
                await broadcast_to_browser(data)
        except Exception as e:
            print("JSON decode error:", e)

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        project_root = os.path.dirname(os.path.dirname(__file__))
        super().__init__(*args, directory=project_root, **kwargs)
    
    def log_message(self, format, *args):
        print(f"[HTTP] {format % args}")

def start_http_server():
    server = HTTPServer(('localhost', 5000), CustomHTTPRequestHandler)
    print("✅ HTTPサーバー起動: http://localhost:5000")
    server.serve_forever()

async def volume_queue_processor():
    """音量キュー処理専用タスク"""
    while True:
        try:
            volume_level = volume_queue.get_nowait()
            if volume_level == "END":
                await broadcast_to_browser({"action": "speech_end"})
            else:
                await broadcast_to_browser({
                    "action": "volume_level", 
                    "level": volume_level
                })
        except queue.Empty:
            await asyncio.sleep(0.01)

async def idle_loop():
    while True:
        await asyncio.sleep(random.uniform(3, 7))
        await broadcast_to_browser({"action": "blink"})
        if random.random() < 0.1:
            await asyncio.sleep(random.uniform(2, 4))
            await handle_speech_request("……ふぅ")

async def main():
    http_thread = threading.Thread(target=start_http_server, daemon=True)
    http_thread.start()
    
    server_browser = await websockets.serve(browser_handler, "localhost", 8767)
    server_control = await websockets.serve(control_handler, "localhost", 8768)
    
    print("✅ ブラウザ用 WebSocket: ws://localhost:8767")
    print("✅ 外部制御用 WebSocket: ws://localhost:8768")
    print("✅ 音量レベル連動システム: 有効")

    await asyncio.gather(
        idle_loop(),
        volume_queue_processor(),
        server_browser.wait_closed(),
        server_control.wait_closed()
    )

if __name__ == "__main__":
    asyncio.run(main())