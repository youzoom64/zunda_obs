@echo off
cd /d "%~dp0"
echo ずんだもんシステム起動中...

:: VOICEVOXの起動確認
echo VOICEVOXの起動を確認中...
curl -s http://localhost:50021/version >nul 2>&1
if %errorlevel% neq 0 (
    echo エラー: VOICEVOXが起動していません
    echo VOICEVOXを先に起動してください
    pause
    exit /b 1
)

:: 仮想環境の有効化
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo 仮想環境を有効化しました
) else (
    echo 警告: 仮想環境が見つかりません
)

:: 依存関係のインストール確認
pip show aiohttp >nul 2>&1
if %errorlevel% neq 0 (
    echo 依存関係をインストール中...
    pip install -r requirements.txt
)

:: サーバー起動
echo サーバーを起動中...
python server/main.py

pause