import logging

class ServiceOptimizerController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        
        # 设置日志
        self.logger = logging.getLogger('ServiceOptimizerController')
        # 添加控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        self.view.set_controller(self)
        
    def refresh_services(self):
        """刷新服务列表"""
        self.logger.info("开始获取服务列表")
        try:
            services = self.model.get_all_services()
            if not services:
                self.logger.warning("获取到的服务列表为空")
                self.view.show_error("未能获取到任何服务")
                return
                
            self.logger.info(f"成功获取服务列表，共 {len(services)} 个服务")
            
            # 确保services是列表类型
            if not isinstance(services, list):
                self.logger.error(f"服务列表类型错误: {type(services)}")
                self.view.show_error("服务列表格式错误")
                return
                
            # 验证每个服务对象的格式
            for service in services:
                if not isinstance(service, dict):
                    self.logger.error(f"服务对象类型错误: {type(service)}")
                    continue
                    
                required_keys = ["name", "display_name", "status", "startup_type", "description"]
                missing_keys = [key for key in required_keys if key not in service]
                if missing_keys:
                    self.logger.error(f"服务对象缺少必要字段: {missing_keys}")
                    continue
                    
            self.view.update_services(services)
            self.logger.info("服务列表更新完成")
            
        except Exception as e:
            self.logger.error(f"刷新服务列表时出错: {str(e)}")
            self.view.show_error(f"刷新服务列表时出错: {str(e)}")
        
    def start_service(self, service_name):
        """启动服务"""
        success, message = self.model.start_service(service_name)
        if success:
            self.view.show_success(message)
            self.refresh_services()
        else:
            self.view.show_error(message)
            
    def stop_service(self, service_name):
        """停止服务"""
        success, message = self.model.stop_service(service_name)
        if success:
            self.view.show_success(message)
            self.refresh_services()
        else:
            self.view.show_error(message)
            
    def set_service_startup_type(self, service_name, startup_type):
        """设置服务启动类型"""
        success, message = self.model.set_startup_type(service_name, startup_type)
        if success:
            self.view.show_success(message)
            self.refresh_services()
        else:
            self.view.show_error(message)
            
    def search_services(self, keyword):
        """搜索服务"""
        services = self.model.search_services(keyword)
        self.view.update_services(services)
        
    def show_service_details(self, service_name):
        """显示服务详情"""
        # 获取服务信息
        services = self.model.get_all_services()
        service = next((s for s in services if s["name"] == service_name), None)
        
        if service:
            details = f"""
服务名称: {service['name']}
显示名称: {service['display_name']}
当前状态: {service['status']}
启动类型: {service['startup_type']}
描述: {service['description']}
"""
            self.view.show_service_details(details)
        else:
            self.view.show_error("未找到服务详情")
        
    def optimize_services(self):
        """一键优化服务"""
        success, message = self.model.optimize_services()
        if success:
            self.view.show_success(message)
            self.refresh_services()
        else:
            self.view.show_error(message)
        
    def restore_services(self):
        """还原服务默认设置"""
        success, message = self.model.restore_services()
        if success:
            self.view.show_success(message)
            self.refresh_services()
        else:
            self.view.show_error(message) 