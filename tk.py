import tkinter as tk
from tkinter import scrolledtext
import subprocess

# 启动另一个Python程序
def start_other_program():
    global other_program_process
    other_program_process = subprocess.Popen(['python', 'test_pro.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        line = other_program_process.stdout.readline().decode('utf-8').strip()
        if line == "ready":
            break

    # 显示tkinter窗口
    window.deiconify()

# 发送问题到另一个程序并获取回答
def get_response(question):
    other_program_process.stdin.write(question.encode('utf-8') + b'\n')
    other_program_process.stdin.flush()
    response = ""
    while True:
        line = other_program_process.stdout.readline().decode('utf-8').strip()
        print(line)
        if line == "111":
            break
        response += line + "\n"
    return response

# 处理用户输入的函数
def process_input():
    
    user_input = input_box.get("1.0", "end-1c")  # 获取用户输入的文本
    response = get_response(user_input)  # 获取回复
    str1=user_input
    str2=response
    #if len(str1)>len(str2): str2+=" "*(len(str1)-len(str2))
    #else: str1+=" "*(len(str2)-len(str1))
    str1+="\n"*str2.count("\n")
    str1+="\n\n"
    str2+="\n\n"
    conversation_log1.insert(tk.END, str1)  # 显示用户输入
    conversation_log2.insert(tk.END, str2)  # 显示机器人回复

    input_box.delete("1.0", tk.END)  # 清空输入框
    conversation_log1.see(tk.END)  # 滚动到最底部
    conversation_log2.see(tk.END)
    

    

# 创建主窗口
window = tk.Tk()
window.title("问答机器人")
window.geometry("2000x1000+0+0")

# 创建对话记录框
conversation_log1 = scrolledtext.ScrolledText(window)
conversation_log1.configure(font=("newspaper", 20), fg="black", bg="white")
conversation_log1.place(x=0,y=0, width=1000, height=900)

conversation_log2 = scrolledtext.ScrolledText(window)
conversation_log2.configure(font=("newspaper", 20), fg="black", bg="white")
conversation_log2.place(x=1000,y=0, width=1000, height=900)

# 创建输入框
input_box = tk.Text(window)
input_box.configure(font=("newspaper", 24), fg="black", bg="white")
input_box.place(x=0,y=900, width=700,height=90)

# 创建发送按钮
send_button = tk.Button(window, text="发送", command=process_input, font=("newspaper", 24))
send_button.place(x=700,y=900,width=100,height=90)
# 隐藏窗口直到另一个程序准备好
window.withdraw()

# 启动另一个程序
start_other_program()



# 运行主循环
window.mainloop()

