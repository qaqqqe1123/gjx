import customtkinter as ctk
from tkinter import ttk

class ServiceOptimizerPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        self.controller = None
        self._create_widgets()
        
    def _create_widgets(self):
        """创建页面组件"""
        # 页面标题
        title = ctk.CTkLabel(self, text="服务优化", 
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
        
        start_btn = ctk.CTkButton(toolbar, text="启动", 
                                 command=self._on_start,
                                 fg_color=("#1a73e8", "#0b57d0"), 
                                 hover_color=("#1557b0", "#0842a0"),
                                 width=100)
        start_btn.pack(side="left", padx=5)
        
        stop_btn = ctk.CTkButton(toolbar, text="停止", 
                                command=self._on_stop,
                                fg_color=("#1a73e8", "#0b57d0"), 
                                hover_color=("#1557b0", "#0842a0"),
                                width=100)
        stop_btn.pack(side="left", padx=5)
        
        auto_btn = ctk.CTkButton(toolbar, text="自动", 
                                command=self._on_auto,
                                fg_color=("#1a73e8", "#0b57d0"), 
                                hover_color=("#1557b0", "#0842a0"),
                                width=100)
        auto_btn.pack(side="left", padx=5)
        
        manual_btn = ctk.CTkButton(toolbar, text="手动", 
                                  command=self._on_manual,
                                  fg_color=("#1a73e8", "#0b57d0"), 
                                  hover_color=("#1557b0", "#0842a0"),
                                  width=100)
        manual_btn.pack(side="left", padx=5)
        
        disable_btn = ctk.CTkButton(toolbar, text="禁用", 
                                   command=self._on_disable,
                                   fg_color=("#1a73e8", "#0b57d0"), 
                                   hover_color=("#1557b0", "#0842a0"),
                                   width=100)
        disable_btn.pack(side="left", padx=5)
        
        # 创建搜索框
        search_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        search_frame.pack(padx=10, pady=(0, 10), fill="x")
        
        search_label = ctk.CTkLabel(search_frame, text="搜索:", 
                                   font=ctk.CTkFont(size=14))
        search_label.pack(side="left", padx=(0, 10))
        
        self.search_var = ctk.StringVar()
        self.search_var.trace("w", self._on_search)
        search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var,
                                  width=200)
        search_entry.pack(side="left")
        
        # 创建Treeview
        columns = ("name", "display_name", "status", "startup_type", "description")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings")
        
        # 设置列标题
        self.tree.heading("name", text="服务名称")
        self.tree.heading("display_name", text="显示名称")
        self.tree.heading("status", text="状态")
        self.tree.heading("startup_type", text="启动类型")
        self.tree.heading("description", text="描述")
        
        # 设置列宽
        self.tree.column("name", width=150)
        self.tree.column("display_name", width=200)
        self.tree.column("status", width=100)
        self.tree.column("startup_type", width=100)
        self.tree.column("description", width=300)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # 放置Treeview和滚动条
        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
        # 绑定双击事件
        self.tree.bind("<Double-1>", self._on_double_click)
        
        # 创建优化方案选择框架
        optimize_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        optimize_frame.pack(padx=10, pady=10, fill="x")
        
        optimize_label = ctk.CTkLabel(optimize_frame, text="优化方案:", 
                                     font=ctk.CTkFont(size=14))
        optimize_label.pack(side="left", padx=(0, 10))
        
        optimize_btn = ctk.CTkButton(optimize_frame, text="一键优化", 
                                    command=self._on_optimize,
                                    fg_color=("#1a73e8", "#0b57d0"), 
                                    hover_color=("#1557b0", "#0842a0"),
                                    width=120)
        optimize_btn.pack(side="left", padx=5)
        
        restore_btn = ctk.CTkButton(optimize_frame, text="还原默认", 
                                   command=self._on_restore,
                                   fg_color=("#1a73e8", "#0b57d0"), 
                                   hover_color=("#1557b0", "#0842a0"),
                                   width=120)
        restore_btn.pack(side="left", padx=5)
        
    def set_controller(self, controller):
        """设置控制器"""
        self.controller = controller
        
    def _on_refresh(self):
        """刷新服务列表"""
        if self.controller:
            self.controller.refresh_services()
            
    def _on_start(self):
        """启动服务"""
        selected_item = self.tree.selection()
        if selected_item and self.controller:
            self.controller.start_service(selected_item[0])
            
    def _on_stop(self):
        """停止服务"""
        selected_item = self.tree.selection()
        if selected_item and self.controller:
            self.controller.stop_service(selected_item[0])
            
    def _on_auto(self):
        """设置自动启动"""
        selected_item = self.tree.selection()
        if selected_item and self.controller:
            self.controller.set_service_startup_type(selected_item[0], "auto")
            
    def _on_manual(self):
        """设置手动启动"""
        selected_item = self.tree.selection()
        if selected_item and self.controller:
            self.controller.set_service_startup_type(selected_item[0], "manual")
            
    def _on_disable(self):
        """禁用服务"""
        selected_item = self.tree.selection()
        if selected_item and self.controller:
            self.controller.set_service_startup_type(selected_item[0], "disabled")
            
    def _on_search(self, *args):
        """搜索服务"""
        if self.controller:
            self.controller.search_services(self.search_var.get())
            
    def _on_double_click(self, event):
        """双击查看服务详情"""
        item = self.tree.selection()
        if item and self.controller:
            self.controller.show_service_details(item[0])
            
    def _on_optimize(self):
        """一键优化服务"""
        if self.controller:
            self.controller.optimize_services()
            
    def _on_restore(self):
        """还原服务默认设置"""
        if self.controller:
            self.controller.restore_services()
            
    def update_services(self, services):
        """更新服务列表"""
        # 清空现有项目
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # 添加新项目
        for service in services:
            self.tree.insert("", "end", values=(
                service["name"],
                service["display_name"],
                service["status"],
                service["startup_type"],
                service["description"]
            ))
            
    def show_error(self, message):
        """显示错误消息"""
        # TODO: 实现错误消息显示
        pass
        
    def show_success(self, message):
        """显示成功消息"""
        # TODO: 实现成功消息显示
        pass 