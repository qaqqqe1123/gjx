import customtkinter as ctk
from tkinter import ttk, messagebox
import webbrowser
import json
import requests
import pyperclip

class SoftwareDetailWindow(ctk.CTkToplevel):
    def __init__(self, parent, software_info):
        super().__init__(parent)
        
        # 设置窗口标题和大小
        self.title(f"软件详情 - {software_info['name']}")
        self.geometry("1000x600")
        self.configure(fg_color="white")  # 设置窗口背景为白色
        
        # 创建主框架
        main_frame = ctk.CTkFrame(self, fg_color="white")  # 白色背景
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # 软件名称
        name_label = ctk.CTkLabel(main_frame, text="软件名称：", 
                                 font=ctk.CTkFont(size=20, weight="bold"),
                                 text_color="#1a1a1a")  # 深色文字
        name_label.pack(anchor="w", pady=(0, 5))
        
        name_value = ctk.CTkLabel(main_frame, text=software_info['name'],
                                 font=ctk.CTkFont(size=18),
                                 text_color="#1a1a1a")  # 深色文字
        name_value.pack(anchor="w", pady=(0, 20))
        
        # 软件介绍
        intro_label = ctk.CTkLabel(main_frame, text="软件介绍：", 
                                  font=ctk.CTkFont(size=20, weight="bold"),
                                  text_color="#1a1a1a")  # 深色文字
        intro_label.pack(anchor="w", pady=(0, 5))
        
        intro_text = ctk.CTkTextbox(main_frame, height=250,
                                   font=ctk.CTkFont(size=16),
                                   fg_color="white",  # 白色背景
                                   text_color="#1a1a1a",  # 黑色文字
                                   border_color="#000000")  # 黑色边框
        intro_text.pack(fill="x", pady=(0, 20))
        intro_text.insert("1.0", software_info['introduce'])
        intro_text.configure(state="disabled")
        
        # 下载链接
        url_frame = ctk.CTkFrame(main_frame, fg_color="white")  # 白色背景
        url_frame.pack(fill="x", pady=(0, 15))
        
        url_label = ctk.CTkLabel(url_frame, text="下载链接：", 
                                font=ctk.CTkFont(size=20, weight="bold"),
                                text_color="#1a1a1a")  # 深色文字
        url_label.pack(side="left", padx=(0, 10))
        
        # 所有按钮放在同一个框架中
        buttons_frame = ctk.CTkFrame(url_frame, fg_color="white")  # 白色背景
        buttons_frame.pack(side="right", padx=5)
        
        # 关闭按钮
        close_btn = ctk.CTkButton(buttons_frame, text="关闭", 
                                 command=self.destroy,
                                 width=150, height=40,
                                 font=ctk.CTkFont(size=18),
                                 fg_color="#dc3545",  # 红色按钮
                                 hover_color="#c82333")  # 深红色悬停
        close_btn.pack(side="right", padx=5)
        
        # 下载按钮
        download_btn = ctk.CTkButton(buttons_frame, text="立即下载", 
                                    command=lambda: self._open_url(software_info['url']),
                                    width=150, height=40,
                                    font=ctk.CTkFont(size=18, weight="bold"),
                                    fg_color="#28a745",  # 绿色按钮
                                    hover_color="#218838")  # 深绿色悬停
        download_btn.pack(side="right", padx=5)
        
        # 复制链接按钮
        copy_btn = ctk.CTkButton(buttons_frame, text="复制链接", 
                                command=lambda: self._copy_url(software_info['url']),
                                width=150, height=40,
                                font=ctk.CTkFont(size=18),
                                fg_color="#007bff",  # 蓝色按钮
                                hover_color="#0056b3")  # 深蓝色悬停
        copy_btn.pack(side="right", padx=5)
        
        url_text = ctk.CTkTextbox(main_frame, height=80,
                                 font=ctk.CTkFont(size=16),
                                 fg_color="white",  # 白色背景
                                 text_color="#1a1a1a",  # 黑色文字
                                 border_color="#000000")  # 黑色边框
        url_text.pack(fill="x", pady=(0, 20))
        url_text.insert("1.0", software_info['url'])
        url_text.configure(state="disabled")
        
        # 设置窗口为模态
        self.transient(parent)
        self.grab_set()
        
    def _open_url(self, url):
        """打开下载链接"""
        try:
            webbrowser.open(url)
        except Exception as e:
            messagebox.showerror("错误", f"打开链接失败: {str(e)}")
            
    def _copy_url(self, url):
        """复制下载链接"""
        try:
            pyperclip.copy(url)
            messagebox.showinfo("成功", "链接已复制到剪贴板")
        except Exception as e:
            messagebox.showerror("错误", f"复制链接失败: {str(e)}")

class SoftwareListWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        # 设置窗口标题和大小
        self.title("软件下载中心")
        self.geometry("1200x700")
        self.configure(fg_color="white")  # 设置窗口背景为白色
        
        # 创建主框架
        main_frame = ctk.CTkFrame(self, fg_color="white")  # 白色背景
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 创建标题
        title = ctk.CTkLabel(main_frame, text="软件下载中心", 
                            font=ctk.CTkFont(size=24, weight="bold"),
                            text_color="#1a1a1a")  # 深色文字
        title.pack(pady=(0, 20))
        
        # 添加作者信息
        author = ctk.CTkLabel(main_frame, text="作者: Same0ld", 
                            font=ctk.CTkFont(size=14),
                            text_color=("#666666", "#999999"))
        author.pack(pady=(0, 15))
        
        # 创建搜索框架
        search_frame = ctk.CTkFrame(main_frame, fg_color="white")  # 白色背景
        search_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.search_var = ctk.StringVar()
        self.search_var.trace("w", self._on_search)
        search_entry = ctk.CTkEntry(search_frame, 
                                  placeholder_text="搜索软件...",
                                  textvariable=self.search_var,
                                  width=200,
                                  fg_color="#f8f9fa",  # 浅灰色背景
                                  text_color="#1a1a1a",  # 深色文字
                                  border_color="#e9ecef")  # 浅色边框
        search_entry.pack(side="left", padx=5)
        
        refresh_btn = ctk.CTkButton(search_frame, text="刷新列表", 
                                   command=self._refresh_list,
                                   width=100,
                                   fg_color="#007bff",  # 蓝色按钮
                                   hover_color="#0056b3")  # 深蓝色悬停
        refresh_btn.pack(side="left", padx=5)
        
        # 创建列表框架
        list_frame = ctk.CTkFrame(main_frame, fg_color="white")  # 白色背景
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 创建Treeview
        columns = ("name", "introduce", "url")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # 设置列标题
        self.tree.heading("name", text="软件名称")
        self.tree.heading("introduce", text="软件介绍")
        self.tree.heading("url", text="下载链接")
        
        # 设置列宽
        self.tree.column("name", width=200)  # 增加名称列宽
        self.tree.column("introduce", width=600)  # 增加介绍列宽
        self.tree.column("url", width=350)  # 增加链接列宽
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # 放置Treeview和滚动条
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 绑定双击事件和右键菜单
        self.tree.bind("<Double-1>", self._on_double_click)
        self.tree.bind("<Button-3>", self._show_context_menu)
        
        # 创建右键菜单
        self.context_menu = ctk.CTkFrame(self, fg_color="white")
        self.copy_menu = None
        
        # 设置窗口为模态
        self.transient(parent)
        self.grab_set()
        
        # 加载数据
        self._refresh_list()
        
    def _refresh_list(self):
        """刷新软件列表"""
        try:
            # 获取API数据
            response = requests.get("https://api.yizero.top/SoftwareDownloads/API.php")
            data = response.json()
            
            # 清空现有项目
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # 添加新项目
            for key, item in data.items():
                if isinstance(item, dict):  # 跳过非字典项（如 Last_updated）
                    values = (
                        item["name"],
                        item["introduce"],
                        item["url"].replace("\\/", "/")  # 修正URL中的转义字符
                    )
                    self.tree.insert("", "end", values=values)
                    
        except Exception as e:
            messagebox.showerror("错误", f"获取数据失败: {str(e)}")
            
    def _on_search(self, *args):
        """搜索功能"""
        search_text = self.search_var.get().lower()
        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            if (search_text in values[0].lower() or 
                search_text in values[1].lower()):
                self.tree.reattach(item, "", "end")
            else:
                self.tree.detach(item)
                
    def _show_context_menu(self, event):
        """显示右键菜单"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            selected_item = self.tree.item(item)
            values = selected_item['values']
            
            # 创建菜单
            if self.copy_menu:
                self.copy_menu.destroy()
                
            self.copy_menu = ctk.CTkFrame(self, fg_color="white")
            
            # 复制名称按钮
            copy_name_btn = ctk.CTkButton(self.copy_menu, text="复制软件名称",
                                         command=lambda: self._copy_text(values[0]))
            copy_name_btn.pack(fill="x", padx=2, pady=2)
            
            # 复制介绍按钮
            copy_intro_btn = ctk.CTkButton(self.copy_menu, text="复制软件介绍",
                                          command=lambda: self._copy_text(values[1]))
            copy_intro_btn.pack(fill="x", padx=2, pady=2)
            
            # 复制链接按钮
            copy_url_btn = ctk.CTkButton(self.copy_menu, text="复制下载链接",
                                        command=lambda: self._copy_text(values[2]))
            copy_url_btn.pack(fill="x", padx=2, pady=2)
            
            # 显示菜单
            self.copy_menu.place(x=event.x_root - self.winfo_rootx(),
                               y=event.y_root - self.winfo_rooty())
            
    def _copy_text(self, text):
        """复制文本"""
        try:
            pyperclip.copy(text)
            messagebox.showinfo("成功", "内容已复制到剪贴板")
            if self.copy_menu:
                self.copy_menu.destroy()
        except Exception as e:
            messagebox.showerror("错误", f"复制失败: {str(e)}")
                
    def _on_double_click(self, event):
        """双击显示软件详情"""
        selected_items = self.tree.selection()
        if selected_items:
            item = self.tree.item(selected_items[0])
            values = item['values']
            software_info = {
                'name': values[0],
                'introduce': values[1],
                'url': values[2]
            }
            detail_window = SoftwareDetailWindow(self, software_info)

class AlipayVoiceWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        # 设置窗口标题和大小
        self.title("支付宝到账语音生成")
        self.geometry("600x400")
        self.configure(fg_color="white")
        
        # 创建主框架
        self.main_frame = ctk.CTkFrame(self, fg_color="white")
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # 金额输入框
        amount_label = ctk.CTkLabel(self.main_frame, text="到账金额：", 
                                   font=ctk.CTkFont(size=16, weight="bold"),
                                   text_color="#1a1a1a")
        amount_label.pack(anchor="w", pady=(0, 5))
        
        self.amount_entry = ctk.CTkEntry(self.main_frame, 
                                       placeholder_text="请输入金额（元）",
                                       width=200,
                                       height=35,
                                       font=ctk.CTkFont(size=14))
        self.amount_entry.pack(anchor="w", pady=(0, 20))
        
        # 按钮框架
        button_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        button_frame.pack(pady=20)
        
        # 生成按钮
        generate_btn = ctk.CTkButton(button_frame, text="生成语音", 
                                    command=self._generate_voice,
                                    width=120, height=40,
                                    font=ctk.CTkFont(size=16),
                                    fg_color="#007bff",
                                    hover_color="#0056b3")
        generate_btn.pack(side="left", padx=5)
        
        # 播放按钮
        self.play_btn = ctk.CTkButton(button_frame, text="播放语音", 
                                     command=self._play_voice,
                                     width=120, height=40,
                                     font=ctk.CTkFont(size=16),
                                     fg_color="#28a745",
                                     hover_color="#218838",
                                     state="disabled")
        self.play_btn.pack(side="left", padx=5)
        
        # 下载按钮
        self.download_btn = ctk.CTkButton(button_frame, text="下载语音", 
                                         command=self._download_voice,
                                         width=120, height=40,
                                         font=ctk.CTkFont(size=16),
                                         fg_color="#17a2b8",
                                         hover_color="#138496",
                                         state="disabled")
        self.download_btn.pack(side="left", padx=5)
        
        # 复制按钮（初始状态为禁用）
        self.copy_btn = ctk.CTkButton(self.main_frame, text="复制链接",
                                     command=lambda: self._copy_url(self.current_voice_url),
                                     width=120,
                                     fg_color="#6c757d",
                                     hover_color="#5a6268",
                                     state="disabled")
        self.copy_btn.pack(pady=10)
        
        # 结果显示框
        self.result_text = ctk.CTkTextbox(self.main_frame, height=150,
                                         font=ctk.CTkFont(size=14),
                                         fg_color="white",
                                         text_color="#1a1a1a",
                                         border_color="#000000")
        self.result_text.pack(fill="x", pady=(0, 20))
        
        # 存储当前语音URL
        self.current_voice_url = None
        
        # 设置窗口为模态
        self.transient(parent)
        self.grab_set()
        
    def _generate_voice(self):
        """生成语音"""
        try:
            amount = self.amount_entry.get().strip()
            if not amount:
                messagebox.showerror("错误", "请输入金额")
                return
                
            try:
                amount = float(amount)
            except ValueError:
                messagebox.showerror("错误", "请输入有效的金额数字")
                return
                
            # 调用API
            url = "https://free.wqwlkj.cn/wqwlapi/alipay_yy.php"
            response = requests.get(url, params={"money": amount})
            
            if response.status_code == 200:
                voice_url = response.url  # 直接使用完整的URL
                self.current_voice_url = voice_url  # 保存URL
                self.result_text.delete("1.0", "end")
                self.result_text.insert("1.0", f"语音链接：{voice_url}\n\n语音已生成，可以使用上方按钮进行播放、下载或复制链接。")
                
                # 启用所有按钮
                self.play_btn.configure(state="normal")
                self.download_btn.configure(state="normal")
                self.copy_btn.configure(state="normal")
            else:
                messagebox.showerror("错误", "生成语音失败")
                
        except Exception as e:
            messagebox.showerror("错误", f"生成语音失败: {str(e)}")
            
    def _play_voice(self):
        """播放语音"""
        if self.current_voice_url:
            try:
                webbrowser.open(self.current_voice_url)
            except Exception as e:
                messagebox.showerror("错误", f"播放失败: {str(e)}")
                
    def _download_voice(self):
        """下载语音"""
        if self.current_voice_url:
            try:
                webbrowser.open(self.current_voice_url)
                messagebox.showinfo("提示", "已打开下载链接，请在浏览器中选择保存位置")
            except Exception as e:
                messagebox.showerror("错误", f"下载失败: {str(e)}")
            
    def _copy_url(self, url):
        """复制URL"""
        try:
            pyperclip.copy(url)
            messagebox.showinfo("成功", "链接已复制到剪贴板")
        except Exception as e:
            messagebox.showerror("错误", f"复制失败: {str(e)}")

class CPURankingWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        # 设置窗口标题和大小
        self.title("桌面CPU性能天梯图")
        self.geometry("1200x800")
        self.configure(fg_color="white")
        
        # 创建主框架
        self.main_frame = ctk.CTkFrame(self, fg_color="white")
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # 标题
        title = ctk.CTkLabel(self.main_frame, text="桌面CPU性能天梯图", 
                            font=ctk.CTkFont(size=24, weight="bold"),
                            text_color="#1a1a1a")
        title.pack(pady=(0, 20))
        
        # 创建表格框架
        table_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 创建Treeview
        columns = ("rank", "name", "score", "cores", "frequency", "release_date", "architecture", "tdp")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # 设置列标题
        self.tree.heading("rank", text="排名")
        self.tree.heading("name", text="处理器名称")
        self.tree.heading("score", text="跑分")
        self.tree.heading("cores", text="核心数")
        self.tree.heading("frequency", text="频率")
        self.tree.heading("release_date", text="发布日期")
        self.tree.heading("architecture", text="架构")
        self.tree.heading("tdp", text="功耗")
        
        # 设置列宽
        self.tree.column("rank", width=60)
        self.tree.column("name", width=300)
        self.tree.column("score", width=100)
        self.tree.column("cores", width=100)
        self.tree.column("frequency", width=100)
        self.tree.column("release_date", width=100)
        self.tree.column("architecture", width=100)
        self.tree.column("tdp", width=100)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # 放置Treeview和滚动条
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 创建按钮框架
        button_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        button_frame.pack(pady=20)
        
        # 刷新按钮
        refresh_btn = ctk.CTkButton(button_frame, text="刷新数据", 
                                   command=self._refresh_data,
                                   width=120, height=40,
                                   font=ctk.CTkFont(size=16),
                                   fg_color="#007bff",
                                   hover_color="#0056b3")
        refresh_btn.pack(side="left", padx=5)
        
        # 复制按钮
        copy_btn = ctk.CTkButton(button_frame, text="复制数据", 
                                command=self._copy_data,
                                width=120, height=40,
                                font=ctk.CTkFont(size=16),
                                fg_color="#28a745",
                                hover_color="#218838")
        copy_btn.pack(side="left", padx=5)
        
        # 设置窗口为模态
        self.transient(parent)
        self.grab_set()
        
        # 加载数据
        self._refresh_data()
        
    def _refresh_data(self):
        """刷新CPU排行榜数据"""
        try:
            # 清空现有数据
            for item in self.tree.get_children():
                self.tree.delete(item)

            # CPU数据
            cpu_data = [
                # 2023年高端CPU
                {
                    "name": "Intel Core i9-13900KS",
                    "score": "62000",
                    "cores": "24",
                    "threads": "32",
                    "frequency": "6.0",
                    "release_date": "2023-Q1",
                    "architecture": "Raptor Lake",
                    "tdp": "150"
                },
                {
                    "name": "AMD Ryzen 9 7950X3D",
                    "score": "60000",
                    "cores": "16",
                    "threads": "32",
                    "frequency": "5.7",
                    "release_date": "2023-Q1",
                    "architecture": "Zen 4",
                    "tdp": "120"
                },
                {
                    "name": "Intel Core i9-13900K",
                    "score": "59000",
                    "cores": "24",
                    "threads": "32",
                    "frequency": "5.8",
                    "release_date": "2023-Q1",
                    "architecture": "Raptor Lake",
                    "tdp": "125"
                },
                {
                    "name": "AMD Ryzen 9 7950X",
                    "score": "58000",
                    "cores": "16",
                    "threads": "32",
                    "frequency": "5.7",
                    "release_date": "2023-Q1",
                    "architecture": "Zen 4",
                    "tdp": "170"
                },
                {
                    "name": "Intel Core i9-13900",
                    "score": "57000",
                    "cores": "24",
                    "threads": "32",
                    "frequency": "5.6",
                    "release_date": "2023-Q1",
                    "architecture": "Raptor Lake",
                    "tdp": "65"
                },
                {
                    "name": "AMD Ryzen 9 7900X3D",
                    "score": "56000",
                    "cores": "12",
                    "threads": "24",
                    "frequency": "5.6",
                    "release_date": "2023-Q1",
                    "architecture": "Zen 4",
                    "tdp": "120"
                },
                # 2023年中端CPU
                {
                    "name": "Intel Core i7-13700K",
                    "score": "55000",
                    "cores": "16",
                    "threads": "24",
                    "frequency": "5.4",
                    "release_date": "2023-Q1",
                    "architecture": "Raptor Lake",
                    "tdp": "125"
                },
                {
                    "name": "AMD Ryzen 7 7800X3D",
                    "score": "54000",
                    "cores": "8",
                    "threads": "16",
                    "frequency": "5.0",
                    "release_date": "2023-Q2",
                    "architecture": "Zen 4",
                    "tdp": "120"
                },
                {
                    "name": "Intel Core i7-13700",
                    "score": "53000",
                    "cores": "16",
                    "threads": "24",
                    "frequency": "5.2",
                    "release_date": "2023-Q1",
                    "architecture": "Raptor Lake",
                    "tdp": "65"
                },
                {
                    "name": "AMD Ryzen 7 7700X",
                    "score": "52500",
                    "cores": "8",
                    "threads": "16",
                    "frequency": "5.4",
                    "release_date": "2023-Q1",
                    "architecture": "Zen 4",
                    "tdp": "105"
                },
                {
                    "name": "Intel Core i5-13600K",
                    "score": "52000",
                    "cores": "14",
                    "threads": "20",
                    "frequency": "5.1",
                    "release_date": "2023-Q1",
                    "architecture": "Raptor Lake",
                    "tdp": "125"
                },
                {
                    "name": "AMD Ryzen 5 7600X",
                    "score": "50000",
                    "cores": "6",
                    "threads": "12",
                    "frequency": "5.3",
                    "release_date": "2023-Q1",
                    "architecture": "Zen 4",
                    "tdp": "105"
                },
                # 2023年入门级CPU
                {
                    "name": "Intel Core i5-13500",
                    "score": "48000",
                    "cores": "14",
                    "threads": "20",
                    "frequency": "4.8",
                    "release_date": "2023-Q1",
                    "architecture": "Raptor Lake",
                    "tdp": "65"
                },
                {
                    "name": "AMD Ryzen 5 7600",
                    "score": "47000",
                    "cores": "6",
                    "threads": "12",
                    "frequency": "5.1",
                    "release_date": "2023-Q1",
                    "architecture": "Zen 4",
                    "tdp": "65"
                },
                {
                    "name": "Intel Core i5-13400",
                    "score": "46000",
                    "cores": "10",
                    "threads": "16",
                    "frequency": "4.6",
                    "release_date": "2023-Q1",
                    "architecture": "Raptor Lake",
                    "tdp": "65"
                },
                {
                    "name": "AMD Ryzen 5 7500F",
                    "score": "45000",
                    "cores": "6",
                    "threads": "12",
                    "frequency": "5.0",
                    "release_date": "2023-Q2",
                    "architecture": "Zen 4",
                    "tdp": "65"
                },
                # 2022年高端CPU
                {
                    "name": "Intel Core i9-12900KS",
                    "score": "44000",
                    "cores": "16",
                    "threads": "24",
                    "frequency": "5.5",
                    "release_date": "2022-Q2",
                    "architecture": "Alder Lake",
                    "tdp": "150"
                },
                {
                    "name": "AMD Ryzen 9 5950X",
                    "score": "43000",
                    "cores": "16",
                    "threads": "32",
                    "frequency": "4.9",
                    "release_date": "2022-Q1",
                    "architecture": "Zen 3",
                    "tdp": "105"
                },
                {
                    "name": "Intel Core i9-12900K",
                    "score": "42000",
                    "cores": "16",
                    "threads": "24",
                    "frequency": "5.2",
                    "release_date": "2022-Q1",
                    "architecture": "Alder Lake",
                    "tdp": "125"
                },
                # 2022年中端CPU
                {
                    "name": "AMD Ryzen 7 5800X3D",
                    "score": "41000",
                    "cores": "8",
                    "threads": "16",
                    "frequency": "4.5",
                    "release_date": "2022-Q2",
                    "architecture": "Zen 3",
                    "tdp": "105"
                },
                {
                    "name": "Intel Core i7-12700K",
                    "score": "40000",
                    "cores": "12",
                    "threads": "20",
                    "frequency": "5.0",
                    "release_date": "2022-Q1",
                    "architecture": "Alder Lake",
                    "tdp": "125"
                },
                {
                    "name": "AMD Ryzen 7 5800X",
                    "score": "39000",
                    "cores": "8",
                    "threads": "16",
                    "frequency": "4.7",
                    "release_date": "2022-Q1",
                    "architecture": "Zen 3",
                    "tdp": "105"
                },
                # 2022年入门级CPU
                {
                    "name": "Intel Core i5-12600K",
                    "score": "38000",
                    "cores": "10",
                    "threads": "16",
                    "frequency": "4.9",
                    "release_date": "2022-Q1",
                    "architecture": "Alder Lake",
                    "tdp": "125"
                },
                {
                    "name": "AMD Ryzen 5 5600X",
                    "score": "37000",
                    "cores": "6",
                    "threads": "12",
                    "frequency": "4.6",
                    "release_date": "2022-Q1",
                    "architecture": "Zen 3",
                    "tdp": "65"
                },
                {
                    "name": "Intel Core i5-12400",
                    "score": "36000",
                    "cores": "6",
                    "threads": "12",
                    "frequency": "4.4",
                    "release_date": "2022-Q1",
                    "architecture": "Alder Lake",
                    "tdp": "65"
                }
            ]

            # 添加数据到表格
            rank = 1
            for cpu in cpu_data:
                try:
                    # 处理频率显示
                    frequency = f"{cpu['frequency']}GHz" if cpu['frequency'] else "未知"
                    # 处理功耗显示
                    tdp = f"{cpu['tdp']}W" if cpu['tdp'] else "未知"
                    # 处理核心数显示
                    cores = f"{cpu['cores']}核{cpu['threads']}线程" if cpu['cores'] and cpu['threads'] else cpu['cores'] if cpu['cores'] else "未知"
                    
                    values = (
                        rank,
                        cpu["name"],
                        cpu["score"],
                        cores,
                        frequency,
                        cpu["release_date"],
                        cpu["architecture"],
                        tdp
                    )
                    self.tree.insert("", "end", values=values)
                    rank += 1
                except KeyError as e:
                    continue
                    
        except Exception as e:
            messagebox.showerror("错误", f"获取数据失败: {str(e)}")
            
    def _copy_data(self):
        """复制所选CPU数据"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("提示", "请先选择要复制的CPU")
            return
            
        try:
            item = self.tree.item(selected_items[0])
            values = item['values']
            text = f"""
CPU名称：{values[1]}
跑分：{values[2]}
核心/线程：{values[3]}
频率：{values[4]}
发布日期：{values[5]}
架构：{values[6]}
功耗：{values[7]}
"""
            pyperclip.copy(text.strip())
            messagebox.showinfo("成功", "CPU信息已复制到剪贴板")
        except Exception as e:
            messagebox.showerror("错误", f"复制失败: {str(e)}")

class WeatherQueryWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("天气查询")
        self.geometry("600x500")
        
        # 创建输入框架
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(padx=20, pady=20, fill="x")
        
        # 省份输入
        province_label = ctk.CTkLabel(input_frame, text="省份:")
        province_label.pack(side="left", padx=5)
        self.province_entry = ctk.CTkEntry(input_frame, placeholder_text="例如：四川省")
        self.province_entry.pack(side="left", padx=5)
        self.province_entry.insert(0, "四川省")
        
        # 城市输入
        city_label = ctk.CTkLabel(input_frame, text="城市:")
        city_label.pack(side="left", padx=5)
        self.city_entry = ctk.CTkEntry(input_frame, placeholder_text="例如：绵阳市")
        self.city_entry.pack(side="left", padx=5)
        self.city_entry.insert(0, "绵阳市")
        
        # 查询按钮
        query_btn = ctk.CTkButton(input_frame, text="查询天气", command=self._query_weather)
        query_btn.pack(side="left", padx=20)
        
        # 创建结果显示文本框
        self.result_text = ctk.CTkTextbox(self, width=560, height=400)
        self.result_text.pack(padx=20, pady=10)
        
    def _query_weather(self):
        """查询天气信息"""
        province = self.province_entry.get().strip()
        city = self.city_entry.get().strip()
        
        if not province or not city:
            messagebox.showerror("错误", "请输入省份和城市")
            return
            
        try:
            # 发送API请求
            params = {
                "id": "10003038",
                "key": "f48fe9fb56249e3b0f8b2d489d6154eb",
                "province": province,
                "city": city,
                "county": ""
            }
            response = requests.get("https://cn.apihz.cn/api/tianqi/tengxun.php", params=params)
            data = response.json()
            
            if data.get("code") == 200:
                # 定义字段映射
                field_mapping = {
                    "province": "省份",
                    "getcity": "城市",
                    "county": "区县",
                    "time": "日期",
                    "day_weather": "白天天气",
                    "day_wind_direction": "白天风向",
                    "day_wind_power": "白天风力",
                    "night_weather": "夜间天气",
                    "night_wind_direction": "夜间风向",
                    "night_wind_power": "夜间风力",
                    "max_degree": "最高温度",
                    "min_degree": "最低温度"
                }

                weather_info = "天气信息：\n\n"
                
                # 添加基本地区信息
                for key in ["province", "getcity", "county"]:
                    if key in data:
                        weather_info += f"{field_mapping.get(key, key)}: {data[key]}\n"
                
                # 添加天气数据信息
                weather_data = data.get("data", [])
                if isinstance(weather_data, list) and weather_data:
                    weather_info += "\n未来8天天气预报:\n"
                    # 遍历所有天气数据
                    for day_weather in weather_data:
                        if isinstance(day_weather, dict):
                            weather_info += "\n----------------------------------------\n"
                            # 按照特定顺序显示信息
                            important_keys = [
                                "time",
                                "day_weather", "day_wind_direction", "day_wind_power",
                                "night_weather", "night_wind_direction", "night_wind_power",
                                "max_degree", "min_degree"
                            ]
                            
                            for key in important_keys:
                                if key in day_weather:
                                    value = day_weather[key]
                                    # 如果是温度相关字段，确保显示单位
                                    if "degree" in key and not str(value).endswith("℃"):
                                        value = f"{value}℃"
                                    weather_info += f"{field_mapping.get(key, key)}: {value}\n"
                
                # 清空并显示结果
                self.result_text.delete("1.0", "end")
                self.result_text.insert("1.0", weather_info)
            else:
                messagebox.showerror("错误", f"获取天气信息失败：{data.get('msg', '未知错误')}")
                
        except Exception as e:
            messagebox.showerror("错误", f"查询天气失败：{str(e)}")

class NetworkToolboxPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="white")
        
        self.controller = None
        self._create_widgets()
        
    def _create_widgets(self):
        """创建页面组件"""
        # 页面标题
        title = ctk.CTkLabel(self, text="网络工具箱", 
                            font=ctk.CTkFont(size=24, weight="bold"),
                            text_color=("#1a5fb4", "#0b3b8c"))
        title.pack(padx=20, pady=(20, 5))
        
        # 添加作者信息
        author = ctk.CTkLabel(self, text="作者: Same0ld", 
                            font=ctk.CTkFont(size=14),
                            text_color=("#666666", "#999999"))
        author.pack(pady=(0, 15))
        
        # 创建主框架
        main_frame = ctk.CTkFrame(self, fg_color="white")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 创建工具栏
        toolbar = ctk.CTkFrame(main_frame, fg_color="white")
        toolbar.pack(padx=10, pady=10, fill="x")
        
        # 添加安装包直链按钮
        direct_link_btn = ctk.CTkButton(toolbar, text="安装包直链", 
                                       command=self._show_direct_links,
                                       fg_color=("#1a73e8", "#0b57d0"), 
                                       hover_color=("#1557b0", "#0842a0"),
                                       width=120,
                                       height=35)
        direct_link_btn.pack(side="left", padx=5)
        
        # 添加支付宝语音按钮
        alipay_voice_btn = ctk.CTkButton(toolbar, text="支付宝到账语音", 
                                        command=self._show_alipay_voice,
                                        fg_color=("#1a73e8", "#0b57d0"), 
                                        hover_color=("#1557b0", "#0842a0"),
                                        width=120,
                                        height=35)
        alipay_voice_btn.pack(side="left", padx=5)
        
        # 添加CPU排行榜按钮
        cpu_ranking_btn = ctk.CTkButton(toolbar, text="桌面CPU排行", 
                                       command=self._show_cpu_ranking,
                                       fg_color=("#1a73e8", "#0b57d0"), 
                                       hover_color=("#1557b0", "#0842a0"),
                                       width=120,
                                       height=35)
        cpu_ranking_btn.pack(side="left", padx=5)

        # 添加笔记本CPU排行榜按钮
        laptop_cpu_btn = ctk.CTkButton(toolbar, text="笔记本CPU排行", 
                                      command=self._show_laptop_cpu_ranking,
                                      fg_color=("#1a73e8", "#0b57d0"), 
                                      hover_color=("#1557b0", "#0842a0"),
                                      width=120,
                                      height=35)
        laptop_cpu_btn.pack(side="left", padx=5)

        # 添加显卡排行榜按钮
        gpu_ranking_btn = ctk.CTkButton(toolbar, text="显卡排行榜", 
                                       command=self._show_gpu_ranking,
                                       fg_color=("#1a73e8", "#0b57d0"), 
                                       hover_color=("#1557b0", "#0842a0"),
                                       width=120,
                                       height=35)
        gpu_ranking_btn.pack(side="left", padx=5)

        # 添加天气查询按钮
        weather_btn = ctk.CTkButton(toolbar, text="天气查询", 
                                   command=self._show_weather_query,
                                   fg_color=("#1a73e8", "#0b57d0"), 
                                   hover_color=("#1557b0", "#0842a0"),
                                   width=120,
                                   height=35)
        weather_btn.pack(side="left", padx=5)
        
    def set_controller(self, controller):
        """设置控制器"""
        self.controller = controller
        
    def _show_direct_links(self):
        """显示安装包直链窗口"""
        list_window = SoftwareListWindow(self)
        
    def _show_alipay_voice(self):
        """显示支付宝语音生成窗口"""
        voice_window = AlipayVoiceWindow(self)
        
    def _show_cpu_ranking(self):
        """显示CPU排行榜窗口"""
        ranking_window = CPURankingWindow(self)

    def _show_laptop_cpu_ranking(self):
        """显示笔记本CPU排行榜窗口"""
        ranking_window = LaptopCPURankingWindow(self)

    def _show_gpu_ranking(self):
        """显示显卡排行榜窗口"""
        ranking_window = GPURankingWindow(self)

    def _show_weather_query(self):
        """显示天气查询窗口"""
        weather_window = WeatherQueryWindow(self)
            
    def show_error(self, message):
        """显示错误消息"""
        messagebox.showerror("错误", message)
        
    def show_success(self, message):
        """显示成功消息"""
        messagebox.showinfo("成功", message)

class GPURankingWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        # 设置窗口标题和大小
        self.title("桌面显卡性能排行")
        self.geometry("1200x800")
        self.configure(fg_color="white")
        
        # 创建主框架
        self.main_frame = ctk.CTkFrame(self, fg_color="white")
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # 标题
        title = ctk.CTkLabel(self.main_frame, text="桌面显卡性能排行", 
                            font=ctk.CTkFont(size=24, weight="bold"),
                            text_color="#1a1a1a")
        title.pack(pady=(0, 20))
        
        # 创建表格框架
        table_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 创建Treeview
        columns = ("rank", "name", "cores", "frequency", "memory", "architecture", "tdp")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # 设置列标题
        self.tree.heading("rank", text="排名")
        self.tree.heading("name", text="显卡名称")
        self.tree.heading("cores", text="CUDA核心")
        self.tree.heading("frequency", text="频率")
        self.tree.heading("memory", text="显存")
        self.tree.heading("architecture", text="架构")
        self.tree.heading("tdp", text="功耗")
        
        # 设置列宽
        self.tree.column("rank", width=60)
        self.tree.column("name", width=300)
        self.tree.column("cores", width=150)
        self.tree.column("frequency", width=100)
        self.tree.column("memory", width=100)
        self.tree.column("architecture", width=150)
        self.tree.column("tdp", width=100)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # 放置Treeview和滚动条
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 创建按钮框架
        button_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        button_frame.pack(pady=20)
        
        # 刷新按钮
        refresh_btn = ctk.CTkButton(button_frame, text="刷新数据", 
                                   command=self._refresh_data,
                                   width=120, height=40,
                                   font=ctk.CTkFont(size=16),
                                   fg_color="#007bff",
                                   hover_color="#0056b3")
        refresh_btn.pack(side="left", padx=5)
        
        # 复制按钮
        copy_btn = ctk.CTkButton(button_frame, text="复制数据", 
                                command=self._copy_data,
                                width=120, height=40,
                                font=ctk.CTkFont(size=16),
                                fg_color="#28a745",
                                hover_color="#218838")
        copy_btn.pack(side="left", padx=5)
        
        # 设置窗口为模态
        self.transient(parent)
        self.grab_set()
        
        # 加载数据
        self._refresh_data()
        
    def _refresh_data(self):
        """刷新显卡排行榜数据"""
        try:
            # 清空现有数据
            for item in self.tree.get_children():
                self.tree.delete(item)

            # 显卡数据
            gpu_data = [
                # NVIDIA RTX 40系列旗舰
                {
                    "name": "NVIDIA GeForce RTX 4090",
                    "cores": "16384",
                    "frequency": "2.52",
                    "memory": "24GB GDDR6X",
                    "architecture": "Ada Lovelace",
                    "tdp": "450"
                },
                {
                    "name": "NVIDIA GeForce RTX 4080",
                    "cores": "9728",
                    "frequency": "2.51",
                    "memory": "16GB GDDR6X",
                    "architecture": "Ada Lovelace",
                    "tdp": "320"
                },
                # AMD RX 7000系列旗舰
                {
                    "name": "AMD Radeon RX 7900 XTX",
                    "cores": "6144",
                    "frequency": "2.50",
                    "memory": "24GB GDDR6",
                    "architecture": "RDNA 3",
                    "tdp": "355"
                },
                {
                    "name": "AMD Radeon RX 7900 XT",
                    "cores": "5376",
                    "frequency": "2.40",
                    "memory": "20GB GDDR6",
                    "architecture": "RDNA 3",
                    "tdp": "315"
                },
                # NVIDIA RTX 40系列高端
                {
                    "name": "NVIDIA GeForce RTX 4070 Ti",
                    "cores": "7680",
                    "frequency": "2.61",
                    "memory": "12GB GDDR6X",
                    "architecture": "Ada Lovelace",
                    "tdp": "285"
                },
                {
                    "name": "NVIDIA GeForce RTX 4070",
                    "cores": "5888",
                    "frequency": "2.48",
                    "memory": "12GB GDDR6X",
                    "architecture": "Ada Lovelace",
                    "tdp": "200"
                },
                # AMD RX 7000系列高端
                {
                    "name": "AMD Radeon RX 7800 XT",
                    "cores": "3840",
                    "frequency": "2.43",
                    "memory": "16GB GDDR6",
                    "architecture": "RDNA 3",
                    "tdp": "263"
                },
                {
                    "name": "AMD Radeon RX 7700 XT",
                    "cores": "3456",
                    "frequency": "2.54",
                    "memory": "12GB GDDR6",
                    "architecture": "RDNA 3",
                    "tdp": "245"
                },
                # NVIDIA RTX 40系列中端
                {
                    "name": "NVIDIA GeForce RTX 4060 Ti 16GB",
                    "cores": "4352",
                    "frequency": "2.54",
                    "memory": "16GB GDDR6",
                    "architecture": "Ada Lovelace",
                    "tdp": "160"
                },
                {
                    "name": "NVIDIA GeForce RTX 4060 Ti",
                    "cores": "4352",
                    "frequency": "2.54",
                    "memory": "8GB GDDR6",
                    "architecture": "Ada Lovelace",
                    "tdp": "160"
                },
                {
                    "name": "NVIDIA GeForce RTX 4060",
                    "cores": "3072",
                    "frequency": "2.46",
                    "memory": "8GB GDDR6",
                    "architecture": "Ada Lovelace",
                    "tdp": "115"
                },
                # AMD RX 7000系列中端
                {
                    "name": "AMD Radeon RX 7600",
                    "cores": "2048",
                    "frequency": "2.66",
                    "memory": "8GB GDDR6",
                    "architecture": "RDNA 3",
                    "tdp": "165"
                },
                # NVIDIA RTX 30系列旗舰
                {
                    "name": "NVIDIA GeForce RTX 3090 Ti",
                    "cores": "10752",
                    "frequency": "1.86",
                    "memory": "24GB GDDR6X",
                    "architecture": "Ampere",
                    "tdp": "450"
                },
                {
                    "name": "NVIDIA GeForce RTX 3090",
                    "cores": "10496",
                    "frequency": "1.70",
                    "memory": "24GB GDDR6X",
                    "architecture": "Ampere",
                    "tdp": "350"
                },
                # NVIDIA RTX 30系列高端
                {
                    "name": "NVIDIA GeForce RTX 3080 Ti",
                    "cores": "10240",
                    "frequency": "1.67",
                    "memory": "12GB GDDR6X",
                    "architecture": "Ampere",
                    "tdp": "350"
                },
                {
                    "name": "NVIDIA GeForce RTX 3080 12GB",
                    "cores": "8960",
                    "frequency": "1.71",
                    "memory": "12GB GDDR6X",
                    "architecture": "Ampere",
                    "tdp": "350"
                },
                {
                    "name": "NVIDIA GeForce RTX 3080",
                    "cores": "8704",
                    "frequency": "1.71",
                    "memory": "10GB GDDR6X",
                    "architecture": "Ampere",
                    "tdp": "320"
                },
                # NVIDIA RTX 30系列中端
                {
                    "name": "NVIDIA GeForce RTX 3070 Ti",
                    "cores": "6144",
                    "frequency": "1.77",
                    "memory": "8GB GDDR6X",
                    "architecture": "Ampere",
                    "tdp": "290"
                },
                {
                    "name": "NVIDIA GeForce RTX 3070",
                    "cores": "5888",
                    "frequency": "1.73",
                    "memory": "8GB GDDR6",
                    "architecture": "Ampere",
                    "tdp": "220"
                },
                {
                    "name": "NVIDIA GeForce RTX 3060 Ti",
                    "cores": "4864",
                    "frequency": "1.67",
                    "memory": "8GB GDDR6",
                    "architecture": "Ampere",
                    "tdp": "200"
                },
                {
                    "name": "NVIDIA GeForce RTX 3060",
                    "cores": "3584",
                    "frequency": "1.78",
                    "memory": "12GB GDDR6",
                    "architecture": "Ampere",
                    "tdp": "170"
                },
                # AMD RX 6000系列旗舰
                {
                    "name": "AMD Radeon RX 6950 XT",
                    "cores": "5120",
                    "frequency": "2.31",
                    "memory": "16GB GDDR6",
                    "architecture": "RDNA 2",
                    "tdp": "335"
                },
                {
                    "name": "AMD Radeon RX 6900 XT",
                    "cores": "5120",
                    "frequency": "2.25",
                    "memory": "16GB GDDR6",
                    "architecture": "RDNA 2",
                    "tdp": "300"
                },
                # AMD RX 6000系列高端
                {
                    "name": "AMD Radeon RX 6800 XT",
                    "cores": "4608",
                    "frequency": "2.25",
                    "memory": "16GB GDDR6",
                    "architecture": "RDNA 2",
                    "tdp": "300"
                },
                {
                    "name": "AMD Radeon RX 6800",
                    "cores": "3840",
                    "frequency": "2.10",
                    "memory": "16GB GDDR6",
                    "architecture": "RDNA 2",
                    "tdp": "250"
                },
                # AMD RX 6000系列中端
                {
                    "name": "AMD Radeon RX 6750 XT",
                    "cores": "2560",
                    "frequency": "2.60",
                    "memory": "12GB GDDR6",
                    "architecture": "RDNA 2",
                    "tdp": "250"
                },
                {
                    "name": "AMD Radeon RX 6700 XT",
                    "cores": "2560",
                    "frequency": "2.58",
                    "memory": "12GB GDDR6",
                    "architecture": "RDNA 2",
                    "tdp": "230"
                },
                {
                    "name": "AMD Radeon RX 6700",
                    "cores": "2304",
                    "frequency": "2.45",
                    "memory": "10GB GDDR6",
                    "architecture": "RDNA 2",
                    "tdp": "175"
                },
                {
                    "name": "AMD Radeon RX 6650 XT",
                    "cores": "2048",
                    "frequency": "2.64",
                    "memory": "8GB GDDR6",
                    "architecture": "RDNA 2",
                    "tdp": "180"
                },
                {
                    "name": "AMD Radeon RX 6600 XT",
                    "cores": "2048",
                    "frequency": "2.59",
                    "memory": "8GB GDDR6",
                    "architecture": "RDNA 2",
                    "tdp": "160"
                },
                {
                    "name": "AMD Radeon RX 6600",
                    "cores": "1792",
                    "frequency": "2.49",
                    "memory": "8GB GDDR6",
                    "architecture": "RDNA 2",
                    "tdp": "132"
                }
            ]

            # 添加数据到表格
            rank = 1
            for gpu in gpu_data:
                try:
                    # 处理频率显示
                    frequency = f"{gpu['frequency']}GHz" if gpu['frequency'] else "未知"
                    # 处理功耗显示
                    tdp = f"{gpu['tdp']}W" if gpu['tdp'] else "未知"
                    # 处理核心数显示
                    cores = f"{gpu['cores']}核心" if gpu['cores'] else "未知"
                    
                    values = (
                        rank,
                        gpu["name"],
                        cores,
                        frequency,
                        gpu["memory"],
                        gpu["architecture"],
                        tdp
                    )
                    self.tree.insert("", "end", values=values)
                    rank += 1
                except KeyError as e:
                    continue
                    
        except Exception as e:
            messagebox.showerror("错误", f"获取数据失败: {str(e)}")
            
    def _copy_data(self):
        """复制所选显卡数据"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("提示", "请先选择要复制的显卡")
            return
            
        try:
            item = self.tree.item(selected_items[0])
            values = item['values']
            text = f"""
显卡名称：{values[1]}
CUDA核心：{values[2]}
频率：{values[3]}
显存：{values[4]}
架构：{values[5]}
功耗：{values[6]}
"""
            pyperclip.copy(text.strip())
            messagebox.showinfo("成功", "显卡信息已复制到剪贴板")
        except Exception as e:
            messagebox.showerror("错误", f"复制失败: {str(e)}")

class LaptopCPURankingWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        # 设置窗口标题和大小
        self.title("笔记本CPU性能排行")
        self.geometry("1200x800")
        self.configure(fg_color="white")
        
        # 创建主框架
        self.main_frame = ctk.CTkFrame(self, fg_color="white")
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # 标题
        title = ctk.CTkLabel(self.main_frame, text="笔记本CPU性能排行", 
                            font=ctk.CTkFont(size=24, weight="bold"),
                            text_color="#1a1a1a")
        title.pack(pady=(0, 20))
        
        # 创建表格框架
        table_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 创建Treeview
        columns = ("rank", "name", "cores", "frequency", "architecture", "tdp")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # 设置列标题
        self.tree.heading("rank", text="排名")
        self.tree.heading("name", text="处理器名称")
        self.tree.heading("cores", text="核心数")
        self.tree.heading("frequency", text="频率")
        self.tree.heading("architecture", text="架构")
        self.tree.heading("tdp", text="功耗")
        
        # 设置列宽
        self.tree.column("rank", width=60)
        self.tree.column("name", width=300)
        self.tree.column("cores", width=150)
        self.tree.column("frequency", width=100)
        self.tree.column("architecture", width=150)
        self.tree.column("tdp", width=100)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # 放置Treeview和滚动条
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 创建按钮框架
        button_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        button_frame.pack(pady=20)
        
        # 刷新按钮
        refresh_btn = ctk.CTkButton(button_frame, text="刷新数据", 
                                   command=self._refresh_data,
                                   width=120, height=40,
                                   font=ctk.CTkFont(size=16),
                                   fg_color="#007bff",
                                   hover_color="#0056b3")
        refresh_btn.pack(side="left", padx=5)
        
        # 复制按钮
        copy_btn = ctk.CTkButton(button_frame, text="复制数据", 
                                command=self._copy_data,
                                width=120, height=40,
                                font=ctk.CTkFont(size=16),
                                fg_color="#28a745",
                                hover_color="#218838")
        copy_btn.pack(side="left", padx=5)
        
        # 设置窗口为模态
        self.transient(parent)
        self.grab_set()
        
        # 加载数据
        self._refresh_data()
        
    def _refresh_data(self):
        """刷新笔记本CPU排行榜数据"""
        try:
            # 清空现有数据
            for item in self.tree.get_children():
                self.tree.delete(item)

            # CPU数据
            cpu_data = [
                # Intel 13代旗舰
                {
                    "name": "Intel Core i9-13980HX",
                    "cores": "24核32线程",
                    "frequency": "5.6",
                    "architecture": "Raptor Lake",
                    "tdp": "55"
                },
                {
                    "name": "Intel Core i9-13950HX",
                    "cores": "24核32线程",
                    "frequency": "5.5",
                    "architecture": "Raptor Lake",
                    "tdp": "55"
                },
                {
                    "name": "Intel Core i9-13900HX",
                    "cores": "24核32线程",
                    "frequency": "5.4",
                    "architecture": "Raptor Lake",
                    "tdp": "55"
                },
                # Intel 13代高性能
                {
                    "name": "Intel Core i9-13900H",
                    "cores": "14核20线程",
                    "frequency": "5.4",
                    "architecture": "Raptor Lake",
                    "tdp": "45"
                },
                {
                    "name": "Intel Core i7-13850HX",
                    "cores": "20核28线程",
                    "frequency": "5.3",
                    "architecture": "Raptor Lake",
                    "tdp": "55"
                },
                {
                    "name": "Intel Core i7-13800H",
                    "cores": "14核20线程",
                    "frequency": "5.2",
                    "architecture": "Raptor Lake",
                    "tdp": "45"
                },
                {
                    "name": "Intel Core i7-13700H",
                    "cores": "14核20线程",
                    "frequency": "5.0",
                    "architecture": "Raptor Lake",
                    "tdp": "45"
                },
                # Intel 13代中端
                {
                    "name": "Intel Core i5-13600HX",
                    "cores": "14核20线程",
                    "frequency": "4.8",
                    "architecture": "Raptor Lake",
                    "tdp": "55"
                },
                {
                    "name": "Intel Core i5-13500H",
                    "cores": "12核16线程",
                    "frequency": "4.7",
                    "architecture": "Raptor Lake",
                    "tdp": "45"
                },
                {
                    "name": "Intel Core i5-13420H",
                    "cores": "8核12线程",
                    "frequency": "4.6",
                    "architecture": "Raptor Lake",
                    "tdp": "45"
                },
                # AMD 7000系列旗舰
                {
                    "name": "AMD Ryzen 9 7945HX",
                    "cores": "16核32线程",
                    "frequency": "5.4",
                    "architecture": "Zen 4",
                    "tdp": "55"
                },
                {
                    "name": "AMD Ryzen 9 7940HS",
                    "cores": "8核16线程",
                    "frequency": "5.2",
                    "architecture": "Zen 4",
                    "tdp": "45"
                },
                {
                    "name": "AMD Ryzen 9 7845HX",
                    "cores": "12核24线程",
                    "frequency": "5.2",
                    "architecture": "Zen 4",
                    "tdp": "55"
                },
                # AMD 7000系列高性能
                {
                    "name": "AMD Ryzen 7 7840HS",
                    "cores": "8核16线程",
                    "frequency": "5.1",
                    "architecture": "Zen 4",
                    "tdp": "45"
                },
                {
                    "name": "AMD Ryzen 7 7745HX",
                    "cores": "8核16线程",
                    "frequency": "5.1",
                    "architecture": "Zen 4",
                    "tdp": "55"
                },
                {
                    "name": "AMD Ryzen 7 7735HS",
                    "cores": "8核16线程",
                    "frequency": "4.7",
                    "architecture": "Zen 3+",
                    "tdp": "45"
                },
                # AMD 7000系列中端
                {
                    "name": "AMD Ryzen 5 7640HS",
                    "cores": "6核12线程",
                    "frequency": "5.0",
                    "architecture": "Zen 4",
                    "tdp": "45"
                },
                {
                    "name": "AMD Ryzen 5 7535HS",
                    "cores": "6核12线程",
                    "frequency": "4.55",
                    "architecture": "Zen 3+",
                    "tdp": "45"
                },
                # Intel 12代旗舰
                {
                    "name": "Intel Core i9-12950HX",
                    "cores": "16核24线程",
                    "frequency": "5.0",
                    "architecture": "Alder Lake",
                    "tdp": "55"
                },
                {
                    "name": "Intel Core i9-12900HX",
                    "cores": "16核24线程",
                    "frequency": "5.0",
                    "architecture": "Alder Lake",
                    "tdp": "55"
                },
                {
                    "name": "Intel Core i9-12900H",
                    "cores": "14核20线程",
                    "frequency": "5.0",
                    "architecture": "Alder Lake",
                    "tdp": "45"
                },
                # Intel 12代高性能
                {
                    "name": "Intel Core i7-12850HX",
                    "cores": "16核24线程",
                    "frequency": "4.8",
                    "architecture": "Alder Lake",
                    "tdp": "55"
                },
                {
                    "name": "Intel Core i7-12800H",
                    "cores": "14核20线程",
                    "frequency": "4.8",
                    "architecture": "Alder Lake",
                    "tdp": "45"
                },
                {
                    "name": "Intel Core i7-12700H",
                    "cores": "14核20线程",
                    "frequency": "4.7",
                    "architecture": "Alder Lake",
                    "tdp": "45"
                },
                # Intel 12代中端
                {
                    "name": "Intel Core i5-12600H",
                    "cores": "12核16线程",
                    "frequency": "4.5",
                    "architecture": "Alder Lake",
                    "tdp": "45"
                },
                {
                    "name": "Intel Core i5-12500H",
                    "cores": "12核16线程",
                    "frequency": "4.5",
                    "architecture": "Alder Lake",
                    "tdp": "45"
                },
                {
                    "name": "Intel Core i5-12450H",
                    "cores": "8核12线程",
                    "frequency": "4.4",
                    "architecture": "Alder Lake",
                    "tdp": "45"
                }
            ]

            # 添加数据到表格
            rank = 1
            for cpu in cpu_data:
                try:
                    # 处理频率显示
                    frequency = f"{cpu['frequency']}GHz" if cpu['frequency'] else "未知"
                    # 处理功耗显示
                    tdp = f"{cpu['tdp']}W" if cpu['tdp'] else "未知"
                    
                    values = (
                        rank,
                        cpu["name"],
                        cpu["cores"],
                        frequency,
                        cpu["architecture"],
                        tdp
                    )
                    self.tree.insert("", "end", values=values)
                    rank += 1
                except KeyError as e:
                    continue
                    
        except Exception as e:
            messagebox.showerror("错误", f"获取数据失败: {str(e)}")
            
    def _copy_data(self):
        """复制所选CPU数据"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("提示", "请先选择要复制的CPU")
            return
            
        try:
            item = self.tree.item(selected_items[0])
            values = item['values']
            text = f"""
处理器名称：{values[1]}
核心/线程：{values[2]}
频率：{values[3]}
架构：{values[4]}
功耗：{values[5]}
"""
            pyperclip.copy(text.strip())
            messagebox.showinfo("成功", "CPU信息已复制到剪贴板")
        except Exception as e:
            messagebox.showerror("错误", f"复制失败: {str(e)}") 