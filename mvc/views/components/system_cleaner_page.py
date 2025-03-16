import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk  # 添加ttk导入

class SystemCleanerPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        self.controller = None
        self.clean_option_buttons = {}
        
        # 定义颜色方案
        self.border_color = ("#1a73e8", "#0b57d0")  # 蓝色边框
        self.header_color = ("#1a5fb4", "#0b3b8c")  # 标题颜色
        self.button_color = ("#1a73e8", "#0b57d0")  # 按钮颜色
        self.button_hover_color = ("#1557b0", "#0842a0")  # 按钮悬停颜色
        
        self._create_widgets()
        
    def _create_widgets(self):
        """创建页面组件"""
        # 页面标题
        title = ctk.CTkLabel(self, text="系统清理", 
                            font=ctk.CTkFont(size=24, weight="bold"),
                            text_color=self.header_color)
        title.pack(padx=20, pady=20)
        
        # 创建选项卡
        self.tabview = ctk.CTkTabview(self, fg_color=("white", "#edf2fb"))
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 添加选项卡
        self.tabview.add("清理选项")
        self.tabview.add("清理结果")
        self.tabview.add("安全设置")
        self.tabview.set("清理选项")
        
        # 配置选项卡
        self._setup_cleaner_options(self.tabview.tab("清理选项"))
        self._setup_cleaner_results(self.tabview.tab("清理结果"))
        self._setup_safety_settings(self.tabview.tab("安全设置"))
        
        # 添加进度条和操作按钮
        self._setup_progress_and_actions()
        
    def _setup_cleaner_options(self, parent):
        """设置清理选项界面"""
        # 创建滚动框架
        options_canvas = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        options_canvas.pack(fill="both", expand=True, padx=5, pady=5)
        
        # 临时文件清理选项
        temp_frame = ctk.CTkFrame(options_canvas, border_width=1, border_color=self.border_color)
        temp_frame.pack(padx=10, pady=10, fill="x")
        
        temp_label = ctk.CTkLabel(temp_frame, text="临时文件清理", 
                                 font=ctk.CTkFont(size=16, weight="bold"),
                                 text_color=self.header_color)
        temp_label.pack(padx=10, pady=(10, 5), anchor="w")
        
        temp_buttons_frame = ctk.CTkFrame(temp_frame, fg_color="transparent")
        temp_buttons_frame.pack(padx=10, pady=5, fill="x")
        temp_buttons_frame.grid_columnconfigure(0, weight=1)
        temp_buttons_frame.grid_columnconfigure(1, weight=1)
        
        # Windows临时文件按钮
        self.clean_option_buttons["windows_temp"] = self._create_clean_option_button(
            temp_buttons_frame, "Windows临时文件", "windows_temp", 0, 0
        )
        
        # 用户临时文件按钮
        self.clean_option_buttons["user_temp"] = self._create_clean_option_button(
            temp_buttons_frame, "用户临时文件", "user_temp", 0, 1
        )
        
        # 预读取文件按钮
        self.clean_option_buttons["prefetch"] = self._create_clean_option_button(
            temp_buttons_frame, "预读取文件", "prefetch", 1, 0
        )
        
        # 最近文档列表按钮
        self.clean_option_buttons["recent_docs"] = self._create_clean_option_button(
            temp_buttons_frame, "最近文档列表", "recent_docs", 1, 1
        )
        
        # 回收站清理选项
        recycle_frame = ctk.CTkFrame(options_canvas, border_width=1, border_color=self.border_color)
        recycle_frame.pack(padx=10, pady=10, fill="x")
        
        recycle_label = ctk.CTkLabel(recycle_frame, text="回收站清理", 
                                    font=ctk.CTkFont(size=16, weight="bold"),
                                    text_color=self.header_color)
        recycle_label.pack(padx=10, pady=(10, 5), anchor="w")
        
        recycle_buttons_frame = ctk.CTkFrame(recycle_frame, fg_color="transparent")
        recycle_buttons_frame.pack(padx=10, pady=5, fill="x")
        
        # 回收站按钮
        self.clean_option_buttons["recycle_bin"] = self._create_clean_option_button(
            recycle_buttons_frame, "清空回收站", "recycle_bin", 0, 0
        )
        
        # 浏览器缓存清理选项
        browser_frame = ctk.CTkFrame(options_canvas, border_width=1, border_color=self.border_color)
        browser_frame.pack(padx=10, pady=10, fill="x")
        
        browser_label = ctk.CTkLabel(browser_frame, text="浏览器缓存清理", 
                                    font=ctk.CTkFont(size=16, weight="bold"),
                                    text_color=self.header_color)
        browser_label.pack(padx=10, pady=(10, 5), anchor="w")
        
        browser_buttons_frame = ctk.CTkFrame(browser_frame, fg_color="transparent")
        browser_buttons_frame.pack(padx=10, pady=5, fill="x")
        browser_buttons_frame.grid_columnconfigure(0, weight=1)
        browser_buttons_frame.grid_columnconfigure(1, weight=1)
        
        # Chrome按钮
        self.clean_option_buttons["chrome"] = self._create_clean_option_button(
            browser_buttons_frame, "Google Chrome", "chrome", 0, 0
        )
        
        # Edge按钮
        self.clean_option_buttons["edge"] = self._create_clean_option_button(
            browser_buttons_frame, "Microsoft Edge", "edge", 0, 1
        )
        
        # Firefox按钮
        self.clean_option_buttons["firefox"] = self._create_clean_option_button(
            browser_buttons_frame, "Mozilla Firefox", "firefox", 1, 0
        )
        
        # Opera按钮
        self.clean_option_buttons["opera"] = self._create_clean_option_button(
            browser_buttons_frame, "Opera", "opera", 1, 1
        )
        
        # 添加全选按钮
        buttons_frame = ctk.CTkFrame(options_canvas, fg_color="transparent")
        buttons_frame.pack(padx=10, pady=10, fill="x")
        
        select_all_btn = ctk.CTkButton(buttons_frame, text="全选", 
                                      command=self._on_select_all,
                                      fg_color=self.button_color, 
                                      hover_color=self.button_hover_color,
                                      width=100)
        select_all_btn.pack(side="left", padx=10)
        
        deselect_all_btn = ctk.CTkButton(buttons_frame, text="取消全选", 
                                        command=self._on_deselect_all,
                                        fg_color=self.button_color, 
                                        hover_color=self.button_hover_color,
                                        width=100)
        deselect_all_btn.pack(side="left", padx=10)
        
    def _setup_cleaner_results(self, parent):
        """设置清理结果界面"""
        result_frame = ctk.CTkFrame(parent, border_width=1, border_color=self.border_color)
        result_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        result_label = ctk.CTkLabel(result_frame, text="清理结果", 
                                   font=ctk.CTkFont(size=16, weight="bold"),
                                   text_color=self.header_color)
        result_label.pack(padx=10, pady=10)
        
        # 使用CTkTextbox，它已经内置了滚动功能
        self.result_text = ctk.CTkTextbox(result_frame, height=300, 
                                         font=ctk.CTkFont(family="Consolas", size=12),
                                         fg_color=("#f5f5f5", "#2b2b2b"),
                                         text_color=("#333333", "#e0e0e0"),
                                         border_width=1,
                                         border_color=self.border_color,
                                         corner_radius=6)
        self.result_text.pack(padx=10, pady=10, fill="both", expand=True)
        
    def _setup_safety_settings(self, parent):
        """设置安全设置界面"""
        # 创建滚动框架
        safety_canvas = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        safety_canvas.pack(fill="both", expand=True, padx=5, pady=5)
        
        # 安全模式设置
        safety_frame = ctk.CTkFrame(safety_canvas, border_width=1, border_color=self.border_color)
        safety_frame.pack(padx=10, pady=10, fill="x")
        
        safety_label = ctk.CTkLabel(safety_frame, text="安全模式设置", 
                                   font=ctk.CTkFont(size=16, weight="bold"),
                                   text_color=self.header_color)
        safety_label.pack(padx=10, pady=(10, 5), anchor="w")
        
        # 安全模式开关
        safe_mode_frame = ctk.CTkFrame(safety_frame, fg_color="transparent")
        safe_mode_frame.pack(padx=10, pady=5, fill="x")
        
        safe_mode_label = ctk.CTkLabel(safe_mode_frame, text="安全模式:", 
                                      font=ctk.CTkFont(size=14))
        safe_mode_label.pack(side="left", padx=(0, 10))
        
        self.safe_mode_switch = ctk.CTkSwitch(safe_mode_frame, text="启用", 
                                            command=self._on_toggle_safe_mode,
                                            progress_color=self.button_color)
        self.safe_mode_switch.pack(side="left")
        self.safe_mode_switch.select()  # 默认启用安全模式
        
        # 安全模式说明
        safe_mode_desc = ctk.CTkLabel(safety_frame, 
                                     text="安全模式将跳过重要文件和文件夹，防止误删除。\n"
                                          "禁用安全模式可能会导致系统不稳定，请谨慎操作。",
                                     font=ctk.CTkFont(size=12),
                                     text_color="gray50")
        safe_mode_desc.pack(padx=10, pady=5, anchor="w")
        
        # 文件年龄设置
        age_frame = ctk.CTkFrame(safety_frame, border_width=1, border_color=self.border_color)
        age_frame.pack(padx=10, pady=10, fill="x")
        
        age_label = ctk.CTkLabel(age_frame, text="文件年龄设置", 
                                font=ctk.CTkFont(size=16, weight="bold"),
                                text_color=self.header_color)
        age_label.pack(padx=10, pady=(10, 5), anchor="w")
        
        # 文件年龄滑块
        age_slider_frame = ctk.CTkFrame(age_frame, fg_color="transparent")
        age_slider_frame.pack(padx=10, pady=5, fill="x")
        
        age_slider_label = ctk.CTkLabel(age_slider_frame, text="清理超过此天数的文件:", 
                                       font=ctk.CTkFont(size=14))
        age_slider_label.pack(side="top", anchor="w", padx=(0, 10), pady=(0, 5))
        
        self.age_slider = ctk.CTkSlider(age_slider_frame, from_=1, to=30, 
                                       command=self._on_age_slider_change,
                                       progress_color=self.button_color)
        self.age_slider.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.age_slider.set(7)  # 默认7天
        
        self.age_label = ctk.CTkLabel(age_slider_frame, text="7天", 
                                     font=ctk.CTkFont(size=14))
        self.age_label.pack(side="left")
        
        # 安全路径设置
        paths_frame = ctk.CTkFrame(safety_frame, border_width=1, border_color=self.border_color)
        paths_frame.pack(padx=10, pady=10, fill="x")
        
        paths_label = ctk.CTkLabel(paths_frame, text="安全路径设置", 
                                  font=ctk.CTkFont(size=16, weight="bold"),
                                  text_color=self.header_color)
        paths_label.pack(padx=10, pady=(10, 5), anchor="w")
        
        # 安全路径列表
        paths_list_frame = ctk.CTkFrame(paths_frame, fg_color="transparent")
        paths_list_frame.pack(padx=10, pady=5, fill="x")
        
        # 创建带滚动条的列表框
        paths_list_container = ctk.CTkFrame(paths_list_frame, fg_color="transparent")
        paths_list_container.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self.paths_listbox = tk.Listbox(paths_list_container, height=5, 
                                       borderwidth=1, relief="solid")
        self.paths_listbox.pack(side="left", fill="both", expand=True)
        
        paths_scrollbar = ttk.Scrollbar(paths_list_container, orient="vertical", 
                                       command=self.paths_listbox.yview)
        self.paths_listbox.configure(yscrollcommand=paths_scrollbar.set)
        paths_scrollbar.pack(side="right", fill="y")
        
        paths_buttons_frame = ctk.CTkFrame(paths_list_frame, fg_color="transparent")
        paths_buttons_frame.pack(side="left", fill="y")
        
        add_path_btn = ctk.CTkButton(paths_buttons_frame, text="添加", 
                                    command=self._on_add_safe_path,
                                    fg_color=self.button_color, 
                                    hover_color=self.button_hover_color,
                                    width=80)
        add_path_btn.pack(pady=2)
        
        remove_path_btn = ctk.CTkButton(paths_buttons_frame, text="移除", 
                                       command=self._on_remove_safe_path,
                                       fg_color=self.button_color, 
                                       hover_color=self.button_hover_color,
                                       width=80)
        remove_path_btn.pack(pady=2)
        
        # 排除的文件类型设置
        ext_frame = ctk.CTkFrame(safety_frame, border_width=1, border_color=self.border_color)
        ext_frame.pack(padx=10, pady=10, fill="x")
        
        ext_label = ctk.CTkLabel(ext_frame, text="排除的文件类型", 
                                font=ctk.CTkFont(size=16, weight="bold"),
                                text_color=self.header_color)
        ext_label.pack(padx=10, pady=(10, 5), anchor="w")
        
        # 文件类型输入框
        ext_input_frame = ctk.CTkFrame(ext_frame, fg_color="transparent")
        ext_input_frame.pack(padx=10, pady=5, fill="x")
        
        self.ext_entry = ctk.CTkEntry(ext_input_frame, placeholder_text=".扩展名",
                                     border_color=self.border_color)
        self.ext_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        add_ext_btn = ctk.CTkButton(ext_input_frame, text="添加", 
                                   command=self._on_add_excluded_extension,
                                   fg_color=self.button_color, 
                                   hover_color=self.button_hover_color,
                                   width=80)
        add_ext_btn.pack(side="left")
        
        # 文件类型列表
        ext_list_frame = ctk.CTkFrame(ext_frame, fg_color="transparent")
        ext_list_frame.pack(padx=10, pady=5, fill="x")
        
        # 创建带滚动条的列表框
        ext_list_container = ctk.CTkFrame(ext_list_frame, fg_color="transparent")
        ext_list_container.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self.ext_listbox = tk.Listbox(ext_list_container, height=5,
                                     borderwidth=1, relief="solid")
        self.ext_listbox.pack(side="left", fill="both", expand=True)
        
        ext_scrollbar = ttk.Scrollbar(ext_list_container, orient="vertical", 
                                     command=self.ext_listbox.yview)
        self.ext_listbox.configure(yscrollcommand=ext_scrollbar.set)
        ext_scrollbar.pack(side="right", fill="y")
        
        remove_ext_btn = ctk.CTkButton(ext_list_frame, text="移除", 
                                      command=self._on_remove_excluded_extension,
                                      fg_color=self.button_color, 
                                      hover_color=self.button_hover_color,
                                      width=80)
        remove_ext_btn.pack(side="left", anchor="n")
        
    def _setup_progress_and_actions(self):
        """设置进度条和操作按钮"""
        # 添加进度条框架
        progress_container = ctk.CTkFrame(self, fg_color="transparent")
        progress_container.pack(padx=20, pady=10, fill="x")
        
        progress_label = ctk.CTkLabel(progress_container, text="进度:", 
                                     font=ctk.CTkFont(size=14))
        progress_label.pack(side="left", padx=(0, 10))
        
        self.progress_bar = ctk.CTkProgressBar(progress_container, height=15,
                                              progress_color=self.button_color)
        self.progress_bar.pack(side="left", fill="x", expand=True)
        self.progress_bar.set(0)
        
        # 添加操作按钮框架
        action_container = ctk.CTkFrame(self, fg_color="transparent")
        action_container.pack(padx=20, pady=(10, 20), fill="x")
        
        scan_button = ctk.CTkButton(action_container, text="扫描", 
                                   command=self._on_scan,
                                   fg_color=self.button_color, 
                                   hover_color=self.button_hover_color,
                                   width=120, height=35,
                                   border_width=1, border_color=self.border_color)
        scan_button.pack(side="left", padx=10)
        
        clean_button = ctk.CTkButton(action_container, text="一键清理", 
                                    command=self._on_clean,
                                    fg_color=self.button_color, 
                                    hover_color=self.button_hover_color,
                                    width=120, height=35,
                                    border_width=1, border_color=self.border_color)
        clean_button.pack(side="left", padx=10)
        
        # 添加安全模式状态标签
        self.safe_mode_status = ctk.CTkLabel(action_container, text="安全模式: 已启用", 
                                           font=ctk.CTkFont(size=14),
                                           text_color="green")
        self.safe_mode_status.pack(side="right", padx=10)
        
    def _create_clean_option_button(self, parent, text, option_key, row, column):
        """创建清理选项按钮"""
        button = ctk.CTkButton(
            parent, 
            text=text,
            command=lambda: self._on_toggle_option(option_key),
            fg_color=self.button_color,
            hover_color=self.button_hover_color,
            width=150,
            height=30,
            border_width=1,
            border_color=self.border_color
        )
        button.grid(row=row, column=column, padx=5, pady=5, sticky="w")
        return button
        
    def set_controller(self, controller):
        """设置控制器"""
        self.controller = controller
        self._update_safety_settings()
        
    def set_color_scheme(self, border_color, header_color, button_color, button_hover_color):
        """设置颜色方案"""
        self.border_color = border_color
        self.header_color = header_color
        self.button_color = button_color
        self.button_hover_color = button_hover_color
        
        # 更新组件颜色
        self._update_component_colors()
        
    def _update_component_colors(self):
        """更新组件颜色"""
        # 更新按钮颜色
        for key, button in self.clean_option_buttons.items():
            button.configure(
                border_color=self.border_color
            )
            
        # 更新进度条颜色
        if hasattr(self, 'progress_bar'):
            self.progress_bar.configure(progress_color=self.button_color)
            
        # 更新滑块颜色
        if hasattr(self, 'age_slider'):
            self.age_slider.configure(progress_color=self.button_color)
            
        # 更新开关颜色
        if hasattr(self, 'safe_mode_switch'):
            self.safe_mode_switch.configure(progress_color=self.button_color)
        
    def _update_safety_settings(self):
        """更新安全设置界面"""
        if not self.controller:
            return
            
        # 更新安全路径列表
        self.paths_listbox.delete(0, tk.END)
        for path in self.controller.get_safe_paths():
            self.paths_listbox.insert(tk.END, path)
            
        # 更新排除的文件类型列表
        self.ext_listbox.delete(0, tk.END)
        for ext in self.controller.get_excluded_extensions():
            self.ext_listbox.insert(tk.END, ext)
            
        # 更新文件年龄滑块
        self.age_slider.set(self.controller.get_max_file_age())
        self.age_label.configure(text=f"{self.controller.get_max_file_age()}天")
        
        # 更新安全模式开关
        if self.controller.is_safe_mode_enabled():
            self.safe_mode_switch.select()
            self.safe_mode_status.configure(text="安全模式: 已启用", text_color="green")
        else:
            self.safe_mode_switch.deselect()
            self.safe_mode_status.configure(text="安全模式: 已禁用", text_color="red")
        
    def _on_toggle_option(self, option_key):
        """切换清理选项状态"""
        if self.controller:
            self.controller.toggle_clean_option(option_key)
            
    def _on_select_all(self):
        """选择所有选项"""
        if self.controller:
            self.controller.select_all_options()
            
    def _on_deselect_all(self):
        """取消选择所有选项"""
        if self.controller:
            self.controller.deselect_all_options()
            
    def _on_toggle_safe_mode(self):
        """切换安全模式"""
        if self.controller:
            safe_mode = self.controller.toggle_safe_mode()
            self.update_safe_mode_status(safe_mode)
            
    def _on_age_slider_change(self, value):
        """文件年龄滑块变化"""
        days = int(value)
        self.age_label.configure(text=f"{days}天")
        if self.controller:
            self.controller.set_max_file_age(days)
            
    def _on_add_safe_path(self):
        """添加安全路径"""
        if self.controller:
            path = filedialog.askdirectory(title="选择要保护的文件夹")
            if path:
                if self.controller.add_safe_path(path):
                    self.paths_listbox.insert(tk.END, path)
                    
    def _on_remove_safe_path(self):
        """移除安全路径"""
        if self.controller:
            selected = self.paths_listbox.curselection()
            if selected:
                path = self.paths_listbox.get(selected[0])
                if self.controller.remove_safe_path(path):
                    self.paths_listbox.delete(selected[0])
                    
    def _on_add_excluded_extension(self):
        """添加排除的文件类型"""
        if self.controller:
            ext = self.ext_entry.get().strip()
            if ext:
                if not ext.startswith('.'):
                    ext = '.' + ext
                if self.controller.add_excluded_extension(ext):
                    self.ext_listbox.insert(tk.END, ext)
                    self.ext_entry.delete(0, tk.END)
                    
    def _on_remove_excluded_extension(self):
        """移除排除的文件类型"""
        if self.controller:
            selected = self.ext_listbox.curselection()
            if selected:
                ext = self.ext_listbox.get(selected[0])
                if self.controller.remove_excluded_extension(ext):
                    self.ext_listbox.delete(selected[0])
            
    def _on_scan(self):
        """扫描系统"""
        if self.controller:
            self.controller.scan_system()
            self.tabview.set("清理结果")
            
    def _on_clean(self):
        """清理系统"""
        if self.controller:
            self.controller.clean_system()
            self.tabview.set("清理结果")
            
    def update_progress(self, value):
        """更新进度条"""
        self.progress_bar.set(value)
        
    def update_result_text(self, text):
        """更新结果文本"""
        self.result_text.delete("0.0", "end")
        self.result_text.insert("0.0", text)
        
        # 为不同类型的行添加不同的颜色标记
        self._colorize_result_text()
        
    def update_safe_mode_status(self, is_enabled):
        """更新安全模式状态"""
        if is_enabled:
            self.safe_mode_status.configure(text="安全模式: 已启用", text_color="green")
        else:
            self.safe_mode_status.configure(text="安全模式: 已禁用", text_color="red")
            
    def update_max_file_age(self, days):
        """更新最大文件年龄"""
        self.age_label.configure(text=f"{days}天")
        self.age_slider.set(days)
        
    def get_clean_option_buttons(self):
        """获取清理选项按钮"""
        return self.clean_option_buttons
        
    def update_button_colors(self, option_key, is_selected):
        """更新按钮颜色"""
        if option_key in self.clean_option_buttons:
            button = self.clean_option_buttons[option_key]
            if is_selected:
                button.configure(
                    fg_color=self.button_color,
                    hover_color=self.button_hover_color
                )
            else:
                button.configure(
                    fg_color=("gray80", "gray30"),
                    hover_color=("gray70", "gray40")
                )

    def _colorize_result_text(self):
        """为不同类型的行添加不同的颜色标记"""
        # 获取文本内容
        text = self.result_text.get("0.0", "end")
        lines = text.split("\n")
        
        # 清除所有标签
        self.result_text.tag_remove("title", "0.0", "end")
        self.result_text.tag_remove("header", "0.0", "end")
        self.result_text.tag_remove("section", "0.0", "end")
        self.result_text.tag_remove("success", "0.0", "end")
        self.result_text.tag_remove("error", "0.0", "end")
        self.result_text.tag_remove("info", "0.0", "end")
        self.result_text.tag_remove("total", "0.0", "end")
        
        # 获取当前颜色模式
        mode = ctk.get_appearance_mode()  # 'Light' 或 'Dark'
        
        # 配置标签颜色 - 根据当前模式选择适当的颜色
        if mode == "Light":
            self.result_text.tag_config("title", foreground="#1a5fb4")
            self.result_text.tag_config("header", foreground="#1c71d8")
            self.result_text.tag_config("section", foreground="#613583")
            self.result_text.tag_config("success", foreground="#2ec27e")
            self.result_text.tag_config("error", foreground="#c01c28")
            self.result_text.tag_config("info", foreground="#a51d2d")
            # 使用更明显的颜色来强调总计行
            self.result_text.tag_config("total", foreground="#d4500c")
        else:  # Dark mode
            self.result_text.tag_config("title", foreground="#3584e4")
            self.result_text.tag_config("header", foreground="#62a0ea")
            self.result_text.tag_config("section", foreground="#c061cb")
            self.result_text.tag_config("success", foreground="#57e389")
            self.result_text.tag_config("error", foreground="#ff7b63")
            self.result_text.tag_config("info", foreground="#f66151")
            # 使用更明显的颜色来强调总计行
            self.result_text.tag_config("total", foreground="#ff9e36")
        
        # 为每一行应用适当的标签
        for i, line in enumerate(lines):
            line_start = f"{i+1}.0"
            line_end = f"{i+1}.end"
            
            # 标题行
            if "╔═══" in line or "╚═══" in line or "╠═══" in line:
                self.result_text.tag_add("title", line_start, line_end)
            # 标题内容
            elif "║" in line and ("系统扫描结果报告" in line or "系统清理结果报告" in line or "扫描时间" in line or "清理时间" in line):
                self.result_text.tag_add("title", line_start, line_end)
            # 分节标题
            elif "┌───" in line or "└───" in line:
                self.result_text.tag_add("section", line_start, line_end)
            # 成功项
            elif "✓" in line:
                self.result_text.tag_add("success", line_start, line_end)
            # 错误项
            elif "✗" in line:
                self.result_text.tag_add("error", line_start, line_end)
            # 信息项
            elif "●" in line:
                self.result_text.tag_add("info", line_start, line_end)
            # 总计行
            elif "总计" in line:
                self.result_text.tag_add("total", line_start, line_end)
            # 安全模式信息
            elif "📋" in line:
                self.result_text.tag_add("header", line_start, line_end) 