import os
import sys
from pathlib import Path

def create_desktop_shortcut():
    project_root = Path(__file__).parent
    
    if sys.platform == "win32":
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        shortcut_path = os.path.join(desktop, "ずんだもんシステム.lnk")
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = str(project_root / "run.bat")
        shortcut.WorkingDirectory = str(project_root)
        shortcut.IconLocation = str(project_root / "icon.ico") if (project_root / "icon.ico").exists() else ""
        shortcut.save()
        
        print(f"デスクトップショートカットを作成しました: {shortcut_path}")
    else:
        print("Windowsでのみショートカット作成をサポートしています")

if __name__ == "__main__":
    try:
        create_desktop_shortcut()
    except ImportError:
        print("ショートカット作成には winshell が必要です")
        print("pip install winshell pywin32")