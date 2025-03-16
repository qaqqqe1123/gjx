import customtkinter as ctk
from .system_cleaner_page import SystemCleanerPage
from .registry_cleaner_page import RegistryCleanerPage
from .startup_manager_page import StartupManagerPage
from .service_optimizer_page import ServiceOptimizerPage

class ContentArea(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=("white", "#f0f6ff"))
        
        self.controller = None
        self.current_page = None
        self.pages = {}
        
        # 定义颜色方案
        self.border_color = ("#1a73e8", "#0b57d0")  # 蓝色边框
        self.header_color = ("#1a5fb4", "#0b3b8c")  # 标题颜色
        self.button_color = ("#1a73e8", "#0b57d0")  # 按钮颜色
        self.button_hover_color = ("#1557b0", "#0842a0")  # 按钮悬停颜色
        
        # 添加边框
        self.configure(border_width=1, border_color=self.border_color)
        
        # 创建滚动框架
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scrollable_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self._create_pages()
        
    def set_color_scheme(self, border_color, header_color, button_color, button_hover_color):
        """设置颜色方案"""
        self.border_color = border_color
        self.header_color = header_color
        self.button_color = button_color
        self.button_hover_color = button_hover_color
        
        # 更新边框颜色
        self.configure(border_color=self.border_color)
        
        # 更新页面颜色
        self._update_page_colors()
        
    def _update_page_colors(self):
        """更新页面颜色"""
        for page_name, page in self.pages.items():
            if hasattr(page, 'set_color_scheme'):
                page.set_color_scheme(
                    self.border_color,
                    self.header_color,
                    self.button_color,
                    self.button_hover_color
                )
        
    def _create_pages(self):
        """创建所有页面"""
        # 系统清理页面
        self.pages["system_cleaner"] = SystemCleanerPage(self.scrollable_frame)
        
        # 注册表清理页面
        self.pages["registry_cleaner"] = RegistryCleanerPage(self.scrollable_frame)
        
        # 启动项管理页面
        self.pages["startup_manager"] = StartupManagerPage(self.scrollable_frame)
        
        # 服务优化页面
        self.pages["service_optimizer"] = ServiceOptimizerPage(self.scrollable_frame)
        
    def set_controller(self, controller):
        """设置控制器"""
        self.controller = controller
        for page in self.pages.values():
            page.set_controller(controller)
            
    def show_page(self, page_name):
        """显示指定页面"""
        if self.current_page:
            self.current_page.pack_forget()
            
        if page_name in self.pages:
            self.current_page = self.pages[page_name]
            self.current_page.pack(fill="both", expand=True)
            
    def update_progress(self, value):
        """更新进度条"""
        if self.current_page and hasattr(self.current_page, "update_progress"):
            self.current_page.update_progress(value)
            
    def update_result_text(self, text):
        """更新结果文本"""
        if self.current_page and hasattr(self.current_page, "update_result_text"):
            self.current_page.update_result_text(text)
            
    def get_clean_option_buttons(self):
        """获取清理选项按钮"""
        if "system_cleaner" in self.pages:
            return self.pages["system_cleaner"].get_clean_option_buttons()
        return {}
        
    def update_button_colors(self, option_key, is_selected):
        """更新按钮颜色"""
        if "system_cleaner" in self.pages:
            self.pages["system_cleaner"].update_button_colors(option_key, is_selected) 