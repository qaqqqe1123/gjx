import customtkinter as ctk
from tkinter import ttk  # 添加ttk导入

class RegistryCleanerPage(ctk.CTkFrame):
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
        title = ctk.CTkLabel(self, text="注册表清理", 
                            font=ctk.CTkFont(size=24, weight="bold"),
                            text_color=self.header_color)
        title.pack(padx=20, pady=20)
        
        # 创建选项卡
        self.tabview = ctk.CTkTabview(self, fg_color=("white", "#edf2fb"))
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 添加选项卡
        self.tabview.add("清理选项")
        self.tabview.add("清理结果")
        self.tabview.set("清理选项")
        
        # 配置选项卡
        self._setup_cleaner_options(self.tabview.tab("清理选项"))
        self._setup_cleaner_results(self.tabview.tab("清理结果"))
        
        # 添加进度条和操作按钮
        self._setup_progress_and_actions()
        
    def _setup_cleaner_options(self, parent):
        """设置清理选项界面"""
        # 创建滚动框架
        options_canvas = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        options_canvas.pack(fill="both", expand=True, padx=5, pady=5)
        
        # 无效项清理选项
        invalid_frame = ctk.CTkFrame(options_canvas, border_width=1, border_color=self.border_color)
        invalid_frame.pack(padx=10, pady=10, fill="x")
        
        invalid_label = ctk.CTkLabel(invalid_frame, text="无效项清理", 
                                    font=ctk.CTkFont(size=16, weight="bold"),
                                    text_color=self.header_color)
        invalid_label.pack(padx=10, pady=(10, 5), anchor="w")
        
        invalid_buttons_frame = ctk.CTkFrame(invalid_frame, fg_color="transparent")
        invalid_buttons_frame.pack(padx=10, pady=5, fill="x")
        invalid_buttons_frame.grid_columnconfigure(0, weight=1)
        invalid_buttons_frame.grid_columnconfigure(1, weight=1)
        
        # 无效的软件项按钮
        self.clean_option_buttons["invalid_software"] = self._create_clean_option_button(
            invalid_buttons_frame, "无效的软件项", "invalid_software", 0, 0
        )
        
        # 无效的文件关联按钮
        self.clean_option_buttons["invalid_file_assoc"] = self._create_clean_option_button(
            invalid_buttons_frame, "无效的文件关联", "invalid_file_assoc", 0, 1
        )
        
        # 无效的启动项按钮
        self.clean_option_buttons["invalid_startup"] = self._create_clean_option_button(
            invalid_buttons_frame, "无效的启动项", "invalid_startup", 1, 0
        )
        
        # 无效的卸载信息按钮
        self.clean_option_buttons["invalid_uninstall"] = self._create_clean_option_button(
            invalid_buttons_frame, "无效的卸载信息", "invalid_uninstall", 1, 1
        )
        
        # 冗余项清理选项
        redundant_frame = ctk.CTkFrame(options_canvas, border_width=1, border_color=self.border_color)
        redundant_frame.pack(padx=10, pady=10, fill="x")
        
        redundant_label = ctk.CTkLabel(redundant_frame, text="冗余项清理", 
                                      font=ctk.CTkFont(size=16, weight="bold"),
                                      text_color=self.header_color)
        redundant_label.pack(padx=10, pady=(10, 5), anchor="w")
        
        redundant_buttons_frame = ctk.CTkFrame(redundant_frame, fg_color="transparent")
        redundant_buttons_frame.pack(padx=10, pady=5, fill="x")
        redundant_buttons_frame.grid_columnconfigure(0, weight=1)
        redundant_buttons_frame.grid_columnconfigure(1, weight=1)
        
        # 冗余的COM组件按钮
        self.clean_option_buttons["redundant_com"] = self._create_clean_option_button(
            redundant_buttons_frame, "冗余的COM组件", "redundant_com", 0, 0
        )
        
        # 冗余的类型库按钮
        self.clean_option_buttons["redundant_typelib"] = self._create_clean_option_button(
            redundant_buttons_frame, "冗余的类型库", "redundant_typelib", 0, 1
        )
        
        # 冗余的帮助文件按钮
        self.clean_option_buttons["redundant_help"] = self._create_clean_option_button(
            redundant_buttons_frame, "冗余的帮助文件", "redundant_help", 1, 0
        )
        
        # 冗余的共享DLL按钮
        self.clean_option_buttons["redundant_dll"] = self._create_clean_option_button(
            redundant_buttons_frame, "冗余的共享DLL", "redundant_dll", 1, 1
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
        
        self.result_text = ctk.CTkTextbox(result_frame, height=300, 
                                         font=ctk.CTkFont(family="Consolas", size=12),
                                         fg_color=("#f5f5f5", "#2b2b2b"),
                                         text_color=("#333333", "#e0e0e0"),
                                         border_width=1,
                                         border_color=self.border_color,
                                         corner_radius=6)
        self.result_text.pack(padx=10, pady=10, fill="both", expand=True)
        
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
        
        backup_button = ctk.CTkButton(action_container, text="备份注册表", 
                                     command=self._on_backup,
                                    fg_color=self.button_color, 
                                    hover_color=self.button_hover_color,
                                    width=120, height=35,
                                    border_width=1, border_color=self.border_color)
        backup_button.pack(side="left", padx=10)
        
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
            
    def _on_scan(self):
        """扫描注册表"""
        if self.controller:
            self.controller.scan_registry()
            self.tabview.set("清理结果")
            
    def _on_clean(self):
        """清理注册表"""
        if self.controller:
            self.controller.clean_registry()
            self.tabview.set("清理结果")
            
    def _on_backup(self):
        """备份注册表"""
        if self.controller:
            self.controller.backup_registry()
            
    def update_progress(self, value):
        """更新进度条"""
        self.progress_bar.set(value)
        
    def update_result_text(self, text):
        """更新结果文本"""
        self.result_text.delete("0.0", "end")
        self.result_text.insert("0.0", text)
        
        # 为不同类型的行添加不同的颜色标记
        self._colorize_result_text()
        
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
            elif "║" in line and ("注册表扫描结果报告" in line or "注册表清理结果报告" in line or "扫描时间" in line or "清理时间" in line):
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