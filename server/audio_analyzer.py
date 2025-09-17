import asyncio
import numpy as np
import soundfile as sf
import pyaudio
import threading
from pathlib import Path

class AudioPlayer:
    def __init__(self, callback=None):
        self.callback = callback
        self.is_playing = False
        
    def play_with_analysis(self, wav_file_path):
        """音声ファイルを再生しながら音量レベルを送信"""
        try:
            data, samplerate = sf.read(wav_file_path)
            
            # モノラルに変換
            if len(data.shape) > 1:
                data = np.mean(data, axis=1)
            
            p = pyaudio.PyAudio()
            
            # チャンクサイズ（音量分析の間隔）
            chunk_size = int(samplerate * 0.1)  # 0.1秒間隔
            
            stream = p.open(format=pyaudio.paFloat32,
                          channels=1,
                          rate=samplerate,
                          output=True)
            
            self.is_playing = True
            
            # チャンクごとに再生と音量分析
            for i in range(0, len(data), chunk_size):
                if not self.is_playing:
                    break
                    
                chunk = data[i:i+chunk_size]
                
                # 音量レベル計算（RMS）
                volume_level = np.sqrt(np.mean(chunk**2))
                
                # 0-1の範囲に正規化
                normalized_volume = min(volume_level * 5, 1.0)
                
                # コールバックで音量レベルを送信
                if self.callback:
                    self.callback(normalized_volume)
                
                # 音声出力
                stream.write(chunk.astype(np.float32).tobytes())
            
            # 再生終了
            self.is_playing = False
            if self.callback:
                self.callback(0.0)  # 音量0で終了
                
            stream.stop_stream()
            stream.close()
            p.terminate()
            
        except Exception as e:
            print(f"音声再生エラー: {e}")
            self.is_playing = False
            if self.callback:
                self.callback(0.0)