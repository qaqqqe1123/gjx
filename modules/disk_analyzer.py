import os
import logging
import psutil
from pathlib import Path
import threading
import time

class DiskAnalyzer:
    def __init__(self):
        # 设置日志
        logging.basicConfig(level=logging.INFO, 
                           format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger('DiskAnalyzer')
        
        # 分析结果
        self.analysis_results = {}
        self.analysis_in_progress = False
        self.analysis_progress = 0
        self.analysis_cancel = False
        
    def get_disk_info(self):
        """获取所有磁盘信息"""
        try:
            disks = []
            for partition in psutil.disk_partitions():
                if os.name == 'nt' and ('cdrom' in partition.opts or partition.fstype == ''):
                    # 跳过CD-ROM驱动器
                    continue
                    
                usage = psutil.disk_usage(partition.mountpoint)
                disks.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent
                })
                
            return disks
        except Exception as e:
            self.logger.error(f"获取磁盘信息时出错: {e}")
            return []
            
    def analyze_directory_size(self, directory, callback=None):
        """分析目录大小"""
        try:
            if not os.path.exists(directory) or not os.path.isdir(directory):
                return {
                    'success': False,
                    'error': f"目录不存在或不是有效目录: {directory}"
                }
                
            self.analysis_results = {}
            self.analysis_in_progress = True
            self.analysis_progress = 0
            self.analysis_cancel = False
            
            # 在新线程中运行分析
            thread = threading.Thread(target=self._analyze_directory_thread, 
                                     args=(directory, callback))
            thread.daemon = True
            thread.start()
            
            return {
                'success': True,
                'message': f"开始分析目录: {directory}"
            }
        except Exception as e:
            self.logger.error(f"分析目录大小时出错: {e}")
            return {
                'success': False,
                'error': str(e)
            }
            
    def _analyze_directory_thread(self, directory, callback):
        """在线程中运行目录分析"""
        try:
            # 获取目录中的所有项目
            items = os.listdir(directory)
            total_items = len(items)
            processed_items = 0
            
            # 分析每个项目
            for item in items:
                if self.analysis_cancel:
                    break
                    
                item_path = os.path.join(directory, item)
                try:
                    if os.path.isdir(item_path):
                        # 如果是目录，递归计算大小
                        size = self._get_dir_size(item_path)
                    else:
                        # 如果是文件，直接获取大小
                        size = os.path.getsize(item_path)
                        
                    self.analysis_results[item] = {
                        'path': item_path,
                        'size': size,
                        'is_dir': os.path.isdir(item_path)
                    }
                except (PermissionError, FileNotFoundError) as e:
                    self.logger.warning(f"无法访问 {item_path}: {e}")
                    
                processed_items += 1
                self.analysis_progress = (processed_items / total_items) * 100
                
                if callback:
                    callback(self.analysis_progress)
                    
            # 按大小排序结果
            self.analysis_results = dict(sorted(self.analysis_results.items(), 
                                              key=lambda x: x[1]['size'], reverse=True))
                                              
            self.analysis_in_progress = False
            
            if callback:
                callback(100)  # 完成
        except Exception as e:
            self.logger.error(f"分析目录线程出错: {e}")
            self.analysis_in_progress = False
            
    def _get_dir_size(self, directory):
        """递归获取目录大小"""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(directory):
                for f in filenames:
                    try:
                        fp = os.path.join(dirpath, f)
                        if os.path.exists(fp):
                            total_size += os.path.getsize(fp)
                    except (PermissionError, FileNotFoundError) as e:
                        self.logger.warning(f"无法访问文件 {fp}: {e}")
        except Exception as e:
            self.logger.warning(f"获取目录 {directory} 大小时出错: {e}")
            
        return total_size
        
    def cancel_analysis(self):
        """取消正在进行的分析"""
        self.analysis_cancel = True
        
    def get_analysis_progress(self):
        """获取分析进度"""
        return {
            'in_progress': self.analysis_in_progress,
            'progress': self.analysis_progress
        }
        
    def get_analysis_results(self, limit=None):
        """获取分析结果"""
        if limit:
            # 返回前N个最大的项目
            results = {}
            for i, (key, value) in enumerate(self.analysis_results.items()):
                if i >= limit:
                    break
                results[key] = value
            return results
        else:
            return self.analysis_results
            
    def find_large_files(self, directory, min_size_mb=100, callback=None):
        """查找大文件"""
        try:
            if not os.path.exists(directory) or not os.path.isdir(directory):
                return {
                    'success': False,
                    'error': f"目录不存在或不是有效目录: {directory}"
                }
                
            min_size = min_size_mb * 1024 * 1024  # 转换为字节
            large_files = []
            
            self.analysis_in_progress = True
            self.analysis_progress = 0
            self.analysis_cancel = False
            
            # 在新线程中运行查找
            thread = threading.Thread(target=self._find_large_files_thread, 
                                     args=(directory, min_size, large_files, callback))
            thread.daemon = True
            thread.start()
            
            return {
                'success': True,
                'message': f"开始查找大文件: {directory}"
            }
        except Exception as e:
            self.logger.error(f"查找大文件时出错: {e}")
            return {
                'success': False,
                'error': str(e)
            }
            
    def _find_large_files_thread(self, directory, min_size, large_files, callback):
        """在线程中运行大文件查找"""
        try:
            total_items = sum([len(files) for _, _, files in os.walk(directory)])
            processed_items = 0
            
            for dirpath, dirnames, filenames in os.walk(directory):
                if self.analysis_cancel:
                    break
                    
                for f in filenames:
                    try:
                        file_path = os.path.join(dirpath, f)
                        if os.path.exists(file_path):
                            size = os.path.getsize(file_path)
                            if size >= min_size:
                                large_files.append({
                                    'path': file_path,
                                    'size': size
                                })
                    except (PermissionError, FileNotFoundError) as e:
                        self.logger.warning(f"无法访问文件 {file_path}: {e}")
                        
                    processed_items += 1
                    if total_items > 0:
                        self.analysis_progress = (processed_items / total_items) * 100
                        
                    if callback:
                        callback(self.analysis_progress)
                        
            # 按大小排序结果
            large_files.sort(key=lambda x: x['size'], reverse=True)
            self.analysis_results = {'large_files': large_files}
            self.analysis_in_progress = False
            
            if callback:
                callback(100)  # 完成
        except Exception as e:
            self.logger.error(f"查找大文件线程出错: {e}")
            self.analysis_in_progress = False
            
    def format_size(self, size_bytes):
        """将字节大小格式化为人类可读的格式"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
        
    def get_formatted_disk_info(self):
        """获取格式化的磁盘信息"""
        disks = self.get_disk_info()
        if not disks:
            return "无法获取磁盘信息"
            
        output = []
        output.append("磁盘信息:")
        
        for disk in disks:
            output.append(f"  {disk['device']} ({disk['mountpoint']}):")
            output.append(f"    文件系统: {disk['fstype']}")
            output.append(f"    总容量: {self.format_size(disk['total'])}")
            output.append(f"    已用空间: {self.format_size(disk['used'])}")
            output.append(f"    可用空间: {self.format_size(disk['free'])}")
            output.append(f"    使用率: {disk['percent']}%")
            output.append("")
            
        return "\n".join(output)
        
    def get_formatted_analysis_results(self, limit=10):
        """获取格式化的分析结果"""
        results = self.get_analysis_results(limit)
        if not results:
            return "没有分析结果"
            
        output = []
        output.append("目录分析结果:")
        
        for name, info in results.items():
            output.append(f"  {name}:")
            output.append(f"    路径: {info['path']}")
            output.append(f"    大小: {self.format_size(info['size'])}")
            output.append(f"    类型: {'目录' if info['is_dir'] else '文件'}")
            output.append("")
            
        return "\n".join(output)
        
    def get_formatted_large_files(self, limit=10):
        """获取格式化的大文件列表"""
        if 'large_files' not in self.analysis_results:
            return "没有大文件分析结果"
            
        large_files = self.analysis_results['large_files']
        if not large_files:
            return "未找到大文件"
            
        output = []
        output.append("大文件列表:")
        
        for i, file_info in enumerate(large_files):
            if i >= limit:
                break
                
            output.append(f"  {i+1}. {os.path.basename(file_info['path'])}")
            output.append(f"    路径: {file_info['path']}")
            output.append(f"    大小: {self.format_size(file_info['size'])}")
            output.append("")
            
        return "\n".join(output) 