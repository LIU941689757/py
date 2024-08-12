import tkinter as tk  # 导入tkinter模块，用于创建图形界面
from tkinter import messagebox  # 导入消息框，用于显示提示和错误信息
import time  # 导入time模块，用于处理时间相关功能
import os  # 导入os模块，用于操作系统级别的功能
import platform  # 导入platform模块，用于检测操作系统
import threading  # 导入threading模块，用于多线程处理
import json  # 导入json模块，用于处理JSON数据
from datetime import datetime, timedelta  # 从datetime模块导入datetime和timedelta，用于时间操作

class ShutdownApp:
    def __init__(self, root):
        self.root = root  # 保存主窗口引用
        self.root.title("定时关机程序")  # 设置窗口标题
        
        # 设置窗口大小为500x500
        self.root.geometry("500x500")
        
        # 将窗口居中
        self.center_window()
        
        # 读取保存的目标关机时间
        self.shutdown_time = self.load_shutdown_time()
        
        # 创建标签用于提示输入定时关机的分钟数
        self.label = tk.Label(root, text="请输入定时关机的分钟数:")
        self.label.pack(pady=10)  # 将标签添加到窗口，并设置上下边距为10
        
        # 创建文本框用于输入分钟数
        self.entry = tk.Entry(root)
        self.entry.pack(pady=5)  # 将文本框添加到窗口，并设置上下边距为5
        
        # 创建按钮框架，用于放置按钮
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)  # 将框架添加到窗口，并设置上下边距为10
        
        # 创建“设置关机”按钮，并设置颜色及点击效果
        self.schedule_button = tk.Button(button_frame, text="设置关机", command=self.schedule_shutdown,
                                        bg="green", fg="white", activebackground="darkgreen", activeforeground="white")
        self.schedule_button.pack(side=tk.LEFT, padx=5)  # 将按钮放置在框架的左侧，并设置左右边距为5
        
        # 创建“取消关机”按钮，并设置颜色及点击效果
        self.cancel_button = tk.Button(button_frame, text="取消关机", command=self.cancel_shutdown,
                                       bg="red", fg="white", activebackground="darkred", activeforeground="white")
        self.cancel_button.pack(side=tk.LEFT, padx=5)  # 将按钮放置在框架的左侧，并设置左右边距为5
        
        # 创建标签用于显示剩余时间
        self.time_label = tk.Label(root, text=self.format_time())
        self.time_label.pack(pady=10)  # 将标签添加到窗口，并设置上下边距为10
        
        # 如果目标关机时间存在且尚未到达，则启动时间更新线程
        if self.shutdown_time:
            threading.Thread(target=self.update_time, daemon=True).start()
    
    def center_window(self):
        # 获取屏幕宽度和高度
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # 获取窗口宽度和高度
        window_width = 300
        window_height = 200
        
        # 计算窗口位置，使其居中
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # 设置窗口位置
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def schedule_shutdown(self):
        try:
            # 获取用户输入的分钟数，并计算目标关机时间
            minutes = int(self.entry.get())
            self.shutdown_time = datetime.now() + timedelta(minutes=minutes)
            self.save_shutdown_time(self.shutdown_time)  # 保存目标关机时间
            
            # 显示关机计划的消息
            self.show_message(f"系统将在 {minutes} 分钟后关机。")
            
            # 启动定时器线程来处理关机任务
            threading.Thread(target=self.shutdown_timer, args=(self.shutdown_time,)).start()
            
            # 启动更新剩余时间的线程
            threading.Thread(target=self.update_time, daemon=True).start()
            
        except ValueError:
            # 如果输入无效，则显示错误消息
            self.show_message("请输入有效的分钟数。", error=True)
    
    def shutdown_timer(self, shutdown_time):
        # 定义定时关机的线程函数
        while datetime.now() < shutdown_time:
            time.sleep(1)  # 每秒检查一次时间
        # 根据操作系统执行关机命令
        if platform.system() == "Windows":
            os.system("shutdown /s /t 1")
        elif platform.system() in ["Linux", "Darwin"]:
            os.system("shutdown -h now")
        else:
            self.show_message("不支持的操作系统", error=True)

    def update_time(self):
        # 定义更新剩余时间的线程函数
        while self.shutdown_time and datetime.now() < self.shutdown_time:
            self.time_label.config(text=self.format_time())  # 更新标签显示剩余时间
            time.sleep(1)  # 每秒更新一次
        # 如果剩余时间为0，则更新文本
        self.time_label.config(text="剩余时间: 0 分钟 0 秒")

    def format_time(self):
        # 格式化剩余时间的显示
        if self.shutdown_time:
            remaining_time = self.shutdown_time - datetime.now()
            if remaining_time > timedelta(0):
                minutes, seconds = divmod(remaining_time.seconds, 60)
                return f"剩余时间: {minutes} 分钟 {seconds} 秒"
        return "剩余时间: 0 分钟 0 秒"

    def save_shutdown_time(self, shutdown_time):
        # 将目标关机时间保存到文件中
        with open("shutdown_timer.json", "w") as f:
            json.dump({"shutdown_time": shutdown_time.isoformat()}, f)

    def load_shutdown_time(self):
        # 从文件中加载目标关机时间
        if os.path.exists("shutdown_timer.json"):
            with open("shutdown_timer.json", "r") as f:
                data = json.load(f)
                return datetime.fromisoformat(data.get("shutdown_time")) if "shutdown_time" in data else None
        return None

    def cancel_shutdown(self):
        # 取消定时关机并删除保存的时间文件
        if os.path.exists("shutdown_timer.json"):
            os.remove("shutdown_timer.json")
            self.shutdown_time = None
            self.time_label.config(text="定时关机已取消")  # 更新标签文本
            self.show_message("定时关机已取消。")  # 显示取消关机的消息
        else:
            self.show_message("没有设置定时关机。", error=True)  # 显示错误消息

    def show_message(self, message, error=False):
        # 显示消息框
        if error:
            messagebox.showerror("提示", message)  # 显示错误消息框
        else:
            messagebox.showinfo("定时关机", message)  # 显示信息消息框

if __name__ == "__main__":
    root = tk.Tk()  # 创建主窗口
    app = ShutdownApp(root)  # 创建应用程序实例
    root.mainloop()  # 运行主事件循环
