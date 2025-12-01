from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QMenuBar, 
                            QToolBar, QStatusBar, QAction, QDockWidget, QListWidget, 
                            QGroupBox, QLabel, QSplitter, QMessageBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
import sys
import os

# 导入自定义组件
from data_import_dialog import DataImportDialog
from data_mapping_widget import DataMappingWidget
from visualization_panel import VisualizationPanel
from utils.matlab_interface import MatlabInterface
from utils.file_handler import FileHandler

class MainWindow(QMainWindow):
    """主界面"""
    
    def __init__(self):
        super().__init__()
        
        print("初始化主窗口...")
        
        # 初始化Matlab接口
        self.matlab_interface = MatlabInterface()
        self.matlab_available = False
        
        # 当前数据和映射
        self.current_data = None
        self.current_mapping = None
        self.current_file = None
        
        # 初始化界面
        print("初始化界面...")
        self.init_ui()
        
        # 初始化文件处理器（先不依赖Matlab）
        print("初始化文件处理器...")
        self.file_handler = FileHandler()
        
        # 尝试启动Matlab引擎（使用线程，防止卡住）
        print("尝试启动Matlab引擎...")
        self._start_matlab_engine()
    
    def init_ui(self):
        """初始化界面"""
        # 设置窗口标题和大小
        self.setWindowTitle("全周期数据管理系统")
        self.resize(1200, 800)
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建工具栏
        self.create_tool_bar()
        
        # 创建中央部件
        self.create_central_widget()
        
        # 创建停靠部件
        self.create_dock_widgets()
        
        # 创建状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("就绪")
    
    def create_menu_bar(self):
        """创建菜单栏"""
        menu_bar = self.menuBar()
        
        # 文件菜单
        file_menu = menu_bar.addMenu("文件")
        
        # 导入数据
        import_action = QAction("导入数据", self)
        import_action.setShortcut("Ctrl+I")
        import_action.triggered.connect(self.import_data)
        file_menu.addAction(import_action)
        
        # 保存数据
        save_action = QAction("保存数据", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_data)
        file_menu.addAction(save_action)
        
        # 退出
        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 数据菜单
        data_menu = menu_bar.addMenu("数据")
        
        # 数据预处理
        preprocess_action = QAction("数据预处理", self)
        data_menu.addAction(preprocess_action)
        
        # 特征提取
        feature_action = QAction("特征提取", self)
        data_menu.addAction(feature_action)
        
        # 可视化菜单
        vis_menu = menu_bar.addMenu("可视化")
        
        # 绘制时域图
        time_plot_action = QAction("绘制时域图", self)
        time_plot_action.triggered.connect(self.plot_time_domain)
        vis_menu.addAction(time_plot_action)
        
        # 绘制频域图
        freq_plot_action = QAction("绘制频域图", self)
        freq_plot_action.triggered.connect(self.plot_freq_domain)
        vis_menu.addAction(freq_plot_action)
        
        # 帮助菜单
        help_menu = menu_bar.addMenu("帮助")
        
        # 关于
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_tool_bar(self):
        """创建工具栏"""
        tool_bar = QToolBar("主工具栏")
        tool_bar.setIconSize(QSize(16, 16))
        
        # 导入数据按钮
        import_btn = QAction("导入数据", self)
        import_btn.triggered.connect(self.import_data)
        tool_bar.addAction(import_btn)
        
        # 保存数据按钮
        save_btn = QAction("保存数据", self)
        save_btn.triggered.connect(self.save_data)
        tool_bar.addAction(save_btn)
        
        tool_bar.addSeparator()
        
        # 绘制时域图按钮
        time_plot_btn = QAction("时域图", self)
        time_plot_btn.triggered.connect(self.plot_time_domain)
        tool_bar.addAction(time_plot_btn)
        
        # 绘制频域图按钮
        freq_plot_btn = QAction("频域图", self)
        freq_plot_btn.triggered.connect(self.plot_freq_domain)
        tool_bar.addAction(freq_plot_btn)
        
        self.addToolBar(tool_bar)
    
    def create_central_widget(self):
        """创建中央部件"""
        # 创建主部件
        main_widget = QWidget()
        
        # 创建垂直布局
        main_layout = QVBoxLayout()
        
        # 创建可视化面板
        self.vis_panel = VisualizationPanel(self.matlab_interface)
        main_layout.addWidget(self.vis_panel)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
    
    def create_dock_widgets(self):
        """创建停靠部件"""
        # 左侧停靠部件：数据文件列表
        left_dock = QDockWidget("数据文件", self)
        left_dock.setAllowedAreas(Qt.LeftDockWidgetArea)
        
        # 文件列表
        self.file_list = QListWidget()
        left_dock.setWidget(self.file_list)
        self.addDockWidget(Qt.LeftDockWidgetArea, left_dock)
        
        # 右侧停靠部件：数据映射和信息
        right_dock = QDockWidget("数据映射", self)
        right_dock.setAllowedAreas(Qt.RightDockWidgetArea)
        
        # 数据映射部件
        self.data_mapping_widget = DataMappingWidget()
        right_dock.setWidget(self.data_mapping_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, right_dock)
    
    def _start_matlab_engine(self):
        """启动Matlab引擎"""
        from PyQt5.QtCore import QThread, pyqtSignal
        
        # 创建一个内部线程类来启动Matlab引擎
        class MatlabEngineThread(QThread):
            engine_started = pyqtSignal(bool)
            
            def __init__(self, matlab_interface, functions_path):
                super().__init__()
                self.matlab_interface = matlab_interface
                self.functions_path = functions_path
            
            def run(self):
                try:
                    print("线程中启动Matlab引擎...")
                    # 启动Matlab引擎
                    success = self.matlab_interface.start_engine()
                    if success:
                        # 设置Matlab函数路径
                        self.matlab_interface.set_functions_path(self.functions_path)
                    self.engine_started.emit(success)
                except Exception as e:
                    print(f"启动Matlab引擎时发生异常: {e}")
                    self.engine_started.emit(False)
        
        # 准备Matlab函数路径
        matlab_functions_path = os.path.join(os.path.dirname(__file__), "..", "matlab_functions")
        
        # 创建并启动线程
        self.matlab_thread = MatlabEngineThread(self.matlab_interface, matlab_functions_path)
        self.matlab_thread.engine_started.connect(self._on_matlab_engine_started)
        self.matlab_thread.start()
        
        # 立即返回，不阻塞主线程
        self.statusBar.showMessage("正在后台启动Matlab引擎...")
    
    def _on_matlab_engine_started(self, success):
        """Matlab引擎启动完成后的回调"""
        if success:
            self.matlab_available = True
            # 更新文件处理器，添加Matlab接口
            self.file_handler.set_matlab_interface(self.matlab_interface)
            # 更新可视化面板的Matlab接口
            self.vis_panel.set_matlab_interface(self.matlab_interface)
            self.statusBar.showMessage("Matlab引擎启动成功")
            print("Matlab引擎启动成功")
        else:
            self.matlab_available = False
            self.statusBar.showMessage("Matlab引擎启动失败，部分功能可能受限")
            print("Matlab引擎启动失败")
    
    def import_data(self):
        """导入数据"""
        # 创建数据导入对话框
        dialog = DataImportDialog(self.file_handler, self)
        
        # 连接数据导入完成信号
        dialog.data_imported.connect(self._on_data_imported)
        
        # 显示对话框
        dialog.exec_()
    
    def _on_data_imported(self, result):
        """数据导入完成后的处理"""
        self.current_file = result['converted_file']
        self.current_data = result['data']
        self.current_mapping = result['data_mapping']
        
        # 更新数据映射部件
        self.data_mapping_widget.set_data(self.current_data, self.current_mapping)
        
        # 更新可视化面板
        self.vis_panel.set_data(self.current_data, self.current_mapping)
        
        # 将文件添加到文件列表
        self.file_list.addItem(os.path.basename(self.current_file))
        
        # 更新状态栏
        self.statusBar.showMessage(f"数据导入成功: {os.path.basename(self.current_file)}")
    
    def save_data(self):
        """保存数据"""
        if not self.current_data or not self.current_mapping:
            QMessageBox.warning(self, "警告", "没有可保存的数据")
            return
        
        # 使用文件处理器保存数据
        success = self.file_handler.write_mat_file(
            self.current_file,
            self.file_handler._apply_data_mapping(self.current_data, self.current_mapping)
        )
        
        if success:
            self.statusBar.showMessage(f"数据保存成功: {os.path.basename(self.current_file)}")
            QMessageBox.information(self, "成功", "数据保存成功")
        else:
            self.statusBar.showMessage("数据保存失败")
            QMessageBox.critical(self, "错误", "数据保存失败")
    
    def plot_time_domain(self):
        """绘制时域图"""
        if self.current_data is None or self.current_mapping is None:
            QMessageBox.warning(self, "警告", "没有可绘制的数据")
            return
        
        # 调用可视化面板的绘制时域图方法
        self.vis_panel._plot_time_domain(
            self.vis_panel._get_selected_data(),
            self.vis_panel.sample_rate_spin.value()
        )
    
    def plot_freq_domain(self):
        """绘制频域图"""
        if self.current_data is None or self.current_mapping is None:
            QMessageBox.warning(self, "警告", "没有可绘制的数据")
            return
        
        # 调用可视化面板的绘制频域图方法
        self.vis_panel._plot_freq_domain(
            self.vis_panel._get_selected_data(),
            self.vis_panel.sample_rate_spin.value()
        )
    
    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(self, "关于", "全周期数据管理系统\n版本: 1.0.0\n\n用于传感器数据的导入、处理、可视化和分析")
    
    def closeEvent(self, event):
        """关闭事件处理"""
        # 关闭Matlab引擎
        self.matlab_interface.stop_engine()
        
        # 确认关闭
        reply = QMessageBox.question(self, "确认关闭", "确定要关闭系统吗？",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

def main():
    """主函数"""
    from PyQt5.QtWidgets import QApplication
    
    # 创建应用程序
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = MainWindow()
    
    # 显示主窗口
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
