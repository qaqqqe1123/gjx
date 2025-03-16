import winreg
import datetime
import logging
import time

class RegistryCleanerModel:
    def __init__(self):
        # 设置日志
        logging.basicConfig(level=logging.INFO, 
                           format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger('RegistryCleaner')
        
        # 清理选项状态
        self.clean_options = {
            "invalid_software": True,
            "invalid_file_assoc": True,
            "invalid_startup": True,
            "invalid_uninstall": True,
            "redundant_com": True,
            "redundant_typelib": True,
            "redundant_help": True,
            "redundant_dll": True
        }
        
        # 扫描和清理结果
        self.scan_results = {}
        self.clean_results = {}
        
        # 注册表路径
        self.registry_paths = {
            "invalid_software": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            "invalid_file_assoc": r"SOFTWARE\Classes",
            "invalid_startup": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
            "invalid_uninstall": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            "redundant_com": r"SOFTWARE\Classes\CLSID",
            "redundant_typelib": r"SOFTWARE\Classes\TypeLib",
            "redundant_help": r"SOFTWARE\Microsoft\Windows\Help",
            "redundant_dll": r"SOFTWARE\Microsoft\Windows\CurrentVersion\SharedDLLs"
        }
        
    def toggle_option(self, option_key):
        """切换清理选项状态"""
        if option_key in self.clean_options:
            self.clean_options[option_key] = not self.clean_options[option_key]
            return True
        return False
        
    def select_all_options(self):
        """选择所有清理选项"""
        for key in self.clean_options:
            self.clean_options[key] = True
            
    def deselect_all_options(self):
        """取消选择所有清理选项"""
        for key in self.clean_options:
            self.clean_options[key] = False
            
    def scan_registry(self):
        """扫描注册表"""
        self.logger.info("开始扫描注册表")
        results = {
            'invalid': {},
            'redundant': {},
            'total_count': 0
        }
        
        # 扫描无效项
        if any(self.clean_options[key] for key in ["invalid_software", "invalid_file_assoc", "invalid_startup", "invalid_uninstall"]):
            invalid_results = self._scan_invalid_entries()
            results['invalid'] = invalid_results
            
        # 扫描冗余项
        if any(self.clean_options[key] for key in ["redundant_com", "redundant_typelib", "redundant_help", "redundant_dll"]):
            redundant_results = self._scan_redundant_entries()
            results['redundant'] = redundant_results
            
        # 计算总数
        invalid_count = sum(len(entries) for entries in results['invalid'].values())
        redundant_count = sum(len(entries) for entries in results['redundant'].values())
        results['total_count'] = invalid_count + redundant_count
        
        self.scan_results = results
        self.logger.info(f"注册表扫描完成，发现 {results['total_count']} 个问题项")
        return results
        
    def _scan_invalid_entries(self):
        """扫描无效的注册表项"""
        results = {}
        
        # 模拟扫描结果
        if self.clean_options["invalid_software"]:
            results["invalid_software"] = self._scan_invalid_software()
            
        if self.clean_options["invalid_file_assoc"]:
            results["invalid_file_assoc"] = self._scan_invalid_file_assoc()
            
        if self.clean_options["invalid_startup"]:
            results["invalid_startup"] = self._scan_invalid_startup()
            
        if self.clean_options["invalid_uninstall"]:
            results["invalid_uninstall"] = self._scan_invalid_uninstall()
            
        # 计算总数和总大小
        total_count = sum(len(entries) for entries in results.values())
        
        results['total'] = {
            'count': total_count,
            'size': 0  # 这里需要根据实际扫描结果计算
        }
        
        return results
        
    def _scan_redundant_entries(self):
        """扫描冗余的注册表项"""
        results = {}
        
        # 模拟扫描结果
        if self.clean_options["redundant_com"]:
            results["redundant_com"] = self._scan_redundant_com()
            
        if self.clean_options["redundant_typelib"]:
            results["redundant_typelib"] = self._scan_redundant_typelib()
            
        if self.clean_options["redundant_help"]:
            results["redundant_help"] = self._scan_redundant_help()
            
        if self.clean_options["redundant_dll"]:
            results["redundant_dll"] = self._scan_redundant_dll()
            
        # 计算总数和总大小
        total_count = sum(len(entries) for entries in results.values())
        
        results['total'] = {
            'count': total_count,
            'size': 0  # 这里需要根据实际扫描结果计算
        }
        
        return results
        
    def clean_registry(self):
        """清理注册表中的无效项和冗余项"""
        if not self.scan_results:
            self.logger.warning("尚未进行扫描，无法进行清理")
            return {"success": False, "error": "尚未进行扫描"}
            
        self.logger.info("开始清理注册表")
        results = {
            "invalid": {},
            "redundant": {}
        }
        
        # 清理无效项
        if "invalid" in self.scan_results and self.scan_results["invalid"]:
            results["invalid"] = self._clean_invalid_entries()
            
        # 清理冗余项
        if "redundant" in self.scan_results and self.scan_results["redundant"]:
            results["redundant"] = self._clean_redundant_entries()
            
        # 计算总数
        invalid_cleaned = sum(result["cleaned"] for result in results["invalid"].values())
        invalid_failed = sum(result["failed"] for result in results["invalid"].values())
        redundant_cleaned = sum(result["cleaned"] for result in results["redundant"].values())
        redundant_failed = sum(result["failed"] for result in results["redundant"].values())
        
        results["total_cleaned"] = invalid_cleaned + redundant_cleaned
        results["total_failed"] = invalid_failed + redundant_failed
        
        self.clean_results = results
        self.logger.info(f"注册表清理完成，已清理 {results['total_cleaned']} 个项目，失败 {results['total_failed']} 个")
        return results
        
    def _clean_invalid_entries(self):
        """清理无效的注册表项"""
        results = {
            "invalid_software": {"cleaned": 0, "failed": 0},
            "invalid_file_assoc": {"cleaned": 0, "failed": 0},
            "invalid_startup": {"cleaned": 0, "failed": 0},
            "invalid_uninstall": {"cleaned": 0, "failed": 0}
        }
        
        if "invalid" not in self.scan_results:
            return results
            
        invalid_entries = self.scan_results["invalid"]
        
        try:
            # 清理无效的软件项
            if self.clean_options["invalid_software"] and "invalid_software" in invalid_entries:
                results["invalid_software"] = self._clean_registry_keys(invalid_entries["invalid_software"])
                
            # 清理无效的文件关联
            if self.clean_options["invalid_file_assoc"] and "invalid_file_assoc" in invalid_entries:
                results["invalid_file_assoc"] = self._clean_registry_keys(invalid_entries["invalid_file_assoc"])
                
            # 清理无效的启动项
            if self.clean_options["invalid_startup"] and "invalid_startup" in invalid_entries:
                results["invalid_startup"] = self._clean_registry_keys(invalid_entries["invalid_startup"])
                
            # 清理无效的卸载信息
            if self.clean_options["invalid_uninstall"] and "invalid_uninstall" in invalid_entries:
                results["invalid_uninstall"] = self._clean_registry_keys(invalid_entries["invalid_uninstall"])
        except Exception as e:
            self.logger.error(f"清理无效注册表项时出错: {str(e)}")
            
        return results
        
    def _clean_redundant_entries(self):
        """清理冗余的注册表项"""
        results = {
            "redundant_com": {"cleaned": 0, "failed": 0},
            "redundant_typelib": {"cleaned": 0, "failed": 0},
            "redundant_help": {"cleaned": 0, "failed": 0},
            "redundant_dll": {"cleaned": 0, "failed": 0}
        }
        
        if "redundant" not in self.scan_results:
            return results
            
        redundant_entries = self.scan_results["redundant"]
        
        try:
            # 清理冗余的COM组件
            if self.clean_options["redundant_com"] and "redundant_com" in redundant_entries:
                results["redundant_com"] = self._clean_registry_keys(redundant_entries["redundant_com"])
                
            # 清理冗余的类型库
            if self.clean_options["redundant_typelib"] and "redundant_typelib" in redundant_entries:
                results["redundant_typelib"] = self._clean_registry_keys(redundant_entries["redundant_typelib"])
                
            # 清理冗余的帮助文件
            if self.clean_options["redundant_help"] and "redundant_help" in redundant_entries:
                results["redundant_help"] = self._clean_registry_keys(redundant_entries["redundant_help"])
                
            # 清理冗余的共享DLL
            if self.clean_options["redundant_dll"] and "redundant_dll" in redundant_entries:
                results["redundant_dll"] = self._clean_registry_keys(redundant_entries["redundant_dll"])
        except Exception as e:
            self.logger.error(f"清理冗余注册表项时出错: {str(e)}")
            
        return results
        
    def backup_registry(self):
        """备份注册表"""
        try:
            import subprocess
            import os
            from datetime import datetime
            
            # 创建备份文件夹
            backup_dir = os.path.join(os.environ["USERPROFILE"], "Documents", "RegistryBackups")
            os.makedirs(backup_dir, exist_ok=True)
            
            # 创建备份文件名
            backup_file = os.path.join(backup_dir, f"registry_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.reg")
            
            # 导出注册表
            subprocess.run(["reg", "export", "HKLM", backup_file, "/y"], check=True, capture_output=True)
            
            self.logger.info(f"注册表已备份到 {backup_file}")
            return {"success": True, "file": backup_file}
        except Exception as e:
            self.logger.error(f"注册表备份失败: {str(e)}")
            return {"success": False, "error": str(e)}
        
    def _clean_registry_keys(self, keys):
        """清理注册表键"""
        result = {"cleaned": 0, "failed": 0}
        
        # 模拟清理过程（示例）
        # 在实际实现中，应该使用winreg库删除注册表键
        for key in keys:
            try:
                # 模拟成功率约为90%
                import random
                if random.random() < 0.9:
                    # 在实际实现中：
                    # key_path = key["key"]
                    # root_key, sub_key = self._parse_reg_path(key_path)
                    # winreg.DeleteKey(root_key, sub_key)
                    result["cleaned"] += 1
                    self.logger.info(f"已清理注册表项: {key['key']}")
                else:
                    result["failed"] += 1
                    self.logger.warning(f"清理注册表项失败: {key['key']}")
            except Exception as e:
                result["failed"] += 1
                self.logger.error(f"清理注册表项出错: {key['key']}, 错误: {str(e)}")
                
        return result
        
    def _parse_reg_path(self, reg_path):
        """解析注册表路径，返回根键和子键"""
        parts = reg_path.split("\\", 1)
        if len(parts) < 2:
            raise ValueError(f"无效的注册表路径: {reg_path}")
            
        root_key_str = parts[0].upper()
        sub_key = parts[1] if len(parts) > 1 else ""
        
        root_key_map = {
            "HKCR": winreg.HKEY_CLASSES_ROOT,
            "HKEY_CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
            "HKCU": winreg.HKEY_CURRENT_USER,
            "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
            "HKLM": winreg.HKEY_LOCAL_MACHINE,
            "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
            "HKU": winreg.HKEY_USERS,
            "HKEY_USERS": winreg.HKEY_USERS,
            "HKCC": winreg.HKEY_CURRENT_CONFIG,
            "HKEY_CURRENT_CONFIG": winreg.HKEY_CURRENT_CONFIG
        }
        
        if root_key_str not in root_key_map:
            raise ValueError(f"无效的注册表根键: {root_key_str}")
            
        return root_key_map[root_key_str], sub_key
        
    def format_size(self, size_bytes):
        """将字节大小格式化为人类可读的格式"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
        
    def _scan_invalid_software(self):
        """扫描无效的软件项"""
        invalid_entries = []
        
        # 模拟扫描结果（示例）
        # 在实际实现中，应该遍历注册表并检查软件路径是否存在
        # 如果路径不存在，则添加到无效列表中
        invalid_entries = [
            {"key": "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\旧软件.exe", "type": "无效路径", "detail": "路径不存在: C:\\Program Files\\旧软件\\app.exe"},
            {"key": "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\未安装应用.exe", "type": "无效路径", "detail": "路径不存在: D:\\已删除\\app.exe"},
            {"key": "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\老游戏.exe", "type": "无效路径", "detail": "路径不存在: E:\\Games\\已卸载\\game.exe"}
        ]
        
        return invalid_entries
    
    def _scan_invalid_file_assoc(self):
        """扫描无效的文件关联"""
        invalid_entries = []
        
        # 模拟扫描结果（示例）
        invalid_entries = [
            {"key": "HKCR\\.oldext", "type": "无效扩展名", "detail": "关联的程序不存在"},
            {"key": "HKCR\\Applications\\旧应用.exe", "type": "无效应用", "detail": "应用程序不存在"}
        ]
        
        return invalid_entries
    
    def _scan_invalid_startup(self):
        """扫描无效的启动项"""
        invalid_entries = []
        
        # 模拟扫描结果（示例）
        invalid_entries = [
            {"key": "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run\\旧启动项", "type": "无效路径", "detail": "路径不存在: C:\\旧程序\\startup.exe"},
            {"key": "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run\\已卸载程序", "type": "无效路径", "detail": "路径不存在: D:\\已删除\\autorun.exe"}
        ]
        
        return invalid_entries
    
    def _scan_invalid_uninstall(self):
        """扫描无效的卸载信息"""
        invalid_entries = []
        
        # 模拟扫描结果（示例）
        invalid_entries = [
            {"key": "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\旧软件", "type": "无效卸载", "detail": "卸载程序不存在"},
            {"key": "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{GUID-123}", "type": "无效卸载", "detail": "未找到安装目录"}
        ]
        
        return invalid_entries
    
    def _scan_redundant_com(self):
        """扫描冗余的COM组件"""
        redundant_entries = []
        
        # 模拟扫描结果（示例）
        redundant_entries = [
            {"key": "HKCR\\CLSID\\{旧GUID-1}", "type": "冗余COM", "detail": "未被引用的组件"},
            {"key": "HKCR\\CLSID\\{旧GUID-2}", "type": "冗余COM", "detail": "未被引用的组件"}
        ]
        
        return redundant_entries
    
    def _scan_redundant_typelib(self):
        """扫描冗余的类型库"""
        redundant_entries = []
        
        # 模拟扫描结果（示例）
        redundant_entries = [
            {"key": "HKCR\\TypeLib\\{旧类型库-1}", "type": "冗余类型库", "detail": "未被引用的类型库"},
            {"key": "HKCR\\TypeLib\\{旧类型库-2}", "type": "冗余类型库", "detail": "未被引用的类型库"}
        ]
        
        return redundant_entries
    
    def _scan_redundant_help(self):
        """扫描冗余的帮助文件"""
        redundant_entries = []
        
        # 模拟扫描结果（示例）
        redundant_entries = [
            {"key": "HKLM\\SOFTWARE\\Microsoft\\Windows\\Help\\旧帮助文件", "type": "冗余帮助", "detail": "帮助文件不存在"},
            {"key": "HKLM\\SOFTWARE\\Microsoft\\Windows\\Help\\旧文档", "type": "冗余帮助", "detail": "帮助文件不存在"}
        ]
        
        return redundant_entries
    
    def _scan_redundant_dll(self):
        """扫描冗余的共享DLL"""
        redundant_entries = []
        
        # 模拟扫描结果（示例）
        redundant_entries = [
            {"key": "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\SharedDLLs\\C:\\Windows\\System32\\旧DLL.dll", "type": "冗余DLL", "detail": "DLL文件不存在"},
            {"key": "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\SharedDLLs\\C:\\Program Files\\Common Files\\旧共享DLL.dll", "type": "冗余DLL", "detail": "DLL文件不存在"}
        ]
        
        return redundant_entries
        
    def get_formatted_scan_results(self):
        """获取格式化的扫描结果"""
        if not self.scan_results:
            return "尚未进行扫描"
            
        output = []
        
        # 添加标题框架
        scan_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        output.append("╔═══════════════════════════════════════════════╗")
        output.append("║             注册表扫描结果报告                ║")
        output.append("╠═══════════════════════════════════════════════╣")
        output.append(f"║ 扫描时间: {scan_time}              ║")
        output.append("╠═══════════════════════════════════════════════╣")
        
        # 无效项结果
        if "invalid" in self.scan_results and any(self.scan_results["invalid"].values()):
            invalid_entries = self.scan_results["invalid"]
            output.append("║ 【无效项】                                  ║")
            
            if "invalid_software" in invalid_entries and invalid_entries["invalid_software"]:
                output.append(f"║ ✓ 无效的软件项: {len(invalid_entries['invalid_software'])} 个")
                for entry in invalid_entries["invalid_software"][:3]:  # 只显示前3个
                    output.append(f"║ ● {entry['detail'][:40]}")
                if len(invalid_entries["invalid_software"]) > 3:
                    output.append(f"║ ● ... 等 {len(invalid_entries['invalid_software']) - 3} 个项目")
            
            if "invalid_file_assoc" in invalid_entries and invalid_entries["invalid_file_assoc"]:
                output.append(f"║ ✓ 无效的文件关联: {len(invalid_entries['invalid_file_assoc'])} 个")
                for entry in invalid_entries["invalid_file_assoc"][:3]:  # 只显示前3个
                    output.append(f"║ ● {entry['detail'][:40]}")
                if len(invalid_entries["invalid_file_assoc"]) > 3:
                    output.append(f"║ ● ... 等 {len(invalid_entries['invalid_file_assoc']) - 3} 个项目")
            
            if "invalid_startup" in invalid_entries and invalid_entries["invalid_startup"]:
                output.append(f"║ ✓ 无效的启动项: {len(invalid_entries['invalid_startup'])} 个")
                for entry in invalid_entries["invalid_startup"][:3]:  # 只显示前3个
                    output.append(f"║ ● {entry['detail'][:40]}")
                if len(invalid_entries["invalid_startup"]) > 3:
                    output.append(f"║ ● ... 等 {len(invalid_entries['invalid_startup']) - 3} 个项目")
            
            if "invalid_uninstall" in invalid_entries and invalid_entries["invalid_uninstall"]:
                output.append(f"║ ✓ 无效的卸载信息: {len(invalid_entries['invalid_uninstall'])} 个")
                for entry in invalid_entries["invalid_uninstall"][:3]:  # 只显示前3个
                    output.append(f"║ ● {entry['detail'][:40]}")
                if len(invalid_entries["invalid_uninstall"]) > 3:
                    output.append(f"║ ● ... 等 {len(invalid_entries['invalid_uninstall']) - 3} 个项目")
                
            output.append("╠═══════════════════════════════════════════════╣")
        
        # 冗余项结果
        if "redundant" in self.scan_results and any(self.scan_results["redundant"].values()):
            redundant_entries = self.scan_results["redundant"]
            output.append("║ 【冗余项】                                  ║")
            
            if "redundant_com" in redundant_entries and redundant_entries["redundant_com"]:
                output.append(f"║ ✓ 冗余的COM组件: {len(redundant_entries['redundant_com'])} 个")
                for entry in redundant_entries["redundant_com"][:3]:  # 只显示前3个
                    output.append(f"║ ● {entry['detail'][:40]}")
                if len(redundant_entries["redundant_com"]) > 3:
                    output.append(f"║ ● ... 等 {len(redundant_entries['redundant_com']) - 3} 个项目")
            
            if "redundant_typelib" in redundant_entries and redundant_entries["redundant_typelib"]:
                output.append(f"║ ✓ 冗余的类型库: {len(redundant_entries['redundant_typelib'])} 个")
                for entry in redundant_entries["redundant_typelib"][:3]:  # 只显示前3个
                    output.append(f"║ ● {entry['detail'][:40]}")
                if len(redundant_entries["redundant_typelib"]) > 3:
                    output.append(f"║ ● ... 等 {len(redundant_entries['redundant_typelib']) - 3} 个项目")
            
            if "redundant_help" in redundant_entries and redundant_entries["redundant_help"]:
                output.append(f"║ ✓ 冗余的帮助文件: {len(redundant_entries['redundant_help'])} 个")
                for entry in redundant_entries["redundant_help"][:3]:  # 只显示前3个
                    output.append(f"║ ● {entry['detail'][:40]}")
                if len(redundant_entries["redundant_help"]) > 3:
                    output.append(f"║ ● ... 等 {len(redundant_entries['redundant_help']) - 3} 个项目")
            
            if "redundant_dll" in redundant_entries and redundant_entries["redundant_dll"]:
                output.append(f"║ ✓ 冗余的共享DLL: {len(redundant_entries['redundant_dll'])} 个")
                for entry in redundant_entries["redundant_dll"][:3]:  # 只显示前3个
                    output.append(f"║ ● {entry['detail'][:40]}")
                if len(redundant_entries["redundant_dll"]) > 3:
                    output.append(f"║ ● ... 等 {len(redundant_entries['redundant_dll']) - 3} 个项目")
                
            output.append("╠═══════════════════════════════════════════════╣")
            
        # 总计
        output.append(f"║ 总计问题项: {self.scan_results.get('total_count', 0)} 个                        ║")
        
        # 添加底部框架
        output.append("╚═══════════════════════════════════════════════╝")
        
        return "\n".join(output)
        
    def get_formatted_clean_results(self):
        """获取格式化的清理结果"""
        if not self.clean_results:
            return "尚未进行清理"
            
        output = []
        
        # 添加标题框架
        clean_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        output.append("╔═══════════════════════════════════════════════╗")
        output.append("║             注册表清理结果报告                ║")
        output.append("╠═══════════════════════════════════════════════╣")
        output.append(f"║ 清理时间: {clean_time}              ║")
        output.append("╠═══════════════════════════════════════════════╣")
        
        # 无效项清理结果
        if "invalid" in self.clean_results and any(result["cleaned"] > 0 for result in self.clean_results["invalid"].values()):
            invalid_results = self.clean_results["invalid"]
            output.append("║ 【无效项】                                  ║")
            
            if "invalid_software" in invalid_results:
                result = invalid_results["invalid_software"]
                if result["cleaned"] > 0:
                    output.append(f"║ ✓ 已清理无效软件项: {result['cleaned']} 个")
                if result["failed"] > 0:
                    output.append(f"║ ✗ 清理失败: {result['failed']} 个")
            
            if "invalid_file_assoc" in invalid_results:
                result = invalid_results["invalid_file_assoc"]
                if result["cleaned"] > 0:
                    output.append(f"║ ✓ 已清理无效文件关联: {result['cleaned']} 个")
                if result["failed"] > 0:
                    output.append(f"║ ✗ 清理失败: {result['failed']} 个")
            
            if "invalid_startup" in invalid_results:
                result = invalid_results["invalid_startup"]
                if result["cleaned"] > 0:
                    output.append(f"║ ✓ 已清理无效启动项: {result['cleaned']} 个")
                if result["failed"] > 0:
                    output.append(f"║ ✗ 清理失败: {result['failed']} 个")
            
            if "invalid_uninstall" in invalid_results:
                result = invalid_results["invalid_uninstall"]
                if result["cleaned"] > 0:
                    output.append(f"║ ✓ 已清理无效卸载信息: {result['cleaned']} 个")
                if result["failed"] > 0:
                    output.append(f"║ ✗ 清理失败: {result['failed']} 个")
                
            output.append("╠═══════════════════════════════════════════════╣")
        
        # 冗余项清理结果
        if "redundant" in self.clean_results and any(result["cleaned"] > 0 for result in self.clean_results["redundant"].values()):
            redundant_results = self.clean_results["redundant"]
            output.append("║ 【冗余项】                                  ║")
            
            if "redundant_com" in redundant_results:
                result = redundant_results["redundant_com"]
                if result["cleaned"] > 0:
                    output.append(f"║ ✓ 已清理冗余COM组件: {result['cleaned']} 个")
                if result["failed"] > 0:
                    output.append(f"║ ✗ 清理失败: {result['failed']} 个")
            
            if "redundant_typelib" in redundant_results:
                result = redundant_results["redundant_typelib"]
                if result["cleaned"] > 0:
                    output.append(f"║ ✓ 已清理冗余类型库: {result['cleaned']} 个")
                if result["failed"] > 0:
                    output.append(f"║ ✗ 清理失败: {result['failed']} 个")
            
            if "redundant_help" in redundant_results:
                result = redundant_results["redundant_help"]
                if result["cleaned"] > 0:
                    output.append(f"║ ✓ 已清理冗余帮助文件: {result['cleaned']} 个")
                if result["failed"] > 0:
                    output.append(f"║ ✗ 清理失败: {result['failed']} 个")
            
            if "redundant_dll" in redundant_results:
                result = redundant_results["redundant_dll"]
                if result["cleaned"] > 0:
                    output.append(f"║ ✓ 已清理冗余共享DLL: {result['cleaned']} 个")
                if result["failed"] > 0:
                    output.append(f"║ ✗ 清理失败: {result['failed']} 个")
                
            output.append("╠═══════════════════════════════════════════════╣")
            
        # 总计
        total_cleaned = self.clean_results.get("total_cleaned", 0)
        total_failed = self.clean_results.get("total_failed", 0)
        output.append(f"║ 总计已清理: {total_cleaned} 个项目                     ║")
        if total_failed > 0:
            output.append(f"║ 总计清理失败: {total_failed} 个项目                   ║")
        
        # 添加底部框架
        output.append("╚═══════════════════════════════════════════════╝")
        
        return "\n".join(output)
        
    def get_formatted_backup_results(self, backup_result):
        """获取格式化的备份结果
        
        Args:
            backup_result: 备份结果字典，包含success和file或error字段
            
        Returns:
            str: 格式化的备份结果
        """
        if not backup_result:
            return "备份失败"
            
        output = []
        
        # 添加标题框架
        backup_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        output.append("╔═══════════════════════════════════════════════╗")
        output.append("║             注册表备份结果报告                ║")
        output.append("╠═══════════════════════════════════════════════╣")
        output.append(f"║ 备份时间: {backup_time}              ║")
        output.append("╠═══════════════════════════════════════════════╣")
        
        # 备份结果
        if backup_result.get("success", False):
            output.append("║ 【备份状态】                                ║")
            output.append("║ ✓ 备份成功                                 ║")
            output.append(f"║ ● 备份文件: {os.path.basename(backup_result['file'])} ║")
            output.append(f"║ ● 存储位置: {os.path.dirname(backup_result['file'])} ║")
            output.append("╠═══════════════════════════════════════════════╣")
            output.append("║ 【温馨提示】                                ║")
            output.append("║ ● 备份文件可用于在系统出现问题时还原注册表  ║")
            output.append("║ ● 还原方法：双击备份文件或使用regedit导入   ║")
        else:
            output.append("║ 【备份状态】                                ║")
            output.append("║ ✗ 备份失败                                 ║")
            output.append(f"║ ● 错误信息: {backup_result.get('error', '未知错误')[:30]} ║")
            output.append("╠═══════════════════════════════════════════════╣")
            output.append("║ 【故障排查】                                ║")
            output.append("║ ● 请确保您有足够的磁盘空间                  ║")
            output.append("║ ● 请确保您有管理员权限                      ║")
            output.append("║ ● 请尝试重新运行备份                        ║")
        
        # 添加底部框架
        output.append("╚═══════════════════════════════════════════════╝")
        
        return "\n".join(output) 