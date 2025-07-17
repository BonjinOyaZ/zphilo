import yaml
import subprocess
import os
import sys

# ファイルパスの定義
ZPHILO_YAML_PATH = "zphilo.yaml"
INIT_SCRIPT_PATH = "init_zphilo_yaml.py"
GEMINI_MD_PATH = "GEMINI.md"
README_PATH = "README.md" # README.mdのパスを追加

def load_zphilo_yaml():
    """zphilo.yaml を読み込み、存在しない場合は初期化スクリプトを実行する"""
    if not os.path.exists(ZPHILO_YAML_PATH):
        print(f"'{ZPHILO_YAML_PATH}' が見つかりません。初期化スクリプトを実行します。")
        run_init_script()
    try:
        with open(ZPHILO_YAML_PATH, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"エラー: '{ZPHILO_YAML_PATH}' の読み込み中に問題が発生しました: {e}")
        exit(1)
    except FileNotFoundError:
        print(f"エラー: '{ZPHILO_YAML_PATH}' が見つかりません。")
        exit(1)

def run_init_script():
    """init_zphilo_yaml.py を実行して zphilo.yaml を初期化する"""
    print("Z-PHILOのデータを初期化します...")
    try:
        result = subprocess.run(["python", INIT_SCRIPT_PATH], check=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        print(result.stdout.strip())
        print("Z-PHILOの初期化が完了しました。")
    except subprocess.CalledProcessError as e:
        print(f"エラー: 初期化スクリプトの実行中に問題が発生しました: {e}")
        exit(1)
    except FileNotFoundError:
        print(f"エラー: '{INIT_SCRIPT_PATH}' が見つかりません。")
        exit(1)

def get_next_step(data):
    """zphilo.yaml の内容から次の入力ステップを判断する"""
    # (この関数の内容は変更なし)
    user_info = data.get('user', {})
    philosophy_info = data.get('philosophy', {})
    mission_info = data.get('mission', {})
    vision_info = data.get('vision', {})
    values_list = data.get('values', [])

    if not user_info.get('name'):
        return "ユーザー名"
    if not philosophy_info.get('title') or not philosophy_info.get('description'):
        return "哲学のタイトルと説明"
    if not mission_info.get('statement'):
        return "使命"
    if not vision_info.get('year_5') or not vision_info.get('year_10') or not vision_info.get('year_20'):
        return "ビジョン（5年後、10年後、20年後）"

    for i, val in enumerate(values_list):
        if not val.get('action'):
            return f"行動指針（{val.get('situation', '不明な状況')}）"
    
    return "全ての項目が入力済みです。素晴らしい！"

def read_file_content(file_path):
    """指定されたファイルを読み込んで内容を返す"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"警告: '{file_path}' が見つかりませんでした。")
        return ""

def main():
    """メイン処理"""
    print("Z-PHILO CLIへようこそ！")

    reset_choice = input("Z-PHILOのデータを最初からやり直しますか？ (y/N): ").lower()
    if reset_choice == 'y':
        run_init_script()
    
    zphilo_data = load_zphilo_yaml()
    next_step = get_next_step(zphilo_data)
    print(f"\n現在の進捗状況: {next_step}")

    # --- 初期プロンプトの構築 ---
    readme_content = read_file_content(README_PATH)
    zphilo_content = read_file_content(ZPHILO_YAML_PATH)

    initial_prompt = f"""
わが友よ、対話を始めよう。
まずは、君のプロジェクトの概要と、現在の哲学の状態をわしに共有しておくれ。
これを元に、我々の議論を深めていこうじゃないか。

--- README.md ---
{readme_content}

--- zphilo.yaml ---
{zphilo_content}

"""

    if "全ての項目が入力済みです" in next_step:
        initial_prompt += "\n君の哲学は既に確立されておるな。いつでもわしと対話できるぞ。\n君の哲学について、さらに深掘りしてみようか。どんなことでも話してみるがよい。"
    else:
        initial_prompt += f"\n次は「{next_step}」について、わしと壁打ちするがよい。\n君の「{next_step}」について、わしと共に言葉を紡いでいこう。さあ、語り始めてくれ。"

    print("\n渋沢栄一翁との対話を開始します。")
    print("対話を終了するには、新しい行で `exit` または `quit` と入力してください。")
    print("-" * 20)

    # --- Gemini CLI の起動と対話 ---
    try:
        # gemini コマンドをsubprocessで起動
        # shell=TrueはWindowsで `gemini` のようなコマンドを見つけるのに役立つ
        process = subprocess.Popen(
            ['gemini'], 
            stdin=subprocess.PIPE, 
            stdout=sys.stdout, # CLIの出力を直接ターミナルに表示
            stderr=sys.stderr, # CLIのエラーを直接ターミナルに表示
            text=True, 
            encoding='utf-8',
            shell=True
        )

        # 初期プロンプトを送信
        process.stdin.write(initial_prompt + '\n')
        process.stdin.flush()

        # ユーザーの入力をCLIに中継
        for line in sys.stdin:
            if line.strip().lower() in ['exit', 'quit']:
                print("対話を終了します。また会おうぞ、友よ。")
                break
            process.stdin.write(line)
            process.stdin.flush()
        
        process.stdin.close()
        process.wait()

    except FileNotFoundError:
        print("\nエラー: 'gemini' コマンドが見つかりません。")
        print("Gemini CLIがインストールされ、パスが通っていることを確認してください。")
        exit(1)
    except Exception as e:
        print(f"\n予期せぬエラーが発生しました: {e}")
        exit(1)

if __name__ == "__main__":
    main()