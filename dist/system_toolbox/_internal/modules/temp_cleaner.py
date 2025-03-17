import os
import shutil
import tempfile
import winreg
import logging
import time
from datetime import datetime, timedelta

class TempCleaner:
    def __init__(self):
        self.temp_locations = {
            'windows_temp': os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Temp'),
            'user_temp': tempfile.gettempdir(),
            'prefetch': os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Prefetch'),
            'recent': os.path.join(os.environ.get('APPDATA', ''), 'Microsoft\\Windows\\Recent')
        }
        
        # 设置日志
        logging.basicConfig(level=logging.INFO, 
                           format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger('TempCleaner')
        
        # 安全路径列表 - 这些路径不会被清理
        self.safe_paths = []
        
        # 排除的文件类型 - 这些类型的文件不会被清理
        self.excluded_extensions = []
        
        # 最大文件年龄（天）- 超过这个时间的临时文件才会被清理
        self.max_file_age_days = 7
        
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
        
    def get_temp_size(self, location_key):
        """获取指定临时文件位置的大小"""
        try:
            path = self.temp_locations.get(location_key)
            if not path or not os.path.exists(path):
                return 0
                
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    try:
                        fp = os.path.join(dirpath, f)
                        if os.path.exists(fp):
                            total_size += os.path.getsize(fp)
                    except (PermissionError, FileNotFoundError) as e:
                        self.logger.warning(f"无法访问文件 {fp}: {e}")
                        
            return total_size
        except Exception as e:
            self.logger.error(f"获取临时文件大小时出错: {e}")
            return 0
            
    def scan_temp_files(self):
        """扫描所有临时文件位置并返回结果"""
        results = {}
        total_size = 0
        
        for key in self.temp_locations:
            size = self.get_temp_size(key)
            results[key] = size
            total_size += size
            
        results['total'] = total_size
        return results
        
    def clean_temp_files(self, locations=None):
        """清理指定的临时文件位置"""
        if locations is None:
            locations = list(self.temp_locations.keys())
            
        results = {}
        total_cleaned = 0
        
        for key in locations:
            if key not in self.temp_locations:
                continue
                
            path = self.temp_locations[key]
            if not os.path.exists(path):
                results[key] = 0
                continue
                
            size_before = self.get_temp_size(key)
            cleaned = self._clean_directory(path)
            size_after = self.get_temp_size(key)
            
            cleaned_size = size_before - size_after
            results[key] = cleaned_size
            total_cleaned += cleaned_size
            
        results['total'] = total_cleaned
        return results
        
    def clean_temp_files_safely(self, locations=None):
        """安全地清理指定的临时文件位置（跳过重要文件）"""
        if locations is None:
            locations = list(self.temp_locations.keys())
            
        results = {}
        total_cleaned = 0
        total_skipped = 0
        
        for key in locations:
            if key not in self.temp_locations:
                continue
                
            path = self.temp_locations[key]
            if not os.path.exists(path):
                results[key] = 0
                continue
                
            size_before = self.get_temp_size(key)
            cleaned, skipped = self._clean_directory_safely(path)
            size_after = self.get_temp_size(key)
            
            cleaned_size = size_before - size_after
            results[key] = cleaned_size
            total_cleaned += cleaned_size
            total_skipped += skipped
            
        results['total'] = total_cleaned
        results['skipped'] = total_skipped
        return results
        
    def _clean_directory(self, directory):
        """清理指定目录中的文件"""
        cleaned_count = 0
        
        try:
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                try:
                    if os.path.isfile(item_path):
                        os.unlink(item_path)
                        cleaned_count += 1
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path, ignore_errors=True)
                        cleaned_count += 1
                except (PermissionError, FileNotFoundError) as e:
                    self.logger.warning(f"无法删除 {item_path}: {e}")
        except Exception as e:
            self.logger.error(f"清理目录 {directory} 时出错: {e}")
            
        return cleaned_count
        
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
                            self.logger.info(f"跳过排除的文件类型: {item_path}")
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
        
        if 'windows_temp' in results:
            output.append(f"Windows临时文件: {self.format_size(results['windows_temp'])}")
            
        if 'user_temp' in results:
            output.append(f"用户临时文件: {self.format_size(results['user_temp'])}")
            
        if 'prefetch' in results:
            output.append(f"预读取文件: {self.format_size(results['prefetch'])}")
            
        if 'recent' in results:
            output.append(f"最近文档: {self.format_size(results['recent'])}")
            
        if 'total' in results:
            output.append(f"总计: {self.format_size(results['total'])}")
            
        if 'skipped' in results:
            output.append(f"已跳过: {results['skipped']} 个文件")
            
        return "\n".join(output) 