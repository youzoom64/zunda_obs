import os
import shutil
from pathlib import Path

# 日本語→英語の変換辞書
translations = {
    # フォルダ名
    '_服装1': 'outfit1',
    '_服装2': 'outfit2',
    '!右腕': 'right_arm',
    '!左腕': 'left_arm',
    '!顔色': 'face_color',
    '!口': 'mouth',
    '!枝豆': 'edamame',
    '!眉': 'eyebrow',
    '!目': 'eye',
    '_目セット': 'eye_set',
    '!黒目': 'pupil',
    '記号など': 'symbols',
    
    # ファイル名
    '_(非表示)': 'hidden',
    '_マイク': 'mic',
    '_基本': 'basic',
    '_苦しむ': 'suffer',
    '_口元': 'mouth_area',
    '_腰': 'waist',
    '_指差し': 'point',
    '_手を挙げる': 'raise_hand',
    '_ひそひそ': 'whisper',
    '_考える': 'think',
    '_胸元': 'chest',
    '_いつもの服': 'usual_clothes',
    '_制服': 'uniform',
    '_スク水': 'swimsuit',
    '_バスタオル': 'towel',
    '_ぱんつ': 'pants',
    '_素体': 'body',
    '_ほっぺ': 'cheek',
    '_ほっぺ2': 'cheek2',
    '_ほっぺ赤め': 'cheek_red',
    '_青ざめ': 'pale',
    'かげり': 'shadow',
    '_△': 'triangle',
    '_お': 'o',
    '_おほお': 'ohoo',
    '_はへえ': 'hahee',
    '_ほあ': 'hoa',
    '_ほあー': 'hoaa',
    '_ほー': 'hoo',
    '_むー': 'muu',
    '_むふ': 'muhu',
    '_ゆ': 'yu',
    '_んー': 'nn',
    '_んあー': 'nnaa',
    '_んへー': 'nnhee',
    '_パーカー(裏地とセットで使用)': 'hoodie_lining',
    '_枝豆萎え': 'edamame_sad',
    '_枝豆通常': 'edamame_normal',
    '_困り眉1': 'troubled_eyebrow1',
    '_困り眉2': 'troubled_eyebrow2',
    '_上がり眉': 'raised_eyebrow',
    '_怒り眉': 'angry_eyebrow',
    '_普通眉': 'normal_eyebrow',
    '_カメラ目線': 'camera_gaze',
    '_カメラ目線2': 'camera_gaze2',
    '_カメラ目線3': 'camera_gaze3',
    '_普通目': 'normal_eye',
    '_普通目2': 'normal_eye2',
    '_普通目3': 'normal_eye3',
    '_目逸らし': 'look_away',
    '_目逸らし2': 'look_away2',
    '_目逸らし3': 'look_away3',
    '_ジト白目': 'sharp_white_eye',
    '_見開き白目': 'wide_white_eye',
    '_普通白目': 'normal_white_eye',
    '____': 'closed_eye',
    '_〇〇': 'circle_eye',
    '_UU': 'sleepy_eye',
    '_ぐるぐる': 'dizzy_eye',
    '_ジト目': 'sharp_eye',
    '_なごみ目': 'peaceful_eye',
    '_にっこり': 'smile_eye',
    '_にっこり2': 'smile_eye2',
    '_細め目': 'narrow_eye',
    '_細め目ハート': 'narrow_heart_eye',
    '_上向き': 'upward_eye',
    '_上向き2': 'upward_eye2',
    '_上向き3': 'upward_eye3',
    'アヒルちゃん': 'duck',
    '汗1': 'sweat1',
    '汗2': 'sweat2',
    '汗3': 'sweat3',
    '涙': 'tear',
    'パーカー裏地': 'hoodie_lining',
    '尻尾的なアレ': 'tail_thing'
}

def clean_filename(filename):
    """ファイル名から pos_数字 部分を削除し、英語に変換"""
    # 拡張子を分離
    name, ext = os.path.splitext(filename)
    
    # pos_数字部分を削除
    if '_pos_' in name:
        name = name.split('_pos_')[0]
    
    # 日本語を英語に変換
    for jp, en in translations.items():
        name = name.replace(jp, en)
    
    return name + ext

def rename_directory_recursive(source_dir, target_dir):
    """ディレクトリ構造を再帰的にリネーム"""
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        
        # 新しい名前を生成
        new_name = clean_filename(item) if os.path.isfile(source_path) else item
        
        # フォルダ名も変換
        for jp, en in translations.items():
            new_name = new_name.replace(jp, en)
        
        target_path = os.path.join(target_dir, new_name)
        
        if os.path.isfile(source_path):
            # ファイルをコピー
            shutil.copy2(source_path, target_path)
            print(f"ファイル: {item} → {new_name}")
        elif os.path.isdir(source_path):
            # ディレクトリを再帰的に処理
            print(f"フォルダ: {item} → {new_name}")
            rename_directory_recursive(source_path, target_path)

if __name__ == "__main__":
    source = "assets/zundamon"
    target = "assets/zundamon_en"
    
    print("ファイル・フォルダ名を英語に変換中...")
    rename_directory_recursive(source, target)
    print("変換完了！")
    print(f"変換後のファイルは {target} フォルダに保存されました")