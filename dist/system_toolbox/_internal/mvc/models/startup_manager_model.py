import os
import winreg
from pathlib import Path

class StartupManagerModel:
    def __init__(self):
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
                    except WindowsError:
                        continue
                        
                winreg.CloseKey(key)
            except WindowsError:
                continue
                
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
            except Exception:
                continue
                
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
        
    def disable_startup_item(self, name, location):
        """禁用启动项"""
        try:
            if "HKCU" in location or "HKLM" in location:
                # 处理注册表启动项
                hive_name = location.split('\\')[0]
                reg_path = self.startup_registry_paths[hive_name]
                
                if hive_name == 'HKCU':
                    hive = winreg.HKEY_CURRENT_USER
                else:  # HKLM
                    hive = winreg.HKEY_LOCAL_MACHINE
                    
                key = winreg.OpenKey(hive, reg_path, 0, winreg.KEY_ALL_ACCESS)
                value, value_type = winreg.QueryValueEx(key, name)
                
                # 备份到禁用键
                disabled_path = reg_path + "Disabled"
                try:
                    disabled_key = winreg.CreateKey(hive, disabled_path)
                    winreg.SetValueEx(disabled_key, name, 0, value_type, value)
                    winreg.CloseKey(disabled_key)
                except WindowsError:
                    pass
                    
                # 删除原始值
                winreg.DeleteValue(key, name)
                winreg.CloseKey(key)
                
            else:
                # 处理文件夹启动项
                item_path = os.path.join(location, name)
                if os.path.exists(item_path):
                    # 创建禁用文件夹
                    disabled_folder = os.path.join(os.path.dirname(location), 'StartupDisabled')
                    if not os.path.exists(disabled_folder):
                        os.makedirs(disabled_folder)
                        
                    # 移动文件到禁用文件夹
                    disabled_path = os.path.join(disabled_folder, name)
                    os.rename(item_path, disabled_path)
                    
            return True, "启动项已禁用"
        except Exception as e:
            return False, f"禁用启动项失败: {str(e)}"
            
    def enable_startup_item(self, name, location):
        """启用启动项"""
        try:
            if "HKCU" in location or "HKLM" in location:
                # 处理注册表启动项
                hive_name = location.split('\\')[0]
                reg_path = self.startup_registry_paths[hive_name]
                disabled_path = reg_path + "Disabled"
                
                if hive_name == 'HKCU':
                    hive = winreg.HKEY_CURRENT_USER
                else:  # HKLM
                    hive = winreg.HKEY_LOCAL_MACHINE
                    
                # 从禁用键恢复
                disabled_key = winreg.OpenKey(hive, disabled_path, 0, winreg.KEY_ALL_ACCESS)
                value, value_type = winreg.QueryValueEx(disabled_key, name)
                
                key = winreg.OpenKey(hive, reg_path, 0, winreg.KEY_ALL_ACCESS)
                winreg.SetValueEx(key, name, 0, value_type, value)
                
                # 删除禁用键中的值
                winreg.DeleteValue(disabled_key, name)
                
                winreg.CloseKey(key)
                winreg.CloseKey(disabled_key)
                
            else:
                # 处理文件夹启动项
                disabled_folder = os.path.join(os.path.dirname(location), 'StartupDisabled')
                disabled_path = os.path.join(disabled_folder, name)
                
                if os.path.exists(disabled_path):
                    enabled_path = os.path.join(location, name)
                    os.rename(disabled_path, enabled_path)
                    
            return True, "启动项已启用"
        except Exception as e:
            return False, f"启用启动项失败: {str(e)}" 