from modules.temp_cleaner import TempCleaner
from modules.recycle_bin import RecycleBinCleaner
from modules.browser_cache import BrowserCacheCleaner
from modules.disk_analyzer import DiskAnalyzer
from modules.startup_manager import StartupManager
from modules.system_optimizer import SystemOptimizer

class AppModel:
    def __init__(self):
        # 初始化各个功能模块
        self.temp_cleaner = TempCleaner()
        self.recycle_bin_cleaner = RecycleBinCleaner()
        self.browser_cache_cleaner = BrowserCacheCleaner()
        self.disk_analyzer = DiskAnalyzer()
        self.startup_manager = StartupManager()
        self.system_optimizer = SystemOptimizer()
        
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
            "opera": False,
            "invalid_software": True,
            "invalid_file_assoc": True,
            "invalid_startup": True,
            "invalid_uninstall": False
        }
        
        # 扫描和清理结果
        self.scan_results = {}
        self.clean_results = {}
        
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
            
    def scan_system(self):
        """扫描系统"""
        results = {
            'temp_files': {},
            'recycle_bin': {},
            'browser_cache': {},
            'registry': {}
        }
        
        # 扫描临时文件
        if any(self.clean_options[key] for key in ["windows_temp", "user_temp", "prefetch", "recent_docs"]):
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
            'browser_cache': {},
            'registry': {}
        }
        
        # 清理临时文件
        temp_locations = []
        if self.clean_options["windows_temp"]: temp_locations.append("windows_temp")
        if self.clean_options["user_temp"]: temp_locations.append("user_temp")
        if self.clean_options["prefetch"]: temp_locations.append("prefetch")
        if self.clean_options["recent_docs"]: temp_locations.append("recent")
        
        if temp_locations:
            results['temp_files'] = self.temp_cleaner.clean_temp_files(temp_locations)
            
        # 清理回收站
        if self.clean_options["recycle_bin"]:
            results['recycle_bin'] = self.recycle_bin_cleaner.empty_recycle_bin()
            
        # 清理浏览器缓存
        for browser in ["chrome", "edge", "firefox", "opera"]:
            if self.clean_options[browser]:
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
        
        # 临时文件结果
        if 'temp_files' in self.scan_results and self.scan_results['temp_files']:
            temp_results = self.scan_results['temp_files']
            if 'windows_temp' in temp_results:
                size = temp_results['windows_temp']
                total_size += size
                output.append(f"Windows临时文件: {self.temp_cleaner.format_size(size)}")
                
            if 'user_temp' in temp_results:
                size = temp_results['user_temp']
                total_size += size
                output.append(f"用户临时文件: {self.temp_cleaner.format_size(size)}")
                
            if 'prefetch' in temp_results:
                size = temp_results['prefetch']
                total_size += size
                output.append(f"预读取文件: {self.temp_cleaner.format_size(size)}")
                
            if 'recent' in temp_results:
                size = temp_results['recent']
                total_size += size
                output.append(f"最近文档: {self.temp_cleaner.format_size(size)}")
                
        # 回收站结果
        if 'recycle_bin' in self.scan_results and self.scan_results['recycle_bin']:
            rb_results = self.scan_results['recycle_bin']
            size = rb_results.get('size', 0)
            total_size += size
            output.append(f"回收站: {self.recycle_bin_cleaner.format_size(size)}")
            output.append(f"包含文件数: {rb_results.get('items', 0)}")
            
        # 浏览器缓存结果
        if 'browser_cache' in self.scan_results and self.scan_results['browser_cache']:
            bc_results = self.scan_results['browser_cache']
            for browser, size in bc_results.items():
                if browser != 'total':
                    total_size += size
                    output.append(f"{browser.title()} 缓存: {self.browser_cache_cleaner.format_size(size)}")
                    
        # 总计
        output.append(f"\n总计可清理空间: {self.temp_cleaner.format_size(total_size)}")
        
        return "\n".join(output)
        
    def get_formatted_clean_results(self):
        """获取格式化的清理结果"""
        if not self.clean_results:
            return "尚未进行清理"
            
        output = []
        total_cleaned = 0
        
        # 临时文件清理结果
        if 'temp_files' in self.clean_results and self.clean_results['temp_files']:
            temp_results = self.clean_results['temp_files']
            for location, cleaned in temp_results.items():
                if location != 'total':
                    output.append(f"已清理{location}: {self.temp_cleaner.format_size(cleaned)}")
                    total_cleaned += cleaned
                    
        # 回收站清理结果
        if 'recycle_bin' in self.clean_results and self.clean_results['recycle_bin']:
            rb_results = self.clean_results['recycle_bin']
            if rb_results.get('success'):
                size = rb_results.get('cleaned_size', 0)
                total_cleaned += size
                output.append(f"已清空回收站: {self.recycle_bin_cleaner.format_size(size)}")
                
        # 浏览器缓存清理结果
        if 'browser_cache' in self.clean_results and self.clean_results['browser_cache']:
            bc_results = self.clean_results['browser_cache']
            for browser, result in bc_results.items():
                if result.get('success'):
                    size = result.get('cleaned_size', 0)
                    total_cleaned += size
                    output.append(f"已清理 {browser.title()} 缓存: {self.browser_cache_cleaner.format_size(size)}")
                    
        # 总计
        output.append(f"\n总计已释放空间: {self.temp_cleaner.format_size(total_cleaned)}")
        
        return "\n".join(output) 