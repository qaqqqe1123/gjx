import os
import logging
import subprocess
import winreg
import ctypes
import psutil

class SystemOptimizer:
    def __init__(self):
        # 设置日志
        logging.basicConfig(level=logging.INFO, 
                           format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger('SystemOptimizer')
        
        # 定义优化项
        self.optimization_options = {
            'visual_effects': '优化视觉效果',
            'startup_items': '优化启动项',
            'services': '优化系统服务',
            'disk_cleanup': '磁盘清理',
            'defrag': '磁盘碎片整理',
            'power_plan': '电源计划优化'
        }
        
    def is_admin(self):
        """检查是否具有管理员权限"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False
            
    def optimize_visual_effects(self):
        """优化视觉效果设置"""
        try:
            if not self.is_admin():
                return {
                    'success': False,
                    'error': '需要管理员权限'
                }
                
            # 打开性能选项注册表项
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects"
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)
                # 设置为"调整为最佳性能"
                winreg.SetValueEx(key, "VisualFXSetting", 0, winreg.REG_DWORD, 2)
                winreg.CloseKey(key)
                
                self.logger.info("视觉效果已优化为最佳性能")
                return {
                    'success': True,
                    'message': '视觉效果已优化为最佳性能'
                }
            except Exception as e:
                self.logger.error(f"优化视觉效果时出错: {e}")
                return {
                    'success': False,
                    'error': str(e)
                }
        except Exception as e:
            self.logger.error(f"优化视觉效果时出错: {e}")
            return {
                'success': False,
                'error': str(e)
            }
            
    def optimize_power_plan(self, plan='high_performance'):
        """优化电源计划"""
        try:
            if not self.is_admin():
                return {
                    'success': False,
                    'error': '需要管理员权限'
                }
                
            # 电源计划GUID
            power_plans = {
                'balanced': '381b4222-f694-41f0-9685-ff5bb260df2e',
                'high_performance': '8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c',
                'power_saver': 'a1841308-3541-4fab-bc81-f71556f20b4a'
            }
            
            if plan not in power_plans:
                return {
                    'success': False,
                    'error': f'不支持的电源计划: {plan}'
                }
                
            # 设置电源计划
            guid = power_plans[plan]
            result = subprocess.run(['powercfg', '/S', guid], 
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            if result.returncode == 0:
                self.logger.info(f"电源计划已设置为: {plan}")
                return {
                    'success': True,
                    'message': f'电源计划已设置为: {plan}'
                }
            else:
                error = result.stderr.decode('gbk', errors='ignore')
                self.logger.error(f"设置电源计划时出错: {error}")
                return {
                    'success': False,
                    'error': error
                }
        except Exception as e:
            self.logger.error(f"优化电源计划时出错: {e}")
            return {
                'success': False,
                'error': str(e)
            }
            
    def run_disk_cleanup(self, drive='C:'):
        """运行磁盘清理"""
        try:
            # 运行磁盘清理
            result = subprocess.run(['cleanmgr', '/sagerun:1', '/d', drive], 
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            if result.returncode == 0:
                self.logger.info(f"磁盘清理已启动，请等待系统完成清理")
                return {
                    'success': True,
                    'message': f'磁盘清理已启动，请等待系统完成清理'
                }
            else:
                error = result.stderr.decode('gbk', errors='ignore')
                self.logger.error(f"运行磁盘清理时出错: {error}")
                return {
                    'success': False,
                    'error': error
                }
        except Exception as e:
            self.logger.error(f"运行磁盘清理时出错: {e}")
            return {
                'success': False,
                'error': str(e)
            }
            
    def run_defrag(self, drive='C:'):
        """运行磁盘碎片整理"""
        try:
            if not self.is_admin():
                return {
                    'success': False,
                    'error': '需要管理员权限'
                }
                
            # 运行磁盘碎片整理
            result = subprocess.run(['defrag', drive, '/U', '/V'], 
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            if result.returncode == 0:
                output = result.stdout.decode('gbk', errors='ignore')
                self.logger.info(f"磁盘碎片整理已完成: {output}")
                return {
                    'success': True,
                    'message': f'磁盘碎片整理已完成',
                    'details': output
                }
            else:
                error = result.stderr.decode('gbk', errors='ignore')
                self.logger.error(f"运行磁盘碎片整理时出错: {error}")
                return {
                    'success': False,
                    'error': error
                }
        except Exception as e:
            self.logger.error(f"运行磁盘碎片整理时出错: {e}")
            return {
                'success': False,
                'error': str(e)
            }
            
    def disable_unnecessary_services(self):
        """禁用不必要的服务"""
        try:
            if not self.is_admin():
                return {
                    'success': False,
                    'error': '需要管理员权限'
                }
                
            # 可以禁用的服务列表（谨慎选择）
            services_to_disable = [
                'DiagTrack',  # Connected User Experiences and Telemetry
                'dmwappushservice',  # WAP Push Message Routing Service
                'MapsBroker',  # Downloaded Maps Manager
                'lfsvc',  # Geolocation Service
                'XblAuthManager',  # Xbox Live Auth Manager
                'XblGameSave',  # Xbox Live Game Save
                'XboxNetApiSvc',  # Xbox Live Networking Service
                'WSearch'  # Windows Search
            ]
            
            results = {}
            for service in services_to_disable:
                try:
                    result = subprocess.run(['sc', 'config', service, 'start=', 'disabled'], 
                                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    
                    if result.returncode == 0:
                        self.logger.info(f"服务 {service} 已禁用")
                        results[service] = True
                    else:
                        error = result.stderr.decode('gbk', errors='ignore')
                        self.logger.error(f"禁用服务 {service} 时出错: {error}")
                        results[service] = False
                except Exception as e:
                    self.logger.error(f"禁用服务 {service} 时出错: {e}")
                    results[service] = False
                    
            return {
                'success': True,
                'results': results
            }
        except Exception as e:
            self.logger.error(f"禁用不必要的服务时出错: {e}")
            return {
                'success': False,
                'error': str(e)
            }
            
    def get_system_info(self):
        """获取系统信息"""
        try:
            info = {}
            
            # CPU信息
            info['cpu'] = {
                'usage': psutil.cpu_percent(interval=1),
                'cores': psutil.cpu_count(logical=False),
                'logical_cores': psutil.cpu_count(logical=True)
            }
            
            # 内存信息
            memory = psutil.virtual_memory()
            info['memory'] = {
                'total': memory.total,
                'available': memory.available,
                'used': memory.used,
                'percent': memory.percent
            }
            
            # 磁盘信息
            info['disks'] = []
            for partition in psutil.disk_partitions():
                if os.name == 'nt' and ('cdrom' in partition.opts or partition.fstype == ''):
                    # 跳过CD-ROM驱动器
                    continue
                    
                usage = psutil.disk_usage(partition.mountpoint)
                info['disks'].append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent
                })
                
            # 网络信息
            info['network'] = psutil.net_io_counters()
            
            return info
        except Exception as e:
            self.logger.error(f"获取系统信息时出错: {e}")
            return {}
            
    def format_size(self, size_bytes):
        """将字节大小格式化为人类可读的格式"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
        
    def get_formatted_system_info(self):
        """获取格式化的系统信息"""
        info = self.get_system_info()
        if not info:
            return "无法获取系统信息"
            
        output = []
        
        # CPU信息
        output.append("CPU信息:")
        output.append(f"  使用率: {info['cpu']['usage']}%")
        output.append(f"  物理核心数: {info['cpu']['cores']}")
        output.append(f"  逻辑核心数: {info['cpu']['logical_cores']}")
        output.append("")
        
        # 内存信息
        output.append("内存信息:")
        output.append(f"  总内存: {self.format_size(info['memory']['total'])}")
        output.append(f"  可用内存: {self.format_size(info['memory']['available'])}")
        output.append(f"  已用内存: {self.format_size(info['memory']['used'])}")
        output.append(f"  内存使用率: {info['memory']['percent']}%")
        output.append("")
        
        # 磁盘信息
        output.append("磁盘信息:")
        for disk in info['disks']:
            output.append(f"  {disk['device']} ({disk['mountpoint']}):")
            output.append(f"    文件系统: {disk['fstype']}")
            output.append(f"    总容量: {self.format_size(disk['total'])}")
            output.append(f"    已用空间: {self.format_size(disk['used'])}")
            output.append(f"    可用空间: {self.format_size(disk['free'])}")
            output.append(f"    使用率: {disk['percent']}%")
            output.append("")
            
        # 网络信息
        output.append("网络信息:")
        output.append(f"  发送: {self.format_size(info['network'].bytes_sent)}")
        output.append(f"  接收: {self.format_size(info['network'].bytes_recv)}")
        
        return "\n".join(output) 