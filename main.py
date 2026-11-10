import tkinter as tk
from tkinter import messagebox, ttk
import tkinter.simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
import db_module
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False
def load_data(search_keyword=""):
    for item in tree.get_children():
        tree.delete(item)
    rows = db_module.get_movies(search_keyword)
    for row in rows:
        rating_display = f"{row[5]}星" if row[5] else "-"
        tree.insert("", tk.END, iid=row[0], values=(row[1], row[2], row[3], row[4], rating_display))

def save_button_clicked():
    title = entry_title.get()
    genre = entry_genre.get()
    year = entry_year.get()
    status = var_status.get()
    rating = entry_rating.get()
    comment = entry_comment.get()
    if not title:
        messagebox.showwarning("警告", "片名不能为空！")
        return
    success = db_module.add_movie(title, genre, year, status, rating, comment)
    if success:
        messagebox.showinfo("成功", f"《{title}》添加成功！")
        entry_title.delete(0, tk.END)
        entry_genre.delete(0, tk.END)
        entry_year.delete(0, tk.END)
        entry_rating.delete(0, tk.END)
        entry_comment.delete(0, tk.END)
        load_data()
    else:
        messagebox.showerror("失败", "数据保存失败！")

def delete_selected():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("提示", "请先在表格里点击选中一行！")
        return
    movie_id = selected[0]
    if messagebox.askyesno("确认删除", "确定要删除这部影视记录吗？"):
        # 🌟 调用模块接口
        db_module.delete_movie(movie_id)
        load_data()

def show_details(event):
    selected = tree.selection()
    if not selected: return
    movie_id = selected[0]
    current_values = tree.item(movie_id, "values")
    title = current_values[0]
    new_rating = tk.simpledialog.askstring("修改评分", f"《{title}》\n请输入新评分（1-5）：")
    if new_rating is None: return
    new_comment = tk.simpledialog.askstring("修改短评", f"《{title}》\n请输入新短评：")
    if new_comment is None: return
    db_module.update_movie_review(movie_id, new_rating, new_comment)
    load_data()

def show_statistics():
    data = db_module.get_genre_stats()
    if not data:
        messagebox.showinfo("提示", "数据为空！")
        return
    labels = [row[0] for row in data]
    sizes = [row[1] for row in data]
    stat_window = tk.Toplevel(root)
    stat_window.title("观影类型占比分析")
    stat_window.geometry("500x450")
    fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, shadow=True)
    ax.set_title("各类型影视收藏占比")
    canvas = FigureCanvasTkAgg(fig, master=stat_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

db_module.init_db()
root = tk.Tk()
root.title("我的影视收藏夹")
root.geometry("750x650")
frame_search = tk.Frame(root)
frame_search.pack(pady=5)
tk.Label(frame_search, text="查找片名:").pack(side=tk.LEFT)
entry_search = tk.Entry(frame_search, width=20)
entry_search.pack(side=tk.LEFT, padx=5)
btn_search = tk.Button(frame_search, text="搜索", command=lambda: load_data(entry_search.get()))
btn_search.pack(side=tk.LEFT, padx=5)
btn_clear = tk.Button(frame_search, text="显示全部", command=lambda: [entry_search.delete(0, tk.END), load_data()])
btn_clear.pack(side=tk.LEFT, padx=5)
frame_input = tk.Frame(root)
frame_input.pack(pady=10)
tk.Label(frame_input, text="片名:").grid(row=0, column=0, padx=5, pady=2)
entry_title = tk.Entry(frame_input)
entry_title.grid(row=0, column=1, padx=5, pady=2)
tk.Label(frame_input, text="类型:").grid(row=0, column=2, padx=5, pady=2)
entry_genre = tk.Entry(frame_input)
entry_genre.grid(row=0, column=3, padx=5, pady=2)
tk.Label(frame_input, text="年份:").grid(row=1, column=0, padx=5, pady=2)
entry_year = tk.Entry(frame_input)
entry_year.grid(row=1, column=1, padx=5, pady=2)
tk.Label(frame_input, text="状态:").grid(row=1, column=2, padx=5, pady=2)
var_status = tk.StringVar(root)
var_status.set("想看")
status_menu = tk.OptionMenu(frame_input, var_status, "想看", "在看", "看过")
status_menu.grid(row=1, column=3, padx=5, pady=2)
tk.Label(frame_input, text="评分(1-5):").grid(row=2, column=0, padx=5, pady=2)
entry_rating = tk.Entry(frame_input, width=10)
entry_rating.grid(row=2, column=1, sticky="w", padx=5, pady=2)
tk.Label(frame_input, text="短评:").grid(row=2, column=2, padx=5, pady=2)
entry_comment = tk.Entry(frame_input, width=25)
entry_comment.grid(row=2, column=3, padx=5, pady=2)
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=5)
btn_save = tk.Button(frame_buttons, text="保存到片库", command=save_button_clicked, bg="lightgreen")
btn_save.grid(row=0, column=0, padx=10)
btn_delete = tk.Button(frame_buttons, text="删除选中记录", command=delete_selected, bg="lightcoral")
btn_delete.grid(row=0, column=1, padx=10)
btn_stats = tk.Button(frame_buttons, text="查看数据统计", command=show_statistics, bg="lightblue")
btn_stats.grid(row=0, column=2, padx=10)
columns = ("title", "genre", "year", "status", "rating")
tree = ttk.Treeview(root, columns=columns, show="headings", height=12)
tree.heading("title", text="片名")
tree.heading("genre", text="类型")
tree.heading("year", text="年份")
tree.heading("status", text="状态")
tree.heading("rating", text="评分")
tree.column("title", width=180)
tree.column("genre", width=100)
tree.column("year", width=80)
tree.column("status", width=80)
tree.column("rating", width=80)
tree.pack(pady=10, fill=tk.X, padx=20)
tree.bind("<Double-1>", show_details)
load_data()
root.mainloop()