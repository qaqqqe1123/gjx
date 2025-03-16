import os
import logging
import winreg
import subprocess
from pathlib import Path

class StartupManager:
    def __init__(self):
        # 设置日志
        logging.basicConfig(level=logging.INFO, 
                           format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger('StartupManager')
        
        # 启动项注册表路径
        self.startup_registry_paths = {
            'HKCU': r'Software\Microsoft\Windows\CurrentVersion\Run',
            'HKLM': r'Software\Microsoft\Windows\CurrentVersion\Run'
        }
        
        # 启动文件夹路径
        self.user_home = str(Path.home())
        self.startup_folder_paths = {
            'user': os.path.join(self.user_home, 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup'),
            'all_users': os.path.join(os.environ.get('PROGRAMDATA', 'C:\\ProgramData'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'StartUp')
        }
        
    def get_registry_startup_items(self):
        """获取注册表中的启动项"""
        items = []
        
        for hive_name, reg_path in self.startup_registry_paths.items():
            try:
                if hive_name == 'HKCU':
                    hive = winreg.HKEY_CURRENT_USER
                else:  # HKLM
                    hive = winreg.HKEY_LOCAL_MACHINE
                    
                key = winreg.OpenKey(hive, reg_path)
                
                # 获取键值数量
                count = winreg.QueryInfoKey(key)[1]
                
                for i in range(count):
                    try:
                        name, value, _ = winreg.EnumValue(key, i)
                        items.append({
                            'name': name,
                            'command': value,
                            'location': f"{hive_name}\\{reg_path}",
                            'type': 'registry',
                            'enabled': True
                        })
                    except WindowsError as e:
                        self.logger.warning(f"获取注册表启动项时出错: {e}")
                        
                winreg.CloseKey(key)
            except WindowsError as e:
                self.logger.warning(f"打开注册表键 {hive_name}\\{reg_path} 时出错: {e}")
                
        return items
        
    def get_folder_startup_items(self):
        """获取启动文件夹中的启动项"""
        items = []
        
        for location_name, folder_path in self.startup_folder_paths.items():
            try:
                if os.path.exists(folder_path):
                    for item in os.listdir(folder_path):
                        item_path = os.path.join(folder_path, item)
                        if os.path.isfile(item_path):
                            items.append({
                                'name': item,
                                'command': item_path,
                                'location': folder_path,
                                'type': 'folder',
                                'enabled': True
                            })
            except Exception as e:
                self.logger.warning(f"获取启动文件夹 {folder_path} 中的项目时出错: {e}")
                
        return items
        
    def get_all_startup_items(self):
        """获取所有启动项"""
        registry_items = self.get_registry_startup_items()
        folder_items = self.get_folder_startup_items()
        
        # 合并结果
        all_items = registry_items + folder_items
        
        # 按名称排序
        all_items.sort(key=lambda x: x['name'].lower())
        
        return all_items
        
    def disable_registry_startup_item(self, name, hive_name):
        """禁用注册表中的启动项"""
        try:
            if hive_name not in self.startup_registry_paths:
                return {
                    'success': False,
                    'error': f"无效的注册表位置: {hive_name}"
                }
                
            reg_path = self.startup_registry_paths[hive_name]
            
            if hive_name == 'HKCU':
                hive = winreg.HKEY_CURRENT_USER
            else:  # HKLM
                hive = winreg.HKEY_LOCAL_MACHINE
                
            # 打开键
            key = winreg.OpenKey(hive, reg_path, 0, winreg.KEY_ALL_ACCESS)
            
            # 获取当前值
            value, value_type = winreg.QueryValueEx(key, name)
            
            # 备份值到禁用键
            disabled_path = reg_path + "Disabled"
            try:
                disabled_key = winreg.CreateKey(hive, disabled_path)
                winreg.SetValueEx(disabled_key, name, 0, value_type, value)
                winreg.CloseKey(disabled_key)
            except WindowsError as e:
                self.logger.warning(f"创建禁用键时出错: {e}")
                
            # 删除原始值
            winreg.DeleteValue(key, name)
            winreg.CloseKey(key)
            
            self.logger.info(f"已禁用启动项: {name}")
            return {
                'success': True,
                'message': f"已禁用启动项: {name}"
            }
        except WindowsError as e:
            self.logger.error(f"禁用启动项 {name} 时出错: {e}")
            return {
                'success': False,
                'error': str(e)
            }
            
    def enable_registry_startup_item(self, name, hive_name):
        """启用注册表中的启动项"""
        try:
            if hive_name not in self.startup_registry_paths:
                return {
                    'success': False,
                    'error': f"无效的注册表位置: {hive_name}"
                }
                
            reg_path = self.startup_registry_paths[hive_name]
            disabled_path = reg_path + "Disabled"
            
            if hive_name == 'HKCU':
                hive = winreg.HKEY_CURRENT_USER
            else:  # HKLM
                hive = winreg.HKEY_LOCAL_MACHINE
                
            # 打开禁用键
            try:
                disabled_key = winreg.OpenKey(hive, disabled_path, 0, winreg.KEY_ALL_ACCESS)
                value, value_type = winreg.QueryValueEx(disabled_key, name)
                
                # 创建启用键
                key = winreg.OpenKey(hive, reg_path, 0, winreg.KEY_ALL_ACCESS)
                winreg.SetValueEx(key, name, 0, value_type, value)
                winreg.CloseKey(key)
                
                # 删除禁用值
                winreg.DeleteValue(disabled_key, name)
                winreg.CloseKey(disabled_key)
                
                self.logger.info(f"已启用启动项: {name}")
                return {
                    'success': True,
                    'message': f"已启用启动项: {name}"
                }
            except WindowsError as e:
                self.logger.error(f"启用启动项 {name} 时出错: {e}")
                return {
                    'success': False,
                    'error': str(e)
                }
        except Exception as e:
            self.logger.error(f"启用启动项 {name} 时出错: {e}")
            return {
                'success': False,
                'error': str(e)
            }
            
    def disable_folder_startup_item(self, name, location):
        """禁用启动文件夹中的启动项"""
        try:
            folder_path = self.startup_folder_paths.get(location)
            if not folder_path:
                return {
                    'success': False,
                    'error': f"无效的启动文件夹位置: {location}"
                }
                
            item_path = os.path.join(folder_path, name)
            if not os.path.exists(item_path):
                return {
                    'success': False,
                    'error': f"启动项不存在: {item_path}"
                }
                
            # 创建禁用文件夹（如果不存在）
            disabled_folder = os.path.join(os.path.dirname(folder_path), 'StartupDisabled')
            if not os.path.exists(disabled_folder):
                os.makedirs(disabled_folder)
                
            # 移动文件到禁用文件夹
            disabled_path = os.path.join(disabled_folder, name)
            os.rename(item_path, disabled_path)
            
            self.logger.info(f"已禁用启动项: {name}")
            return {
                'success': True,
                'message': f"已禁用启动项: {name}"
            }
        except Exception as e:
            self.logger.error(f"禁用启动项 {name} 时出错: {e}")
            return {
                'success': False,
                'error': str(e)
            }
            
    def enable_folder_startup_item(self, name, location):
        """启用启动文件夹中的启动项"""
        try:
            folder_path = self.startup_folder_paths.get(location)
            if not folder_path:
                return {
                    'success': False,
                    'error': f"无效的启动文件夹位置: {location}"
                }
                
            # 获取禁用文件夹路径
            disabled_folder = os.path.join(os.path.dirname(folder_path), 'StartupDisabled')
            disabled_path = os.path.join(disabled_folder, name)
            
            if not os.path.exists(disabled_path):
                return {
                    'success': False,
                    'error': f"禁用的启动项不存在: {disabled_path}"
                }
                
            # 移动文件回启动文件夹
            enabled_path = os.path.join(folder_path, name)
            os.rename(disabled_path, enabled_path)
            
            self.logger.info(f"已启用启动项: {name}")
            return {
                'success': True,
                'message': f"已启用启动项: {name}"
            }
        except Exception as e:
            self.logger.error(f"启用启动项 {name} 时出错: {e}")
            return {
                'success': False,
                'error': str(e)
            }
            
    def disable_startup_item(self, item):
        """禁用启动项"""
        if item['type'] == 'registry':
            # 从位置中提取注册表位置
            hive_name = item['location'].split('\\')[0]
            return self.disable_registry_startup_item(item['name'], hive_name)
        else:  # folder
            # 从位置中提取文件夹位置
            for location_name, path in self.startup_folder_paths.items():
                if path == item['location']:
                    return self.disable_folder_startup_item(item['name'], location_name)
                    
            return {
                'success': False,
                'error': f"无法确定启动项位置: {item['location']}"
            }
            
    def enable_startup_item(self, item):
        """启用启动项"""
        if item['type'] == 'registry':
            # 从位置中提取注册表位置
            hive_name = item['location'].split('\\')[0]
            return self.enable_registry_startup_item(item['name'], hive_name)
        else:  # folder
            # 从位置中提取文件夹位置
            for location_name, path in self.startup_folder_paths.items():
                if path == item['location']:
                    return self.enable_folder_startup_item(item['name'], location_name)
                    
            return {
                'success': False,
                'error': f"无法确定启动项位置: {item['location']}"
            }
            
    def add_registry_startup_item(self, name, command, hive_name='HKCU'):
        """添加注册表启动项"""
        try:
            if hive_name not in self.startup_registry_paths:
                return {
                    'success': False,
                    'error': f"无效的注册表位置: {hive_name}"
                }
                
            reg_path = self.startup_registry_paths[hive_name]
            
            if hive_name == 'HKCU':
                hive = winreg.HKEY_CURRENT_USER
            else:  # HKLM
                hive = winreg.HKEY_LOCAL_MACHINE
                
            # 打开键
            key = winreg.OpenKey(hive, reg_path, 0, winreg.KEY_ALL_ACCESS)
            
            # 添加值
            winreg.SetValueEx(key, name, 0, winreg.REG_SZ, command)
            winreg.CloseKey(key)
            
            self.logger.info(f"已添加启动项: {name}")
            return {
                'success': True,
                'message': f"已添加启动项: {name}"
            }
        except WindowsError as e:
            self.logger.error(f"添加启动项 {name} 时出错: {e}")
            return {
                'success': False,
                'error': str(e)
            }
            
    def delete_startup_item(self, item):
        """删除启动项"""
        try:
            if item['type'] == 'registry':
                # 从位置中提取注册表位置
                hive_name = item['location'].split('\\')[0]
                reg_path = self.startup_registry_paths[hive_name]
                
                if hive_name == 'HKCU':
                    hive = winreg.HKEY_CURRENT_USER
                else:  # HKLM
                    hive = winreg.HKEY_LOCAL_MACHINE
                    
                # 打开键
                key = winreg.OpenKey(hive, reg_path, 0, winreg.KEY_ALL_ACCESS)
                
                # 删除值
                winreg.DeleteValue(key, item['name'])
                winreg.CloseKey(key)
                
                self.logger.info(f"已删除启动项: {item['name']}")
                return {
                    'success': True,
                    'message': f"已删除启动项: {item['name']}"
                }
            else:  # folder
                item_path = os.path.join(item['location'], item['name'])
                if os.path.exists(item_path):
                    os.remove(item_path)
                    
                    self.logger.info(f"已删除启动项: {item['name']}")
                    return {
                        'success': True,
                        'message': f"已删除启动项: {item['name']}"
                    }
                else:
                    return {
                        'success': False,
                        'error': f"启动项不存在: {item_path}"
                    }
        except Exception as e:
            self.logger.error(f"删除启动项 {item['name']} 时出错: {e}")
            return {
                'success': False,
                'error': str(e)
            }
            
    def get_formatted_startup_items(self):
        """获取格式化的启动项列表"""
        items = self.get_all_startup_items()
        if not items:
            return "没有找到启动项"
            
        output = []
        output.append("启动项列表:")
        
        for i, item in enumerate(items):
            output.append(f"  {i+1}. {item['name']}")
            output.append(f"    命令: {item['command']}")
            output.append(f"    位置: {item['location']}")
            output.append(f"    类型: {item['type']}")
            output.append(f"    状态: {'启用' if item['enabled'] else '禁用'}")
            output.append("")
            
        return "\n".join(output) 