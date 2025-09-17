import aiohttp
import asyncio
import json
from pathlib import Path

class VoicevoxClient:
    def __init__(self, host="localhost", port=50021):
        self.base_url = f"http://{host}:{port}"
        self.audio_dir = Path("../web/audio")
        self.audio_dir.mkdir(exist_ok=True)
    
    async def synthesize_speech(self, text: str, speaker_id: int = 3):
        """テキストを音声ファイルに変換"""
        try:
            async with aiohttp.ClientSession() as session:
                # 音声クエリ生成
                query_params = {"text": text, "speaker": speaker_id}
                async with session.post(f"{self.base_url}/audio_query", params=query_params) as response:
                    if response.status != 200:
                        print(f"VOICEVOX クエリエラー: {response.status}")
                        return None
                    query_data = await response.json()
                
                # 音声合成
                headers = {"Content-Type": "application/json"}
                synthesis_params = {"speaker": speaker_id}
                async with session.post(
                    f"{self.base_url}/synthesis",
                    params=synthesis_params,
                    json=query_data,
                    headers=headers
                ) as response:
                    if response.status != 200:
                        print(f"VOICEVOX 合成エラー: {response.status}")
                        return None
                    
                    # 音声ファイル保存
                    audio_filename = f"speech_{hash(text) % 10000}.wav"
                    audio_path = self.audio_dir / audio_filename
                    
                    with open(audio_path, "wb") as f:
                        f.write(await response.read())
                    
                    return f"/audio/{audio_filename}"
        
        except Exception as e:
            print(f"VOICEVOX エラー: {e}")
            return None