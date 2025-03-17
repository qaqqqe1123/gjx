from modules.temp_cleaner import TempCleaner
from modules.recycle_bin import RecycleBinCleaner
from modules.browser_cache import BrowserCacheCleaner
import os
import time

class SystemCleanerModel:
    def __init__(self):
        # 初始化清理模块
        self.temp_cleaner = TempCleaner()
        self.recycle_bin_cleaner = RecycleBinCleaner()
        self.browser_cache_cleaner = BrowserCacheCleaner()
        
        # 清理选项状态
        self.clean_options = {
            "windows_temp": True,
            "user_temp": True,
            "prefetch": True,
            "recent_docs": False,
            "recycle_bin": True,
            "chrome": True,
            "edge": True,
            "firefox": False,
            "opera": False
        }
        
        # 扫描和清理结果
        self.scan_results = {}
        self.clean_results = {}
        
        # 安全路径列表 - 这些路径不会被清理
        self.safe_paths = [
            os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'System32'),
            os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'SysWOW64'),
            os.path.join(os.environ.get('ProgramFiles', 'C:\\Program Files')),
            os.path.join(os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)')),
            os.path.join(os.environ.get('USERPROFILE', ''), 'Documents'),
            os.path.join(os.environ.get('USERPROFILE', ''), 'Pictures'),
            os.path.join(os.environ.get('USERPROFILE', ''), 'Videos'),
            os.path.join(os.environ.get('USERPROFILE', ''), 'Music'),
            os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop')
        ]
        
        # 排除的文件类型 - 这些类型的文件不会被清理
        self.excluded_extensions = [
            '.exe', '.dll', '.sys', '.ini', '.dat', '.key',
            '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.pdf',
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.mp3', '.mp4', '.avi', '.mov'
        ]
        
        # 最大文件年龄（天）- 超过这个时间的临时文件才会被清理
        self.max_file_age_days = 7
        
        # 是否启用安全模式
        self.safe_mode = True
        
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
            
    def toggle_safe_mode(self):
        """切换安全模式"""
        self.safe_mode = not self.safe_mode
        return self.safe_mode
        
    def set_max_file_age(self, days):
        """设置最大文件年龄"""
        if days > 0:
            self.max_file_age_days = days
            return True
        return False
        
    def add_safe_path(self, path):
        """添加安全路径"""
        if os.path.exists(path) and path not in self.safe_paths:
            self.safe_paths.append(path)
            return True
        return False
        
    def remove_safe_path(self, path):
        """移除安全路径"""
        if path in self.safe_paths:
            self.safe_paths.remove(path)
            return True
        return False
        
    def add_excluded_extension(self, extension):
        """添加排除的文件类型"""
        if extension.startswith('.') and extension not in self.excluded_extensions:
            self.excluded_extensions.append(extension)
            return True
        return False
        
    def remove_excluded_extension(self, extension):
        """移除排除的文件类型"""
        if extension in self.excluded_extensions:
            self.excluded_extensions.remove(extension)
            return True
        return False
        
    def scan_system(self):
        """扫描系统"""
        results = {
            'temp_files': {},
            'recycle_bin': {},
            'browser_cache': {}
        }
        
        # 扫描临时文件
        if any(self.clean_options[key] for key in ["windows_temp", "user_temp", "prefetch", "recent_docs"]):
            # 传递安全路径和排除的文件类型
            if hasattr(self.temp_cleaner, 'set_safe_paths'):
                self.temp_cleaner.set_safe_paths(self.safe_paths)
            if hasattr(self.temp_cleaner, 'set_excluded_extensions'):
                self.temp_cleaner.set_excluded_extensions(self.excluded_extensions)
            if hasattr(self.temp_cleaner, 'set_max_file_age'):
                self.temp_cleaner.set_max_file_age(self.max_file_age_days)
                
            results['temp_files'] = self.temp_cleaner.scan_temp_files()
            
        # 扫描回收站
        if self.clean_options["recycle_bin"]:
            results['recycle_bin'] = self.recycle_bin_cleaner.get_recycle_bin_size()
            
        # 扫描浏览器缓存
        browsers = []
        if self.clean_options["chrome"]: browsers.append("chrome")
        if self.clean_options["edge"]: browsers.append("edge")
        if self.clean_options["firefox"]: browsers.append("firefox")
        if self.clean_options["opera"]: browsers.append("opera")
        
        if browsers:
            results['browser_cache'] = self.browser_cache_cleaner.scan_browser_caches(browsers)
            
        self.scan_results = results
        return results
        
    def clean_system(self):
        """清理系统"""
        results = {
            'temp_files': {},
            'recycle_bin': {},
            'browser_cache': {}
        }
        
        # 清理临时文件
        temp_locations = []
        if self.clean_options["windows_temp"]: temp_locations.append("windows_temp")
        if self.clean_options["user_temp"]: temp_locations.append("user_temp")
        if self.clean_options["prefetch"]: temp_locations.append("prefetch")
        if self.clean_options["recent_docs"]: temp_locations.append("recent")
        
        if temp_locations:
            # 传递安全路径和排除的文件类型
            if hasattr(self.temp_cleaner, 'set_safe_paths'):
                self.temp_cleaner.set_safe_paths(self.safe_paths)
            if hasattr(self.temp_cleaner, 'set_excluded_extensions'):
                self.temp_cleaner.set_excluded_extensions(self.excluded_extensions)
            if hasattr(self.temp_cleaner, 'set_max_file_age'):
                self.temp_cleaner.set_max_file_age(self.max_file_age_days)
                
            # 如果启用安全模式，则使用安全清理方法
            if self.safe_mode and hasattr(self.temp_cleaner, 'clean_temp_files_safely'):
                results['temp_files'] = self.temp_cleaner.clean_temp_files_safely(temp_locations)
            else:
                results['temp_files'] = self.temp_cleaner.clean_temp_files(temp_locations)
            
        # 清理回收站
        if self.clean_options["recycle_bin"]:
            results['recycle_bin'] = self.recycle_bin_cleaner.empty_recycle_bin(
                no_confirmation=True,
                no_progress_ui=False,
                no_sound=True
            )
            
        # 清理浏览器缓存
        for browser in ["chrome", "edge", "firefox", "opera"]:
            if self.clean_options[browser]:
                # 如果启用安全模式，则使用安全清理方法
                if self.safe_mode and hasattr(self.browser_cache_cleaner, 'clean_browser_cache_safely'):
                    result = self.browser_cache_cleaner.clean_browser_cache_safely(browser)
                else:
                    result = self.browser_cache_cleaner.clean_browser_cache(browser)
                results['browser_cache'][browser] = result
                
        self.clean_results = results
        return results
        
    def get_formatted_scan_results(self):
        """获取格式化的扫描结果"""
        if not self.scan_results:
            return "尚未进行扫描"
            
        output = []
        total_size = 0
        
        # 添加标题框架
        scan_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        output.append("╔═══════════════════════════════════════════════╗")
        output.append("║             系统扫描结果报告                  ║")
        output.append("╠═══════════════════════════════════════════════╣")
        output.append(f"║ 扫描时间: {scan_time}              ║")
        output.append("╠═══════════════════════════════════════════════╣")
        
        # 临时文件结果
        if 'temp_files' in self.scan_results and self.scan_results['temp_files']:
            temp_results = self.scan_results['temp_files']
            output.append("║ 【临时文件】                                ║")
            
            if 'windows_temp' in temp_results:
                size = temp_results['windows_temp']
                total_size += size
                output.append(f"║ ✓ Windows临时文件: {self.temp_cleaner.format_size(size)}")
                
            if 'user_temp' in temp_results:
                size = temp_results['user_temp']
                total_size += size
                output.append(f"║ ✓ 用户临时文件: {self.temp_cleaner.format_size(size)}")
                
            if 'prefetch' in temp_results:
                size = temp_results['prefetch']
                total_size += size
                output.append(f"║ ✓ 预读取文件: {self.temp_cleaner.format_size(size)}")
                
            if 'recent' in temp_results:
                size = temp_results['recent']
                total_size += size
                output.append(f"║ ✓ 最近文档: {self.temp_cleaner.format_size(size)}")
            
            output.append("╠═══════════════════════════════════════════════╣")
                
        # 回收站结果
        if 'recycle_bin' in self.scan_results and self.scan_results['recycle_bin']:
            rb_results = self.scan_results['recycle_bin']
            size = rb_results.get('size', 0)
            total_size += size
            output.append("║ 【回收站】                                  ║")
            output.append(f"║ ✓ 回收站大小: {self.recycle_bin_cleaner.format_size(size)}")
            output.append(f"║ ● 包含文件数: {rb_results.get('items', 0)} 个项目")
            output.append("╠═══════════════════════════════════════════════╣")
            
        # 浏览器缓存结果
        if 'browser_cache' in self.scan_results and self.scan_results['browser_cache']:
            bc_results = self.scan_results['browser_cache']
            output.append("║ 【浏览器缓存】                              ║")
            
            for browser, size in bc_results.items():
                if browser != 'total':
                    total_size += size
                    browser_name = browser.title()
                    if browser == "chrome":
                        browser_name = "Chrome"
                    elif browser == "edge":
                        browser_name = "Edge"
                    elif browser == "firefox":
                        browser_name = "Firefox"
                    elif browser == "opera":
                        browser_name = "Opera"
                    
                    output.append(f"║ ✓ {browser_name} 缓存: {self.browser_cache_cleaner.format_size(size)}")
            
            output.append("╠═══════════════════════════════════════════════╣")
                    
        # 总计
        output.append(f"║ 总计可清理空间: {self.temp_cleaner.format_size(total_size)}               ║")
        
        # 安全模式提示
        if self.safe_mode:
            output.append("╠═══════════════════════════════════════════════╣")
            output.append("║ 📋 安全模式已启用，清理时将跳过:              ║")
            output.append(f"║ ● 最近 {self.max_file_age_days} 天内修改的文件")
            output.append(f"║ ● {len(self.safe_paths)} 个安全路径")
            output.append(f"║ ● {len(self.excluded_extensions)} 种文件类型")
        
        # 添加底部框架
        output.append("╚═══════════════════════════════════════════════╝")
        
        return "\n".join(output)
        
    def get_formatted_clean_results(self):
        """获取格式化的清理结果"""
        if not self.clean_results:
            return "尚未进行清理"
            
        output = []
        total_cleaned = 0
        items_cleaned = 0
        
        # 添加标题框架
        clean_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        output.append("╔═══════════════════════════════════════════════╗")
        output.append("║             系统清理结果报告                  ║")
        output.append("╠═══════════════════════════════════════════════╣")
        output.append(f"║ 清理时间: {clean_time}              ║")
        output.append("╠═══════════════════════════════════════════════╣")
        
        # 临时文件清理结果
        if 'temp_files' in self.clean_results and self.clean_results['temp_files']:
            temp_results = self.clean_results['temp_files']
            
            if any(temp_results[loc] > 0 for loc in temp_results if loc != 'total'):
                output.append("║ 【临时文件】                                ║")
                
                for location, cleaned in temp_results.items():
                    if location != 'total' and cleaned > 0:
                        output.append(f"║ ✓ 已清理{location}: {self.temp_cleaner.format_size(cleaned)}")
                        total_cleaned += cleaned
                        
                if 'skipped' in temp_results:
                    output.append(f"║ ● 已跳过: {temp_results['skipped']} 个文件")
                
                output.append("╠═══════════════════════════════════════════════╣")
                    
        # 回收站清理结果
        if 'recycle_bin' in self.clean_results and self.clean_results['recycle_bin']:
            rb_results = self.clean_results['recycle_bin']
            if rb_results.get('success'):
                size = rb_results.get('cleaned_size', 0)
                items = rb_results.get('cleaned_items', 0)
                total_cleaned += size
                items_cleaned += items
                
                output.append("║ 【回收站】                                  ║")
                output.append(f"║ ✓ 已清空回收站: {self.recycle_bin_cleaner.format_size(size)}")
                output.append(f"║ ● 清理项目数: {items} 个")
                output.append("╠═══════════════════════════════════════════════╣")
            else:
                error = rb_results.get('error', '未知错误')
                output.append("║ 【回收站】                                  ║")
                output.append(f"║ ✗ 清理回收站失败: {error}")
                output.append("╠═══════════════════════════════════════════════╣")
                
        # 浏览器缓存清理结果
        if 'browser_cache' in self.clean_results and self.clean_results['browser_cache']:
            bc_results = self.clean_results['browser_cache']
            
            if any(result.get('success', False) for result in bc_results.values()):
                output.append("║ 【浏览器缓存】                              ║")
                
                for browser, result in bc_results.items():
                    if result.get('success'):
                        size = result.get('cleaned_size', 0)
                        total_cleaned += size
                        browser_name = browser.title()
                        if browser == "chrome":
                            browser_name = "Chrome"
                        elif browser == "edge":
                            browser_name = "Edge"
                        elif browser == "firefox":
                            browser_name = "Firefox"
                        elif browser == "opera":
                            browser_name = "Opera"
                        
                        output.append(f"║ ✓ 已清理 {browser_name} 缓存: {self.browser_cache_cleaner.format_size(size)}")
                    else:
                        error = result.get('error', '未知错误')
                        output.append(f"║ ✗ 清理 {browser.title()} 缓存失败: {error}")
                
                output.append("╠═══════════════════════════════════════════════╣")
                    
        # 总计
        output.append(f"║ 总计已释放空间: {self.temp_cleaner.format_size(total_cleaned)}               ║")
        if items_cleaned > 0:
            output.append(f"║ 已清理项目数: {items_cleaned} 个                   ║")
        
        # 添加安全模式信息
        if self.safe_mode:
            output.append("╠═══════════════════════════════════════════════╣")
            output.append("║ 📋 安全模式已启用，清理时已跳过:              ║")
            output.append(f"║ ● 最近 {self.max_file_age_days} 天内修改的文件")
            output.append(f"║ ● {len(self.safe_paths)} 个安全路径")
            output.append(f"║ ● {len(self.excluded_extensions)} 种文件类型")
        
        # 添加底部框架
        output.append("╚═══════════════════════════════════════════════╝")
        
        return "\n".join(output) 