import threading
from mvc.models.registry_cleaner_model import RegistryCleanerModel

class RegistryCleanerController:
    def __init__(self, view, model=None):
        self.view = view
        self.model = model if model else RegistryCleanerModel()
        
    def toggle_clean_option(self, option_key):
        """切换清理选项状态"""
        if self.model.toggle_option(option_key):
            self.view.update_button_colors(option_key, self.model.clean_options[option_key])
            
    def select_all_options(self):
        """选择所有清理选项"""
        self.model.select_all_options()
        for key in self.model.clean_options:
            self.view.update_button_colors(key, True)
            
    def deselect_all_options(self):
        """取消选择所有清理选项"""
        self.model.deselect_all_options()
        for key in self.model.clean_options:
            self.view.update_button_colors(key, False)
            
    def scan_registry(self):
        """扫描注册表"""
        def scan_task():
            # 更新UI
            self.view.update_result_text("正在扫描注册表...\n")
            self.view.update_progress(0)
            
            # 执行扫描
            results = self.model.scan_registry()
            
            # 更新结果
            formatted_results = self.model.get_formatted_scan_results()
            self.view.update_result_text(formatted_results)
            self.view.update_progress(1)
            
        # 在新线程中运行扫描任务
        threading.Thread(target=scan_task, daemon=True).start()
        
    def clean_registry(self):
        """清理注册表"""
        def clean_task():
            # 更新UI
            self.view.update_result_text("正在清理注册表...\n")
            self.view.update_progress(0)
            
            # 执行清理
            results = self.model.clean_registry()
            
            # 更新结果
            formatted_results = self.model.get_formatted_clean_results()
            self.view.update_result_text(formatted_results)
            self.view.update_progress(1)
            
        # 在新线程中运行清理任务
        threading.Thread(target=clean_task, daemon=True).start()
        
    def backup_registry(self):
        """备份注册表"""
        def backup_task():
            # 更新UI
            self.view.update_result_text("正在备份注册表...\n")
            self.view.update_progress(0)
            
            # 执行备份
            backup_result = self.model.backup_registry()
            
            # 更新结果
            formatted_results = self.model.get_formatted_backup_results(backup_result)
            self.view.update_result_text(formatted_results)
            self.view.update_progress(1)
            
        # 在新线程中运行备份任务
        threading.Thread(target=backup_task, daemon=True).start() 