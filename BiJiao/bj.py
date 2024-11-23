import os
import filecmp
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox

# 递归比较两个目录，返回A有而B没有的文件、B有而A没有的文件和相同的文件
def compare_directories(dir1, dir2):
    def recursive_compare(dcmp):
        only_in_a = dcmp.left_only
        only_in_b = dcmp.right_only
        same_files = []

        for name in dcmp.common_files:
            file1 = os.path.join(dcmp.left, name)
            file2 = os.path.join(dcmp.right, name)
            if filecmp.cmp(file1, file2, shallow=False):
                same_files.append(name)

        for sub_dcmp in dcmp.subdirs.values():
            sub_only_in_a, sub_only_in_b, sub_same_files = recursive_compare(sub_dcmp)
            only_in_a += sub_only_in_a
            only_in_b += sub_only_in_b
            same_files += sub_same_files

        return only_in_a, only_in_b, same_files

    dcmp = filecmp.dircmp(dir1, dir2)
    return recursive_compare(dcmp)

# 主函数，显示比较结果
def show_differences(dir1, dir2):
    if not dir1 or not dir2:
        messagebox.showwarning("警告", "请选定两个文件夹。")
        return

    only_in_a, only_in_b, same_files = compare_directories(dir1, dir2)

    # 清空文本框
    result_text_a.delete(1.0, tk.END)
    result_text_b.delete(1.0, tk.END)
    result_text_common.delete(1.0, tk.END)

    # 显示A有B没有的文件/文件夹
    if only_in_a:
        result_text_a.insert(tk.END, f"仅在 {dir1} 中存在的文件/文件夹：\n")
        for item in only_in_a:
            result_text_a.insert(tk.END, item + "\n")
    else:
        result_text_a.insert(tk.END, f"{dir1} 中没有独有的文件/文件夹\n")

    # 显示B有A没有的文件/文件夹
    if only_in_b:
        result_text_b.insert(tk.END, f"仅在 {dir2} 中存在的文件/文件夹：\n")
        for item in only_in_b:
            result_text_b.insert(tk.END, item + "\n")
    else:
        result_text_b.insert(tk.END, f"{dir2} 中没有独有的文件/文件夹\n")

    # 显示相同的文件
    if same_files:
        result_text_common.insert(tk.END, "内容相同的文件：\n")
        for file_name in same_files:
            result_text_common.insert(tk.END, f"在 {dir1} 和 {dir2} 中相同的文件：{file_name}\n")
    else:
        result_text_common.insert(tk.END, "没有内容相同的文件。\n")

# 选择第一个文件夹
def select_directory1():
    dir1 = filedialog.askdirectory()
    if dir1:
        dir1_entry.delete(0, tk.END)
        dir1_entry.insert(0, dir1)

# 选择第二个文件夹
def select_directory2():
    dir2 = filedialog.askdirectory()
    if dir2:
        dir2_entry.delete(0, tk.END)
        dir2_entry.insert(0, dir2)

# 创建主窗口
window = tk.Tk()
window.title("文件夹比较工具")

# 文件夹1选择
dir1_label = tk.Label(window, text="文件夹 1:")
dir1_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
dir1_entry = tk.Entry(window, width=50)
dir1_entry.grid(row=0, column=1, padx=10, pady=5, sticky='ew')
dir1_button = tk.Button(window, text="浏览", command=select_directory1)
dir1_button.grid(row=0, column=2, padx=10, pady=5, sticky='e')

# 文件夹2选择
dir2_label = tk.Label(window, text="文件夹 2:")
dir2_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')
dir2_entry = tk.Entry(window, width=50)
dir2_entry.grid(row=1, column=1, padx=10, pady=5, sticky='ew')
dir2_button = tk.Button(window, text="浏览", command=select_directory2)
dir2_button.grid(row=1, column=2, padx=10, pady=5, sticky='e')

# 比较按钮
compare_button = tk.Button(window, text="比较", command=lambda: show_differences(dir1_entry.get(), dir2_entry.get()))
compare_button.grid(row=2, column=0, columnspan=3, pady=10, sticky='ew')

# 标签和滚动文本框1：显示A有B没有的文件
label_a = tk.Label(window, text="仅在文件夹 1 中存在的文件/文件夹：")
label_a.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky='w')
result_text_a = scrolledtext.ScrolledText(window, width=50, height=10)
result_text_a.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

# 标签和滚动文本框2：显示B有A没有的文件
label_b = tk.Label(window, text="仅在文件夹 2 中存在的文件/文件夹：")
label_b.grid(row=5, column=0, columnspan=3, padx=10, pady=5, sticky='w')
result_text_b = scrolledtext.ScrolledText(window, width=50, height=10)
result_text_b.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

# 标签和滚动文本框3：显示相同的文件
label_common = tk.Label(window, text="内容相同的文件：")
label_common.grid(row=7, column=0, columnspan=3, padx=10, pady=5, sticky='w')
result_text_common = scrolledtext.ScrolledText(window, width=50, height=10)
result_text_common.grid(row=8, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

# 调整列和行的权重，使得窗口大小改变时，元素能够自动调整
window.columnconfigure(1, weight=1)
window.rowconfigure(4, weight=1)
window.rowconfigure(6, weight=1)
window.rowconfigure(8, weight=1)

# 运行主循环
window.mainloop()
