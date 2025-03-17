import customtkinter as ctk
from tkinter import ttk, messagebox
import logging

class ServiceOptimizerPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        # 设置日志
        self.logger = logging.getLogger('ServiceOptimizerPage')
        # 添加控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
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
        
        # 创建顶部按钮框架
        top_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        top_frame.pack(padx=10, pady=10, fill="x")
        
        # 添加一键优化和还原按钮
        optimize_btn = ctk.CTkButton(top_frame, text="一键优化", 
                                    command=self._on_optimize,
                                    fg_color=("#2ecc71", "#27ae60"), 
                                    hover_color=("#27ae60", "#219a52"),
                                    width=150,
                                    height=40,
                                    font=ctk.CTkFont(size=16, weight="bold"))
        optimize_btn.pack(side="left", padx=5)
        
        restore_btn = ctk.CTkButton(top_frame, text="还原默认", 
                                   command=self._on_restore,
                                   fg_color=("#e74c3c", "#c0392b"), 
                                   hover_color=("#c0392b", "#a93226"),
                                   width=150,
                                   height=40,
                                   font=ctk.CTkFont(size=16, weight="bold"))
        restore_btn.pack(side="left", padx=5)
        
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
        
    def set_controller(self, controller):
        """设置控制器"""
        self.logger.info("设置控制器")
        self.controller = controller
        # 设置控制器后自动刷新服务列表
        self.logger.info("准备刷新服务列表")
        self.after(100, self._on_refresh)
        
    def _on_refresh(self):
        """刷新服务列表"""
        self.logger.info("开始刷新服务列表")
        if self.controller:
            self.controller.refresh_services()
        else:
            self.logger.error("控制器未设置")
            
    def _on_start(self):
        """启动服务"""
        selected_items = self.tree.selection()
        if selected_items and self.controller:
            service_name = self.tree.item(selected_items[0])['values'][0]
            self.controller.start_service(service_name)
            
    def _on_stop(self):
        """停止服务"""
        selected_items = self.tree.selection()
        if selected_items and self.controller:
            service_name = self.tree.item(selected_items[0])['values'][0]
            self.controller.stop_service(service_name)
            
    def _on_auto(self):
        """设置自动启动"""
        selected_items = self.tree.selection()
        if selected_items and self.controller:
            service_name = self.tree.item(selected_items[0])['values'][0]
            self.controller.set_service_startup_type(service_name, "auto")
            
    def _on_manual(self):
        """设置手动启动"""
        selected_items = self.tree.selection()
        if selected_items and self.controller:
            service_name = self.tree.item(selected_items[0])['values'][0]
            self.controller.set_service_startup_type(service_name, "manual")
            
    def _on_disable(self):
        """禁用服务"""
        selected_items = self.tree.selection()
        if selected_items and self.controller:
            service_name = self.tree.item(selected_items[0])['values'][0]
            self.controller.set_service_startup_type(service_name, "disabled")
            
    def _on_search(self, *args):
        """搜索服务"""
        if self.controller:
            self.controller.search_services(self.search_var.get())
            
    def _on_double_click(self, event):
        """双击查看服务详情"""
        selected_items = self.tree.selection()
        if selected_items and self.controller:
            service_name = self.tree.item(selected_items[0])['values'][0]
            self.controller.show_service_details(service_name)
            
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
        self.logger.info(f"开始更新服务列表，收到 {len(services)} 个服务")
        
        try:
            # 清空现有项目
            self.logger.info("清空现有服务列表")
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # 添加新项目
            self.logger.info("开始添加新的服务项目")
            added_count = 0
            for service in services:
                try:
                    # 验证服务数据完整性
                    if not all(key in service for key in ["name", "display_name", "status", "startup_type", "description"]):
                        self.logger.warning(f"服务数据不完整: {service}")
                        continue
                        
                    # 确保所有值都是字符串类型
                    values = (
                        str(service["name"]),
                        str(service["display_name"]),
                        str(service["status"]),
                        str(service["startup_type"]),
                        str(service["description"])
                    )
                    
                    self.tree.insert("", "end", values=values)
                    added_count += 1
                    
                except Exception as e:
                    self.logger.error(f"添加服务项目时出错: {str(e)}")
                    continue
                    
            self.logger.info(f"服务列表更新完成，成功显示 {added_count} 个服务")
            
            # 如果没有添加任何服务，显示警告
            if added_count == 0:
                self.logger.warning("未能添加任何服务到列表中")
                self.show_error("未能显示任何服务")
                
        except Exception as e:
            self.logger.error(f"更新服务列表时出错: {str(e)}")
            self.show_error(f"更新服务列表时出错: {str(e)}")
            
    def show_error(self, message):
        """显示错误消息"""
        self.logger.error(f"错误: {message}")
        messagebox.showerror("错误", message)
        
    def show_success(self, message):
        """显示成功消息"""
        self.logger.info(f"成功: {message}")
        messagebox.showinfo("成功", message) 