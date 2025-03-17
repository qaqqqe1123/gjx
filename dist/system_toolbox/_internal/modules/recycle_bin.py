import os
import ctypes
import logging
from ctypes import windll, wintypes
from ctypes.wintypes import DWORD
import time

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
        
        # 定义错误码
        self.ERROR_ACCESS_DENIED = -2147024891  # 0x80070005
        self.ERROR_FILE_NOT_FOUND = -2147024894  # 0x80070002
        self.ERROR_PATH_NOT_FOUND = -2147024893  # 0x80070003
        self.ERROR_SHARING_VIOLATION = -2147024864  # 0x80070020
        self.ERROR_LOCK_VIOLATION = -2147024863  # 0x80070021
        
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
    
    def empty_recycle_bin(self, no_confirmation=True, no_progress_ui=False, no_sound=True, max_retries=3):
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
            
            # 重试机制
            retry_count = 0
            last_error = None
            
            while retry_count < max_retries:
                try:
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
                        error_msg = self._get_error_message(result)
                        self.logger.warning(f"清空回收站失败，错误码: {result}，错误信息: {error_msg}")
                        last_error = result
                        
                        # 根据错误类型决定是否重试
                        if result in [self.ERROR_SHARING_VIOLATION, self.ERROR_LOCK_VIOLATION]:
                            retry_count += 1
                            if retry_count < max_retries:
                                self.logger.info(f"等待1秒后进行第{retry_count + 1}次重试...")
                                time.sleep(1)  # 等待1秒后重试
                                continue
                        else:
                            # 其他错误直接返回
                            break
                            
                except Exception as e:
                    self.logger.error(f"清空回收站时出现异常: {e}")
                    last_error = str(e)
                    retry_count += 1
                    if retry_count < max_retries:
                        self.logger.info(f"等待1秒后进行第{retry_count + 1}次重试...")
                        time.sleep(1)  # 等待1秒后重试
                        continue
                    break
                    
            # 所有重试都失败
            error_msg = self._get_error_message(last_error) if isinstance(last_error, int) else str(last_error)
            return {
                'success': False,
                'error': f"清空回收站失败: {error_msg}"
            }
                
        except Exception as e:
            self.logger.error(f"清空回收站时出错: {e}")
            return {
                'success': False,
                'error': str(e)
            }
            
    def _get_error_message(self, error_code):
        """获取错误信息"""
        if error_code == self.ERROR_ACCESS_DENIED:
            return "访问被拒绝，请检查权限"
        elif error_code == self.ERROR_FILE_NOT_FOUND:
            return "找不到文件"
        elif error_code == self.ERROR_PATH_NOT_FOUND:
            return "找不到路径"
        elif error_code == self.ERROR_SHARING_VIOLATION:
            return "文件正被其他程序使用"
        elif error_code == self.ERROR_LOCK_VIOLATION:
            return "文件被锁定"
        else:
            return f"未知错误 (错误码: {error_code})"
        
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