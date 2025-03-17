import customtkinter as ctk
from .components.sidebar import Sidebar
from .components.content_area import ContentArea

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # 定义颜色方案
        self.border_color = ("#1a73e8", "#0b57d0")  # 蓝色边框
        self.header_color = ("#1a5fb4", "#0b3b8c")  # 标题颜色
        self.button_color = ("#1a73e8", "#0b57d0")  # 按钮颜色
        self.button_hover_color = ("#1557b0", "#0842a0")  # 按钮悬停颜色
        self.bg_color = ("#ffffff", "#f0f6ff")  # 背景颜色
        
        # 配置窗口
        self.title("系统工具箱")
        self.geometry("1200x700")
        self.minsize(1000, 600)
        
        # 创建主框架
        self.main_frame = ctk.CTkFrame(self, fg_color=self.bg_color, 
                                      border_width=1, border_color=self.border_color)
        self.main_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # 创建侧边栏
        self.sidebar = Sidebar(self.main_frame)
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        
        # 创建内容区域
        self.content_area = ContentArea(self.main_frame)
        self.content_area.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        
        # 传递颜色方案给子组件
        self.pass_color_scheme()
        
    def pass_color_scheme(self):
        """将颜色方案传递给子组件"""
        if hasattr(self.sidebar, 'set_color_scheme'):
            self.sidebar.set_color_scheme(
                self.border_color, 
                self.header_color, 
                self.button_color, 
                self.button_hover_color
            )
            
        if hasattr(self.content_area, 'set_color_scheme'):
            self.content_area.set_color_scheme(
                self.border_color, 
                self.header_color, 
                self.button_color, 
                self.button_hover_color
            )
        
    def set_controller(self, controller):
        """设置控制器"""
        self.controller = controller
        self.sidebar.set_controller(controller)
        self.content_area.set_controller(controller)
        
    def update_nav_button_states(self, active_page):
        """更新导航按钮状态"""
        self.sidebar.update_button_states(active_page)
        
    def show_page(self, page_name):
        """显示指定页面"""
        self.content_area.show_page(page_name)
        
    def update_progress(self, value):
        """更新进度条"""
        self.content_area.update_progress(value)
        
    def update_result_text(self, text):
        """更新结果文本"""
        self.content_area.update_result_text(text)
        
    def get_clean_option_buttons(self):
        """获取清理选项按钮"""
        return self.content_area.get_clean_option_buttons()
        
    def update_button_colors(self, option_key, is_selected):
        """更新按钮颜色"""
        self.content_area.update_button_colors(option_key, is_selected) 