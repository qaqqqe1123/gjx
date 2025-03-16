import customtkinter as ctk

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=("#e6f0ff", "#d0e3ff"), width=200)
        
        self.controller = None
        self.nav_buttons = {}
        
        # 定义颜色方案
        self.border_color = ("#1a73e8", "#0b57d0")  # 蓝色边框
        self.header_color = ("#1a5fb4", "#0b3b8c")  # 标题颜色
        self.button_color = ("#1a73e8", "#0b57d0")  # 按钮颜色
        self.button_hover_color = ("#1557b0", "#0842a0")  # 按钮悬停颜色
        
        self._create_widgets()
        
    def set_color_scheme(self, border_color, header_color, button_color, button_hover_color):
        """设置颜色方案"""
        self.border_color = border_color
        self.header_color = header_color
        self.button_color = button_color
        self.button_hover_color = button_hover_color
        
        # 更新已有组件的颜色
        self._update_colors()
        
    def _update_colors(self):
        """更新组件颜色"""
        # 更新导航按钮颜色
        for text, btn in self.nav_buttons.items():
            btn.configure(
                text_color=self.header_color,
                hover_color=("#d0e3ff", "#b8d4ff")
            )
        
    def _create_widgets(self):
        """创建侧边栏组件"""
        # 功能导航标题
        nav_title = ctk.CTkLabel(self, text="功能导航", 
                                font=ctk.CTkFont(size=20, weight="bold"),
                                text_color=self.header_color)
        nav_title.pack(padx=20, pady=20)
        
        # 创建滚动框架
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scrollable_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # 系统工具标签
        tools_label = ctk.CTkLabel(self.scrollable_frame, text="系统工具", 
                                  font=ctk.CTkFont(size=16, weight="bold"),
                                  text_color=self.header_color)
        tools_label.pack(padx=10, pady=(10, 5), anchor="w")
        
        # 创建导航按钮框架
        nav_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent", 
                                border_width=1, border_color=self.border_color)
        nav_frame.pack(padx=10, pady=5, fill="x")
        
        # 创建导航按钮
        nav_items = [
            ("系统清理", "show_system_cleaner"),
            ("注册表清理", "show_registry_cleaner"),
            ("启动项管理", "show_startup_manager"),
            ("服务优化", "show_service_optimizer")
        ]
        
        for text, command in nav_items:
            btn = ctk.CTkButton(
                nav_frame,
                text=text,
                command=lambda cmd=command: self._on_nav_button_click(cmd),
                fg_color="transparent",
                text_color=self.header_color,
                hover_color=("#d0e3ff", "#b8d4ff"),
                anchor="w",
                height=40,
                width=180,
                border_width=0
            )
            btn.pack(padx=5, pady=2)
            self.nav_buttons[text] = btn
            
    def set_controller(self, controller):
        """设置控制器"""
        self.controller = controller
        
    def _on_nav_button_click(self, command):
        """导航按钮点击事件"""
        if self.controller and hasattr(self.controller, command):
            getattr(self.controller, command)()
            
    def update_button_states(self, active_button):
        """更新按钮状态"""
        for text, btn in self.nav_buttons.items():
            if text == active_button:
                btn.configure(
                    fg_color=self.button_color,
                    text_color="white",
                    hover_color=self.button_hover_color
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=self.header_color,
                    hover_color=("#d0e3ff", "#b8d4ff")
                ) 