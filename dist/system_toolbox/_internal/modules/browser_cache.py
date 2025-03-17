import os
import shutil
import logging
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

class BrowserCacheCleaner:
    def __init__(self):
        # 设置日志
        logging.basicConfig(level=logging.INFO, 
                           format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger('BrowserCacheCleaner')
        
        # 获取用户主目录
        self.user_home = str(Path.home())
        
        # 定义各浏览器缓存路径
        self.browser_paths = {
            'chrome': {
                'cache': os.path.join(self.user_home, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Cache'),
                'cookies': os.path.join(self.user_home, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Cookies'),
                'history': os.path.join(self.user_home, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'History')
            },
            'edge': {
                'cache': os.path.join(self.user_home, 'AppData', 'Local', 'Microsoft', 'Edge', 'User Data', 'Default', 'Cache'),
                'cookies': os.path.join(self.user_home, 'AppData', 'Local', 'Microsoft', 'Edge', 'User Data', 'Default', 'Cookies'),
                'history': os.path.join(self.user_home, 'AppData', 'Local', 'Microsoft', 'Edge', 'User Data', 'Default', 'History')
            },
            'firefox': {
                'cache': os.path.join(self.user_home, 'AppData', 'Local', 'Mozilla', 'Firefox', 'Profiles'),
                'cookies': os.path.join(self.user_home, 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles')
            },
            'opera': {
                'cache': os.path.join(self.user_home, 'AppData', 'Local', 'Opera Software', 'Opera Stable', 'Cache'),
                'cookies': os.path.join(self.user_home, 'AppData', 'Roaming', 'Opera Software', 'Opera Stable', 'Cookies')
            }
        }
        
        # 安全路径列表 - 这些路径不会被清理
        self.safe_paths = []
        
        # 排除的文件类型 - 这些类型的文件不会被清理
        self.excluded_extensions = []
        
        # 最大文件年龄（天）- 超过这个时间的缓存文件才会被清理
        self.max_file_age_days = 7
        
        # 重要的浏览器文件 - 这些文件不会被清理
        self.important_browser_files = [
            'Bookmarks', 'Bookmarks.bak', 'Favicons', 'Login Data',
            'Preferences', 'Web Data', 'places.sqlite', 'key4.db',
            'logins.json', 'cert9.db', 'permissions.sqlite'
        ]
        
    def set_safe_paths(self, paths):
        """设置安全路径列表"""
        self.safe_paths = paths
        
    def set_excluded_extensions(self, extensions):
        """设置排除的文件类型"""
        self.excluded_extensions = extensions
        
    def set_max_file_age(self, days):
        """设置最大文件年龄"""
        if days > 0:
            self.max_file_age_days = days
            
    def is_path_safe(self, path):
        """检查路径是否安全（不应被清理）"""
        # 检查路径是否在安全路径列表中
        for safe_path in self.safe_paths:
            if path.startswith(safe_path):
                return True
                
        return False
        
    def is_file_excluded(self, file_path):
        """检查文件是否应被排除（不应被清理）"""
        # 检查文件扩展名
        _, ext = os.path.splitext(file_path.lower())
        if ext in self.excluded_extensions:
            return True
            
        # 检查是否是重要的浏览器文件
        file_name = os.path.basename(file_path)
        if file_name in self.important_browser_files:
            return True
            
        return False
        
    def is_file_too_new(self, file_path):
        """检查文件是否太新（不应被清理）"""
        try:
            # 获取文件修改时间
            mtime = os.path.getmtime(file_path)
            file_datetime = datetime.fromtimestamp(mtime)
            
            # 计算文件年龄
            age_days = (datetime.now() - file_datetime).days
            
            # 如果文件年龄小于最大年龄，则不应清理
            return age_days < self.max_file_age_days
        except (OSError, ValueError) as e:
            self.logger.warning(f"无法获取文件 {file_path} 的修改时间: {e}")
            # 如果无法确定，则认为文件太新（不清理）
            return True
        
    def get_browser_cache_size(self, browser):
        """获取指定浏览器缓存大小"""
        try:
            if browser not in self.browser_paths:
                return 0
                
            browser_info = self.browser_paths[browser]
            total_size = 0
            
            for cache_type, path in browser_info.items():
                if os.path.exists(path):
                    if os.path.isdir(path):
                        # 如果是目录，计算目录大小
                        for dirpath, dirnames, filenames in os.walk(path):
                            for f in filenames:
                                try:
                                    fp = os.path.join(dirpath, f)
                                    if os.path.exists(fp):
                                        total_size += os.path.getsize(fp)
                                except (PermissionError, FileNotFoundError) as e:
                                    self.logger.warning(f"无法访问文件 {fp}: {e}")
                    else:
                        # 如果是文件，直接获取文件大小
                        total_size += os.path.getsize(path)
                        
            return total_size
        except Exception as e:
            self.logger.error(f"获取浏览器缓存大小时出错: {e}")
            return 0
            
    def scan_browser_caches(self, browsers=None):
        """扫描指定浏览器的缓存大小"""
        if browsers is None:
            browsers = list(self.browser_paths.keys())
            
        results = {}
        total_size = 0
        
        for browser in browsers:
            if browser in self.browser_paths:
                size = self.get_browser_cache_size(browser)
                results[browser] = size
                total_size += size
                
        results['total'] = total_size
        return results
        
    def clean_browser_cache(self, browser):
        """清理指定浏览器的缓存"""
        try:
            if browser not in self.browser_paths:
                return {
                    'success': False,
                    'error': f"不支持的浏览器: {browser}"
                }
                
            # 获取清理前的大小
            size_before = self.get_browser_cache_size(browser)
            
            # 关闭浏览器进程
            self._kill_browser_process(browser)
            
            # 清理缓存
            browser_info = self.browser_paths[browser]
            for cache_type, path in browser_info.items():
                if os.path.exists(path):
                    try:
                        if os.path.isdir(path):
                            # 如果是Firefox配置文件夹，需要特殊处理
                            if browser == 'firefox' and cache_type == 'cache':
                                self._clean_firefox_cache(path)
                            else:
                                # 清空目录内容但保留目录本身
                                for item in os.listdir(path):
                                    item_path = os.path.join(path, item)
                                    try:
                                        if os.path.isfile(item_path):
                                            os.unlink(item_path)
                                        elif os.path.isdir(item_path):
                                            shutil.rmtree(item_path, ignore_errors=True)
                                    except (PermissionError, FileNotFoundError) as e:
                                        self.logger.warning(f"无法删除 {item_path}: {e}")
                        else:
                            # 如果是文件，直接删除
                            os.unlink(path)
                    except Exception as e:
                        self.logger.error(f"清理 {browser} 的 {cache_type} 时出错: {e}")
                        
            # 获取清理后的大小
            size_after = self.get_browser_cache_size(browser)
            cleaned_size = size_before - size_after
            
            return {
                'success': True,
                'cleaned_size': cleaned_size
            }
        except Exception as e:
            self.logger.error(f"清理浏览器缓存时出错: {e}")
            return {
                'success': False,
                'error': str(e)
            }
            
    def clean_browser_cache_safely(self, browser):
        """安全地清理指定浏览器的缓存（跳过重要文件）"""
        try:
            if browser not in self.browser_paths:
                return {
                    'success': False,
                    'error': f"不支持的浏览器: {browser}"
                }
                
            # 获取清理前的大小
            size_before = self.get_browser_cache_size(browser)
            
            # 关闭浏览器进程
            self._kill_browser_process(browser)
            
            # 清理缓存
            browser_info = self.browser_paths[browser]
            skipped_files = 0
            
            for cache_type, path in browser_info.items():
                if os.path.exists(path):
                    try:
                        if os.path.isdir(path):
                            # 如果是Firefox配置文件夹，需要特殊处理
                            if browser == 'firefox' and cache_type == 'cache':
                                cleaned, skipped = self._clean_firefox_cache_safely(path)
                                skipped_files += skipped
                            else:
                                # 安全清理目录
                                cleaned, skipped = self._clean_directory_safely(path)
                                skipped_files += skipped
                        else:
                            # 如果是文件，检查是否应该跳过
                            if self.is_file_excluded(path) or self.is_path_safe(path):
                                self.logger.info(f"跳过重要文件: {path}")
                                skipped_files += 1
                            else:
                                os.unlink(path)
                    except Exception as e:
                        self.logger.error(f"安全清理 {browser} 的 {cache_type} 时出错: {e}")
                        skipped_files += 1
                        
            # 获取清理后的大小
            size_after = self.get_browser_cache_size(browser)
            cleaned_size = size_before - size_after
            
            return {
                'success': True,
                'cleaned_size': cleaned_size,
                'skipped': skipped_files
            }
        except Exception as e:
            self.logger.error(f"安全清理浏览器缓存时出错: {e}")
            return {
                'success': False,
                'error': str(e)
            }
            
    def _clean_directory_safely(self, directory):
        """安全地清理指定目录中的文件（跳过重要文件）"""
        cleaned_count = 0
        skipped_count = 0
        
        try:
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                try:
                    # 检查是否应跳过此文件/目录
                    if self.is_path_safe(item_path):
                        self.logger.info(f"跳过安全路径: {item_path}")
                        skipped_count += 1
                        continue
                        
                    if os.path.isfile(item_path):
                        # 检查文件是否应被排除
                        if self.is_file_excluded(item_path):
                            self.logger.info(f"跳过排除的文件: {item_path}")
                            skipped_count += 1
                            continue
                            
                        # 检查文件是否太新
                        if self.is_file_too_new(item_path):
                            self.logger.info(f"跳过较新的文件: {item_path}")
                            skipped_count += 1
                            continue
                            
                        # 删除文件
                        os.unlink(item_path)
                        cleaned_count += 1
                    elif os.path.isdir(item_path):
                        # 递归清理子目录
                        sub_cleaned, sub_skipped = self._clean_directory_safely(item_path)
                        cleaned_count += sub_cleaned
                        skipped_count += sub_skipped
                        
                        # 如果目录为空，则删除
                        if not os.listdir(item_path):
                            os.rmdir(item_path)
                except (PermissionError, FileNotFoundError) as e:
                    self.logger.warning(f"无法访问 {item_path}: {e}")
                    skipped_count += 1
        except Exception as e:
            self.logger.error(f"安全清理目录 {directory} 时出错: {e}")
            
        return cleaned_count, skipped_count
            
    def _kill_browser_process(self, browser):
        """关闭浏览器进程"""
        process_names = {
            'chrome': 'chrome.exe',
            'edge': 'msedge.exe',
            'firefox': 'firefox.exe',
            'opera': 'opera.exe'
        }
        
        if browser in process_names:
            try:
                subprocess.run(['taskkill', '/F', '/IM', process_names[browser]], 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except Exception as e:
                self.logger.warning(f"关闭 {browser} 进程时出错: {e}")
                
    def _clean_firefox_cache(self, profiles_dir):
        """清理Firefox缓存"""
        try:
            # 遍历所有配置文件
            for profile in os.listdir(profiles_dir):
                profile_path = os.path.join(profiles_dir, profile)
                if os.path.isdir(profile_path):
                    # 清理缓存文件夹
                    cache_path = os.path.join(profile_path, 'cache2')
                    if os.path.exists(cache_path):
                        shutil.rmtree(cache_path, ignore_errors=True)
                        
                    # 清理其他缓存文件
                    for cache_file in ['cookies.sqlite', 'webappsstore.sqlite', 'chromeappsstore.sqlite']:
                        file_path = os.path.join(profile_path, cache_file)
                        if os.path.exists(file_path):
                            try:
                                os.unlink(file_path)
                            except Exception as e:
                                self.logger.warning(f"无法删除 {file_path}: {e}")
        except Exception as e:
            self.logger.error(f"清理Firefox缓存时出错: {e}")
            
    def _clean_firefox_cache_safely(self, profiles_dir):
        """安全地清理Firefox缓存"""
        cleaned_count = 0
        skipped_count = 0
        
        try:
            # 遍历所有配置文件
            for profile in os.listdir(profiles_dir):
                profile_path = os.path.join(profiles_dir, profile)
                if os.path.isdir(profile_path):
                    # 清理缓存文件夹
                    cache_path = os.path.join(profile_path, 'cache2')
                    if os.path.exists(cache_path):
                        sub_cleaned, sub_skipped = self._clean_directory_safely(cache_path)
                        cleaned_count += sub_cleaned
                        skipped_count += sub_skipped
                        
                    # 清理其他缓存文件，但跳过重要文件
                    for cache_file in ['cookies.sqlite', 'webappsstore.sqlite', 'chromeappsstore.sqlite']:
                        file_path = os.path.join(profile_path, cache_file)
                        if os.path.exists(file_path):
                            # 检查是否应跳过此文件
                            if self.is_file_excluded(file_path) or self.is_path_safe(file_path):
                                self.logger.info(f"跳过重要文件: {file_path}")
                                skipped_count += 1
                                continue
                                
                            try:
                                os.unlink(file_path)
                                cleaned_count += 1
                            except Exception as e:
                                self.logger.warning(f"无法删除 {file_path}: {e}")
                                skipped_count += 1
        except Exception as e:
            self.logger.error(f"安全清理Firefox缓存时出错: {e}")
            
        return cleaned_count, skipped_count
            
    def format_size(self, size_bytes):
        """将字节大小格式化为人类可读的格式"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
        
    def get_formatted_results(self, results):
        """获取格式化的结果字符串"""
        output = []
        
        browser_names = {
            'chrome': 'Google Chrome',
            'edge': 'Microsoft Edge',
            'firefox': 'Mozilla Firefox',
            'opera': 'Opera'
        }
        
        for browser, size in results.items():
            if browser == 'total':
                continue
                
            browser_name = browser_names.get(browser, browser)
            output.append(f"{browser_name}: {self.format_size(size)}")
            
        if 'total' in results:
            output.append(f"总计: {self.format_size(results['total'])}")
            
        if 'skipped' in results:
            output.append(f"已跳过: {results['skipped']} 个重要文件")
            
        return "\n".join(output) 