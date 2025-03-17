class StartupManagerController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.view.set_controller(self)
        
    def refresh_startup_items(self):
        """刷新启动项列表"""
        items = self.model.get_all_startup_items()
        self.view.update_startup_items(items)
        
    def disable_startup_item(self, name, location):
        """禁用启动项"""
        success, message = self.model.disable_startup_item(name, location)
        if success:
            self.view.show_success(message)
            self.refresh_startup_items()
        else:
            self.view.show_error(message)
            
    def enable_startup_item(self, name, location):
        """启用启动项"""
        success, message = self.model.enable_startup_item(name, location)
        if success:
            self.view.show_success(message)
            self.refresh_startup_items()
        else:
            self.view.show_error(message) 