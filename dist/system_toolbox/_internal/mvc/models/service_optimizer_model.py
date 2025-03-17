import psutil
import win32serviceutil
import win32service
import json
import os
import logging
from pathlib import Path

class ServiceOptimizerModel:
    def __init__(self):
        self.services = []
        self.backup_file = os.path.join(str(Path.home()), 'service_backup.json')
        
        # 设置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            force=True
        )
        self.logger = logging.getLogger('ServiceOptimizer')
        # 添加控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # 优化配置：服务名称及其推荐的启动类型
        self.optimization_config = {
            # 可以禁用的服务
            'disable': [
                'TabletInputService',  # 平板电脑输入服务
                'WSearch',  # Windows搜索
                'DiagTrack',  # Connected User Experiences and Telemetry
                'dmwappushservice',  # WAP推送消息路由服务
                'MapsBroker',  # 下载的地图管理器
                'lfsvc',  # 地理位置服务
                'SharedAccess',  # Internet Connection Sharing (ICS)
                'WMPNetworkSvc',  # Windows Media Player Network Sharing Service
            ],
            # 可以设置为手动的服务
            'manual': [
                'Fax',  # 传真
                'PrintNotify',  # 打印机扩展
                'WerSvc',  # Windows错误报告服务
                'SysMain',  # Superfetch
                'WbioSrvc',  # Windows生物识别服务
                'FontCache',  # Windows字体缓存服务
                'PhoneSvc',  # 电话服务
            ],
            # 必须保持自动的服务
            'auto': [
                'Dhcp',  # DHCP客户端
                'Dnscache',  # DNS客户端
                'RpcSs',  # 远程过程调用
                'EventLog',  # Windows事件日志
                'Schedule',  # 任务计划程序
                'LSM',  # 本地会话管理器
                'PlugPlay',  # 即插即用
                'Power',  # 电源
                'SystemEventsBroker',  # 系统事件代理
                'Themes',  # 主题
                'UserManager',  # 用户管理器
                'Winmgmt',  # Windows Management Instrumentation
            ]
        }
        
    def get_all_services(self):
        """获取所有Windows服务"""
        self.logger.info("开始获取服务列表...")
        services = []
        try:
            # 获取服务列表前先清空现有列表
            self.services = []
            
            service_list = list(psutil.win_service_iter())
            self.logger.info(f"找到 {len(service_list)} 个服务")
            
            for service in service_list:
                try:
                    name = service.name()
                    display_name = service.display_name()
                    description = service.description()
                    
                    # 尝试获取服务状态和配置
                    try:
                        service_info = win32serviceutil.QueryServiceStatus(name)
                        service_config = win32serviceutil.QueryServiceConfig(name)
                        status = self._get_service_status(service_info[1])
                        startup_type = self._get_startup_type(service_config[1])
                    except Exception as e:
                        self.logger.warning(f"无法获取服务 {name} 的状态或配置: {str(e)}")
                        status = "未知"
                        startup_type = "未知"
                    
                    service_data = {
                        "name": name,
                        "display_name": display_name,
                        "status": status,
                        "startup_type": startup_type,
                        "description": description
                    }
                    
                    services.append(service_data)
                    self.logger.debug(f"成功添加服务: {name}")
                    
                except Exception as e:
                    self.logger.error(f"处理服务时出错: {str(e)}")
                    continue
            
            self.logger.info(f"成功获取 {len(services)} 个服务信息")
            self.services = services
            return services
            
        except Exception as e:
            self.logger.error(f"获取服务列表时出错: {str(e)}")
            return []
        
    def _get_service_status(self, status_code):
        """转换服务状态代码为可读文本"""
        status_map = {
            win32service.SERVICE_STOPPED: "已停止",
            win32service.SERVICE_START_PENDING: "正在启动",
            win32service.SERVICE_STOP_PENDING: "正在停止",
            win32service.SERVICE_RUNNING: "运行中",
            win32service.SERVICE_CONTINUE_PENDING: "继续挂起",
            win32service.SERVICE_PAUSE_PENDING: "暂停挂起",
            win32service.SERVICE_PAUSED: "已暂停"
        }
        return status_map.get(status_code, "未知")
        
    def _get_startup_type(self, start_type):
        """转换启动类型代码为可读文本"""
        type_map = {
            win32service.SERVICE_AUTO_START: "自动",
            win32service.SERVICE_DEMAND_START: "手动",
            win32service.SERVICE_DISABLED: "禁用",
            win32service.SERVICE_BOOT_START: "系统启动",
            win32service.SERVICE_SYSTEM_START: "系统"
        }
        return type_map.get(start_type, "未知")
        
    def start_service(self, service_name):
        """启动服务"""
        try:
            win32serviceutil.StartService(service_name)
            return True, "服务启动成功"
        except Exception as e:
            return False, f"启动服务失败: {str(e)}"
            
    def stop_service(self, service_name):
        """停止服务"""
        try:
            win32serviceutil.StopService(service_name)
            return True, "服务停止成功"
        except Exception as e:
            return False, f"停止服务失败: {str(e)}"
            
    def set_startup_type(self, service_name, startup_type):
        """设置服务启动类型"""
        type_map = {
            "auto": win32service.SERVICE_AUTO_START,
            "manual": win32service.SERVICE_DEMAND_START,
            "disabled": win32service.SERVICE_DISABLED
        }
        
        try:
            win32serviceutil.ChangeServiceConfig(
                service_name,
                startType=type_map.get(startup_type, win32service.SERVICE_NO_CHANGE)
            )
            return True, "服务启动类型修改成功"
        except Exception as e:
            return False, f"修改服务启动类型失败: {str(e)}"
            
    def search_services(self, keyword):
        """搜索服务"""
        if not keyword:
            return self.services
            
        keyword = keyword.lower()
        return [
            service for service in self.services
            if keyword in service["name"].lower() or
               keyword in service["display_name"].lower() or
               keyword in service["description"].lower()
        ] 
        
    def backup_services(self):
        """备份当前服务配置"""
        try:
            services_config = {}
            for service in self.get_all_services():
                services_config[service['name']] = {
                    'startup_type': service['startup_type'],
                    'status': service['status']
                }
                
            with open(self.backup_file, 'w', encoding='utf-8') as f:
                json.dump(services_config, f, ensure_ascii=False, indent=4)
                
            return True, "服务配置已备份"
        except Exception as e:
            return False, f"备份服务配置失败: {str(e)}"
            
    def optimize_services(self):
        """优化服务配置"""
        try:
            # 首先备份当前配置
            success, message = self.backup_services()
            if not success:
                return False, message
                
            # 应用优化配置
            for service_name in self.optimization_config['disable']:
                try:
                    self.set_startup_type(service_name, 'disabled')
                    if self._get_service_status(win32serviceutil.QueryServiceStatus(service_name)[1]) == "运行中":
                        self.stop_service(service_name)
                except:
                    continue
                    
            for service_name in self.optimization_config['manual']:
                try:
                    self.set_startup_type(service_name, 'manual')
                except:
                    continue
                    
            for service_name in self.optimization_config['auto']:
                try:
                    self.set_startup_type(service_name, 'auto')
                    if self._get_service_status(win32serviceutil.QueryServiceStatus(service_name)[1]) != "运行中":
                        self.start_service(service_name)
                except:
                    continue
                    
            return True, "服务优化完成"
        except Exception as e:
            return False, f"服务优化失败: {str(e)}"
            
    def restore_services(self):
        """还原服务配置"""
        try:
            if not os.path.exists(self.backup_file):
                return False, "未找到备份文件"
                
            with open(self.backup_file, 'r', encoding='utf-8') as f:
                backup_config = json.load(f)
                
            for service_name, config in backup_config.items():
                try:
                    # 还原启动类型
                    startup_type = config['startup_type']
                    if startup_type == "自动":
                        self.set_startup_type(service_name, 'auto')
                    elif startup_type == "手动":
                        self.set_startup_type(service_name, 'manual')
                    elif startup_type == "禁用":
                        self.set_startup_type(service_name, 'disabled')
                        
                    # 还原运行状态
                    status = config['status']
                    if status == "运行中":
                        self.start_service(service_name)
                    elif status == "已停止":
                        self.stop_service(service_name)
                except:
                    continue
                    
            return True, "服务配置已还原"
        except Exception as e:
            return False, f"还原服务配置失败: {str(e)}" 