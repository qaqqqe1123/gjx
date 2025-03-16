import threading
from .system_cleaner_controller import SystemCleanerController
from .registry_cleaner_controller import RegistryCleanerController
from mvc.models.system_cleaner_model import SystemCleanerModel
from mvc.models.registry_cleaner_model import RegistryCleanerModel

class AppController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        
        # 创建系统清理模型和控制器
        self.system_cleaner_model = SystemCleanerModel()
        self.system_cleaner_controller = SystemCleanerController(
            self.view.content_area.pages["system_cleaner"],
            self.system_cleaner_model
        )
        
        # 创建注册表清理模型和控制器
        self.registry_cleaner_model = RegistryCleanerModel()
        self.registry_cleaner_controller = RegistryCleanerController(
            self.view.content_area.pages["registry_cleaner"],
            self.registry_cleaner_model
        )
        
        # 设置视图的控制器引用
        self.view.set_controller(self)
        
        # 显示默认页面
        self.show_system_cleaner()
        
    def show_system_cleaner(self):
        """显示系统清理页面"""
        self.view.show_page("system_cleaner")
        self.view.update_nav_button_states("系统清理")
        
    def show_registry_cleaner(self):
        """显示注册表清理页面"""
        self.view.show_page("registry_cleaner")
        self.view.update_nav_button_states("注册表清理")
        
    def show_startup_manager(self):
        """显示启动项管理页面"""
        self.view.show_page("startup_manager")
        self.view.update_nav_button_states("启动项管理")
        
    def show_service_optimizer(self):
        """显示服务优化页面"""
        self.view.show_page("service_optimizer")
        self.view.update_nav_button_states("服务优化")
        
    # 系统清理相关方法委托给系统清理控制器
    def toggle_clean_option(self, option_key):
        """切换清理选项状态"""
        if self.view.current_page == self.view.content_area.pages["system_cleaner"]:
            self.system_cleaner_controller.toggle_clean_option(option_key)
        elif self.view.current_page == self.view.content_area.pages["registry_cleaner"]:
            self.registry_cleaner_controller.toggle_clean_option(option_key)
        
    def select_all_options(self):
        """选择所有清理选项"""
        if self.view.current_page == self.view.content_area.pages["system_cleaner"]:
            self.system_cleaner_controller.select_all_options()
        elif self.view.current_page == self.view.content_area.pages["registry_cleaner"]:
            self.registry_cleaner_controller.select_all_options()
        
    def deselect_all_options(self):
        """取消选择所有清理选项"""
        if self.view.current_page == self.view.content_area.pages["system_cleaner"]:
            self.system_cleaner_controller.deselect_all_options()
        elif self.view.current_page == self.view.content_area.pages["registry_cleaner"]:
            self.registry_cleaner_controller.deselect_all_options()
        
    def scan_system(self):
        """扫描系统"""
        self.system_cleaner_controller.scan_system()
        
    def clean_system(self):
        """清理系统"""
        self.system_cleaner_controller.clean_system()
        
    def scan_registry(self):
        """扫描注册表"""
        self.registry_cleaner_controller.scan_registry()
        
    def clean_registry(self):
        """清理注册表"""
        self.registry_cleaner_controller.clean_registry()
        
    def backup_registry(self):
        """备份注册表"""
        self.registry_cleaner_controller.backup_registry()
        
    # 安全路径相关方法委托给系统清理控制器
    def toggle_safe_mode(self):
        """切换安全模式"""
        return self.system_cleaner_controller.toggle_safe_mode()
        
    def set_max_file_age(self, days):
        """设置最大文件年龄"""
        return self.system_cleaner_controller.set_max_file_age(days)
        
    def add_safe_path(self, path):
        """添加安全路径"""
        return self.system_cleaner_controller.add_safe_path(path)
        
    def remove_safe_path(self, path):
        """移除安全路径"""
        return self.system_cleaner_controller.remove_safe_path(path)
        
    def add_excluded_extension(self, extension):
        """添加排除的文件类型"""
        return self.system_cleaner_controller.add_excluded_extension(extension)
        
    def remove_excluded_extension(self, extension):
        """移除排除的文件类型"""
        return self.system_cleaner_controller.remove_excluded_extension(extension)
        
    def get_safe_paths(self):
        """获取安全路径列表"""
        return self.system_cleaner_controller.get_safe_paths()
        
    def get_excluded_extensions(self):
        """获取排除的文件类型列表"""
        return self.system_cleaner_controller.get_excluded_extensions()
        
    def get_max_file_age(self):
        """获取最大文件年龄"""
        return self.system_cleaner_controller.get_max_file_age()
        
    def is_safe_mode_enabled(self):
        """检查安全模式是否启用"""
        return self.system_cleaner_controller.is_safe_mode_enabled() 