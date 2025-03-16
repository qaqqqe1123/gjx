import os
import ctypes
import logging
from ctypes import windll, wintypes
from ctypes.wintypes import DWORD

class RecycleBinCleaner:
    def __init__(self):
        # 设置日志
        logging.basicConfig(level=logging.INFO, 
                           format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger('RecycleBinCleaner')
        
        # 定义Windows API常量
        self.SHERB_NOCONFIRMATION = 0x00000001
        self.SHERB_NOPROGRESSUI = 0x00000002
        self.SHERB_NOSOUND = 0x00000004
        
    def get_recycle_bin_size(self):
        """获取回收站大小"""
        try:
            # 定义SHQueryRecycleBin函数
            shell32 = ctypes.windll.shell32
            
            class SHQUERYRBINFO(ctypes.Structure):
                _fields_ = [
                    ('cbSize', wintypes.DWORD),
                    ('i64Size', ctypes.c_ulonglong),
                    ('i64NumItems', ctypes.c_ulonglong)
                ]
            
            info = SHQUERYRBINFO()
            info.cbSize = ctypes.sizeof(info)
            
            # 调用SHQueryRecycleBin函数
            result = shell32.SHQueryRecycleBinW(None, ctypes.byref(info))
            
            if result == 0:  # S_OK
                return {
                    'size': info.i64Size,
                    'items': info.i64NumItems
                }
            else:
                self.logger.error(f"获取回收站信息失败，错误码: {result}")
                return {
                    'size': 0,
                    'items': 0
                }
        except Exception as e:
            self.logger.error(f"获取回收站大小时出错: {e}")
            return {
                'size': 0,
                'items': 0
            }
    
    def empty_recycle_bin(self, no_confirmation=True, no_progress_ui=False, no_sound=True):
        """清空回收站"""
        try:
            # 定义SHEmptyRecycleBin函数
            shell32 = ctypes.windll.shell32
            
            # 设置标志
            flags = 0
            if no_confirmation:
                flags |= self.SHERB_NOCONFIRMATION
            if no_progress_ui:
                flags |= self.SHERB_NOPROGRESSUI
            if no_sound:
                flags |= self.SHERB_NOSOUND
                
            # 获取清理前的大小
            before_info = self.get_recycle_bin_size()
            
            # 调用SHEmptyRecycleBin函数
            result = shell32.SHEmptyRecycleBinW(None, None, flags)
            
            if result == 0:  # S_OK
                self.logger.info("回收站清空成功")
                return {
                    'success': True,
                    'cleaned_size': before_info['size'],
                    'cleaned_items': before_info['items']
                }
            else:
                self.logger.error(f"清空回收站失败，错误码: {result}")
                return {
                    'success': False,
                    'error': f"清空回收站失败，错误码: {result}"
                }
        except Exception as e:
            self.logger.error(f"清空回收站时出错: {e}")
            return {
                'success': False,
                'error': str(e)
            }
            
    def format_size(self, size_bytes):
        """将字节大小格式化为人类可读的格式"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
        
    def get_formatted_info(self):
        """获取格式化的回收站信息"""
        info = self.get_recycle_bin_size()
        
        size_str = self.format_size(info['size'])
        items_str = f"{info['items']} 个项目"
        
        return f"回收站大小: {size_str}\n包含文件: {items_str}" 