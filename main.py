import os
import sys
import customtkinter as ctk
from PIL import Image, ImageTk
import threading
import time

# 导入MVC组件
from mvc.views.main_window import MainWindow
from mvc.controllers.app_controller import AppController
from mvc.models.app_model import AppModel

def main():
    # 设置主题
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    # 创建MVC组件
    model = AppModel()
    app = MainWindow()
    controller = AppController(app, model)
    
    # 运行应用
    app.mainloop()

if __name__ == "__main__":
    main() 