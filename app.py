#OECU-StudentCardLeader V1.0
import nfc
import os
from datetime import datetime
#from playsound import playsound


print("""\033[31m

   ____  ______________  __     _____ __            __           __  ______               ____                   __         
  / __ \/ ____/ ____/ / / /    / ___// /___  ______/ /__  ____  / /_/ ____/___ __________/ / /   ___  ____ _____/ /__  _____
 / / / / __/ / /   / / / /_____\__ \/ __/ / / / __  / _ \/ __ \/ __/ /   / __ `/ ___/ __  / /   / _ \/ __ `/ __  / _ \/ ___/
/ /_/ / /___/ /___/ /_/ /_____/__/ / /_/ /_/ / /_/ /  __/ / / / /_/ /___/ /_/ / /  / /_/ / /___/  __/ /_/ / /_/ /  __/ /    
\____/_____/\____/\____/     /____/\__/\__,_/\__,_/\___/_/ /_/\__/\____/\__,_/_/   \__,_/_____/\___/\__,_/\__,_/\___/_/     
                                                                                                                            

\033[0m""")
print("/////////////////////////////////////////////////////////////////////////")


def remove_log():
    os.remove("log.txt")
    with open("log.txt", 'w') as file:
        file.write('')

def on_connect(tag: nfc.tag.Tag) -> bool:
    
    print("connected")
    

    try:
        data = tag.dump()
        #print("\n".join(data))  
        remove_log()
        with open("log.txt", "a") as f:
            f.write("\n".join(data) + "\n") 
        extract_value_from_line(5, 2, 10)  
    except nfc.tag.tt3.Type3TagCommandError as e:
        print(f"Error: {e}") 
    except Exception as e:
        print(f"Unexpected error: {e}") 

    return True  # Trueを返しておくとタグが存在しなくなるまで待機され、離すとon_releaseが発火する

def on_release(tag: nfc.tag.Tag) -> None:
    print("released")
    print("/////////////////////////////////////////////////////////////////////////")
    
def extract_value_from_line(line_number, start_col, end_col):
    with open("log.txt", 'r') as file:
        lines = file.readlines()

        target_line = lines[line_number - 1]  
        columns = target_line.split()  # スペースで分割


        extracted_values = columns[start_col:end_col + 1]
        decoded_values = [chr(int(value, 16)) for value in extracted_values[1:]]  # 最初の要素（インデックス）を除外
        students_id = ''.join(decoded_values)  # デコードした文字を結合
        print(f"student_id: {students_id}")
        with open("students_id.txt", "a") as f:
                f.write(f"{datetime.now()} / {students_id}\n")
        #playsound("sounds/iD.wav")
        
        students_id_str = str(students_id)
        grade =students_id_str[2] + students_id_str[3]
        if int(grade) == 24:
            print("1年生")
        elif int(grade) == 23:
            print("2年生")
        elif int(grade) == 22:
            print("3年生")
        elif int(grade) == 21:
            print("4年生")
        else:
            print("留年で草")



if os.path.exists("log.txt"):
    remove_log()
else:
    with open("log.txt", 'w') as file:
        file.write('')
        


with nfc.ContactlessFrontend("usb") as clf:
    while True:
        clf.connect(rdwr={"on-connect": on_connect, "on-release": on_release})
