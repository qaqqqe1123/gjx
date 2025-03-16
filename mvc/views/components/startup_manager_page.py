import customtkinter as ctk
from tkinter import ttk

class StartupManagerPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        self.controller = None
        self._create_widgets()
        
    def _create_widgets(self):
        """创建页面组件"""
        # 页面标题
        title = ctk.CTkLabel(self, text="启动项管理", 
                            font=ctk.CTkFont(size=24, weight="bold"),
                            text_color=("#1a5fb4", "#0b3b8c"))
        title.pack(padx=20, pady=20)
        
        # 创建主框架
        main_frame = ctk.CTkFrame(self, fg_color=("white", "#edf2fb"))
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 创建工具栏
        toolbar = ctk.CTkFrame(main_frame, fg_color="transparent")
        toolbar.pack(padx=10, pady=10, fill="x")
        
        # 添加工具栏按钮
        refresh_btn = ctk.CTkButton(toolbar, text="刷新", 
                                   command=self._on_refresh,
                                   fg_color=("#1a73e8", "#0b57d0"), 
                                   hover_color=("#1557b0", "#0842a0"),
                                   width=100)
        refresh_btn.pack(side="left", padx=5)
        
        add_btn = ctk.CTkButton(toolbar, text="添加", 
                               command=self._on_add,
                               fg_color=("#1a73e8", "#0b57d0"), 
                               hover_color=("#1557b0", "#0842a0"),
                               width=100)
        add_btn.pack(side="left", padx=5)
        
        delete_btn = ctk.CTkButton(toolbar, text="删除", 
                                  command=self._on_delete,
                                  fg_color=("#1a73e8", "#0b57d0"), 
                                  hover_color=("#1557b0", "#0842a0"),
                                  width=100)
        delete_btn.pack(side="left", padx=5)
        
        enable_btn = ctk.CTkButton(toolbar, text="启用", 
                                  command=self._on_enable,
                                  fg_color=("#1a73e8", "#0b57d0"), 
                                  hover_color=("#1557b0", "#0842a0"),
                                  width=100)
        enable_btn.pack(side="left", padx=5)
        
        disable_btn = ctk.CTkButton(toolbar, text="禁用", 
                                   command=self._on_disable,
                                   fg_color=("#1a73e8", "#0b57d0"), 
                                   hover_color=("#1557b0", "#0842a0"),
                                   width=100)
        disable_btn.pack(side="left", padx=5)
        
        # 创建Treeview
        columns = ("name", "command", "location", "status")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings")
        
        # 设置列标题
        self.tree.heading("name", text="名称")
        self.tree.heading("command", text="命令")
        self.tree.heading("location", text="位置")
        self.tree.heading("status", text="状态")
        
        # 设置列宽
        self.tree.column("name", width=150)
        self.tree.column("command", width=300)
        self.tree.column("location", width=150)
        self.tree.column("status", width=100)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # 放置Treeview和滚动条
        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
        # 绑定双击事件
        self.tree.bind("<Double-1>", self._on_double_click)
        
    def set_controller(self, controller):
        """设置控制器"""
        self.controller = controller
        
    def _on_refresh(self):
        """刷新启动项列表"""
        if self.controller:
            self.controller.refresh_startup_items()
            
    def _on_add(self):
        """添加启动项"""
        if self.controller:
            self.controller.add_startup_item()
            
    def _on_delete(self):
        """删除启动项"""
        selected_item = self.tree.selection()
        if selected_item and self.controller:
            self.controller.delete_startup_item(selected_item[0])
            
    def _on_enable(self):
        """启用启动项"""
        selected_item = self.tree.selection()
        if selected_item and self.controller:
            self.controller.enable_startup_item(selected_item[0])
            
    def _on_disable(self):
        """禁用启动项"""
        selected_item = self.tree.selection()
        if selected_item and self.controller:
            self.controller.disable_startup_item(selected_item[0])
            
    def _on_double_click(self, event):
        """双击编辑启动项"""
        item = self.tree.selection()
        if item and self.controller:
            self.controller.edit_startup_item(item[0])
            
    def update_startup_items(self, items):
        """更新启动项列表"""
        # 清空现有项目
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # 添加新项目
        for item in items:
            self.tree.insert("", "end", values=(
                item["name"],
                item["command"],
                item["location"],
                "启用" if item["enabled"] else "禁用"
            ))
            
    def show_error(self, message):
        """显示错误消息"""
        # TODO: 实现错误消息显示
        pass
        
    def show_success(self, message):
        """显示成功消息"""
        # TODO: 实现成功消息显示
        pass 