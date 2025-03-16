import threading

class SystemCleanerController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        
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
            
    def toggle_safe_mode(self):
        """切换安全模式"""
        safe_mode = self.model.toggle_safe_mode()
        if hasattr(self.view, 'update_safe_mode_status'):
            self.view.update_safe_mode_status(safe_mode)
        return safe_mode
        
    def set_max_file_age(self, days):
        """设置最大文件年龄"""
        if self.model.set_max_file_age(days):
            if hasattr(self.view, 'update_max_file_age'):
                self.view.update_max_file_age(days)
            return True
        return False
        
    def add_safe_path(self, path):
        """添加安全路径"""
        return self.model.add_safe_path(path)
        
    def remove_safe_path(self, path):
        """移除安全路径"""
        return self.model.remove_safe_path(path)
        
    def add_excluded_extension(self, extension):
        """添加排除的文件类型"""
        return self.model.add_excluded_extension(extension)
        
    def remove_excluded_extension(self, extension):
        """移除排除的文件类型"""
        return self.model.remove_excluded_extension(extension)
        
    def get_safe_paths(self):
        """获取安全路径列表"""
        return self.model.safe_paths
        
    def get_excluded_extensions(self):
        """获取排除的文件类型列表"""
        return self.model.excluded_extensions
        
    def get_max_file_age(self):
        """获取最大文件年龄"""
        return self.model.max_file_age_days
        
    def is_safe_mode_enabled(self):
        """检查安全模式是否启用"""
        return self.model.safe_mode
            
    def scan_system(self):
        """扫描系统"""
        def scan_task():
            # 更新UI
            self.view.update_result_text("正在扫描...\n")
            self.view.update_progress(0)
            
            # 执行扫描
            results = self.model.scan_system()
            
            # 更新结果
            formatted_results = self.model.get_formatted_scan_results()
            self.view.update_result_text(formatted_results)
            self.view.update_progress(1)
            
        # 在新线程中运行扫描任务
        threading.Thread(target=scan_task, daemon=True).start()
        
    def clean_system(self):
        """清理系统"""
        def clean_task():
            # 更新UI
            self.view.update_result_text("正在清理...\n")
            self.view.update_progress(0)
            
            # 执行清理
            results = self.model.clean_system()
            
            # 更新结果
            formatted_results = self.model.get_formatted_clean_results()
            self.view.update_result_text(formatted_results)
            self.view.update_progress(1)
            
        # 在新线程中运行清理任务
        threading.Thread(target=clean_task, daemon=True).start() 