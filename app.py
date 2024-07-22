import nfc
import os
from datetime import datetime
from playsound import playsound

print("""
      
      
      
ooooo      ooo oooooooooooo   .oooooo.   
`888b.     `8' `888'     `8  d8P'  `Y8b  
 8 `88b.    8   888         888          
 8   `88b.  8   888oooo8    888          
 8     `88b.8   888    "    888          
 8       `888   888         `88b    ooo  
o8o        `8  o888o         `Y8bood8P'  
                                         
                                         
                                         

""")

def remove_log():
    os.remove("app/log.txt")
    with open("app/log.txt", 'w') as file:
        file.write('')

def on_connect(tag: nfc.tag.Tag) -> bool:
    print("connected")
    

    try:
        # 生データを読み込む
        data = tag.dump()
        #print("\n".join(data))  
        remove_log()# 修正: tag.dump() を data で表示
        with open("app/log.txt", "a") as f:
            f.write("\n".join(data) + "\n") 
            # 修正: データをログに書き込む際に改行を追加
        extract_value_from_line(5, 2, 10)  # 5行目の0列目から5列目を取得
    except nfc.tag.tt3.Type3TagCommandError as e:
        print(f"Error: {e}")  # タイムアウトエラーをキャッチして表示
    except Exception as e:
        print(f"Unexpected error: {e}") 
    # その他のエラーをキャッチして表示

    return True  # Trueを返しておくとタグが存在しなくなるまで待機され、離すとon_releaseが発火する

def on_release(tag: nfc.tag.Tag) -> None:
    print("released")
    
def extract_value_from_line(line_number, start_col, end_col):
    with open("app/log.txt", 'r') as file:
        lines = file.readlines()
        
        # 行数を確認

        
        target_line = lines[line_number - 1]  # 行番号は1から始まるため、-1する
        columns = target_line.split()  # スペースで分割
        
        # 指定された列範囲が有効か確認

        
        # 指定された列範囲の値を取得
        extracted_values = columns[start_col:end_col + 1]
        decoded_values = [chr(int(value, 16)) for value in extracted_values[1:]]  # 最初の要素（インデックス）を除外
        decoded_string = ''.join(decoded_values)  # デコードした文字を結合
        print(f"student_id: {decoded_string}")
        with open("app/students_id.txt", "a") as f:
                f.write(f"{datetime.now()} / {decoded_string}\n")
                playsound("app/sounds/ID.wav")


if os.path.exists("app/log.txt"):
    remove_log()
else:
    with open("app/log.txt", 'w') as file:
        # ファイルに書き込む内容
        file.write('')
        

with nfc.ContactlessFrontend("usb") as clf:
    while True:
        clf.connect(rdwr={"on-connect": on_connect, "on-release": on_release})