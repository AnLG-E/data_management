from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                            QFileDialog, QTableWidget, QTableWidgetItem, QComboBox, 
                            QGroupBox, QGridLayout, QMessageBox, QProgressBar)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import numpy as np
import os
from utils.file_handler import FileHandler

class DataImportDialog(QDialog):
    """数据导入对话框"""
    
    # 信号：数据导入完成
    data_imported = pyqtSignal(dict)
    
    def __init__(self, file_handler, parent=None):
        super().__init__(parent)
        self.file_handler = file_handler
        self.current_file = None
        self.current_data = None
        self.data_mapping = {
            'acceleration': [],
            'gyroscope': [],
            'noise': []
        }
        
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("数据导入")
        self.resize(800, 600)
        
        # 主布局
        main_layout = QVBoxLayout()
        
        # 文件选择区域
        file_layout = QHBoxLayout()
        self.file_label = QLabel("未选择文件")
        self.browse_btn = QPushButton("浏览...")
        self.browse_btn.clicked.connect(self.browse_file)
        
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.browse_btn)
        main_layout.addLayout(file_layout)
        
        # 数据预览区域
        preview_group = QGroupBox("数据预览")
        preview_layout = QVBoxLayout()
        
        self.preview_table = QTableWidget()
        self.preview_table.setEditTriggers(QTableWidget.NoEditTriggers)
        preview_layout.addWidget(self.preview_table)
        preview_group.setLayout(preview_layout)
        main_layout.addWidget(preview_group)
        
        # 数据映射区域
        mapping_group = QGroupBox("数据列映射")
        mapping_layout = QGridLayout()
        
        # 加速度数据映射
        mapping_layout.addWidget(QLabel("加速度数据（最多3列）:"), 0, 0)
        self.accel_combo1 = QComboBox()
        self.accel_combo2 = QComboBox()
        self.accel_combo3 = QComboBox()
        mapping_layout.addWidget(self.accel_combo1, 0, 1)
        mapping_layout.addWidget(self.accel_combo2, 0, 2)
        mapping_layout.addWidget(self.accel_combo3, 0, 3)
        
        # 陀螺仪数据映射
        mapping_layout.addWidget(QLabel("陀螺仪数据（最多3列）:"), 1, 0)
        self.gyro_combo1 = QComboBox()
        self.gyro_combo2 = QComboBox()
        self.gyro_combo3 = QComboBox()
        mapping_layout.addWidget(self.gyro_combo1, 1, 1)
        mapping_layout.addWidget(self.gyro_combo2, 1, 2)
        mapping_layout.addWidget(self.gyro_combo3, 1, 3)
        
        # 噪声数据映射
        mapping_layout.addWidget(QLabel("噪声数据（1列）:"), 2, 0)
        self.noise_combo = QComboBox()
        mapping_layout.addWidget(self.noise_combo, 2, 1)
        
        mapping_group.setLayout(mapping_layout)
        main_layout.addWidget(mapping_group)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # 按钮区域
        btn_layout = QHBoxLayout()
        self.import_btn = QPushButton("导入")
        self.import_btn.clicked.connect(self.import_data)
        self.import_btn.setEnabled(False)
        
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.import_btn)
        btn_layout.addWidget(self.cancel_btn)
        main_layout.addLayout(btn_layout)
        
        self.setLayout(main_layout)
        
        # 连接信号
        self._connect_signals()
    
    def _connect_signals(self):
        """连接信号"""
        # 加速度组合框信号
        self.accel_combo1.currentIndexChanged.connect(self._update_mapping)
        self.accel_combo2.currentIndexChanged.connect(self._update_mapping)
        self.accel_combo3.currentIndexChanged.connect(self._update_mapping)
        
        # 陀螺仪组合框信号
        self.gyro_combo1.currentIndexChanged.connect(self._update_mapping)
        self.gyro_combo2.currentIndexChanged.connect(self._update_mapping)
        self.gyro_combo3.currentIndexChanged.connect(self._update_mapping)
        
        # 噪声组合框信号
        self.noise_combo.currentIndexChanged.connect(self._update_mapping)
    
    def browse_file(self):
        """浏览文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择数据文件", "", "支持的文件 (*.xlsx *.xls *.csv *.mat)"
        )
        
        if file_path:
            self.current_file = file_path
            self.file_label.setText(os.path.basename(file_path))
            
            # 读取文件并显示预览
            self._load_file_data()
    
    def _load_file_data(self):
        """加载文件数据"""
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(20)
        
        # 读取文件
        self.current_data = self.file_handler.read_file(self.current_file)
        
        # 如果是列表，只取第一个数据集
        if isinstance(self.current_data, list):
            self.current_data = self.current_data[0]
        
        self.progress_bar.setValue(50)
        
        # 显示数据预览
        self._show_data_preview()
        
        self.progress_bar.setValue(80)
        
        # 更新组合框选项
        self._update_combo_options()
        
        self.progress_bar.setValue(100)
        self.progress_bar.setVisible(False)
        
        # 启用导入按钮
        self.import_btn.setEnabled(True)
    
    def _show_data_preview(self):
        """显示数据预览"""
        if self.current_data is None:
            return
        
        # 获取数据维度
        rows, cols = self.current_data.shape
        
        # 限制预览行数
        preview_rows = min(20, rows)
        
        # 设置表格维度
        self.preview_table.setRowCount(preview_rows)
        self.preview_table.setColumnCount(cols)
        
        # 设置列名
        self.preview_table.setHorizontalHeaderLabels([f"列 {i+1}" for i in range(cols)])
        
        # 填充数据
        for i in range(preview_rows):
            for j in range(cols):
                item = QTableWidgetItem(str(self.current_data[i, j]))
                self.preview_table.setItem(i, j, item)
        
        # 调整列宽
        self.preview_table.resizeColumnsToContents()
    
    def _update_combo_options(self):
        """更新组合框选项"""
        if self.current_data is None:
            return
        
        cols = self.current_data.shape[1]
        
        # 创建选项列表（包括空选项）
        options = ["未选择"] + [f"列 {i+1}" for i in range(cols)]
        
        # 更新所有组合框
        for combo in [self.accel_combo1, self.accel_combo2, self.accel_combo3,
                     self.gyro_combo1, self.gyro_combo2, self.gyro_combo3,
                     self.noise_combo]:
            combo.clear()
            combo.addItems(options)
    
    def _update_mapping(self):
        """更新数据映射"""
        # 重置映射
        self.data_mapping = {
            'acceleration': [],
            'gyroscope': [],
            'noise': []
        }
        
        # 获取加速度映射
        for combo in [self.accel_combo1, self.accel_combo2, self.accel_combo3]:
            idx = combo.currentIndex() - 1  # 减去空选项
            if idx >= 0:
                self.data_mapping['acceleration'].append(idx)
        
        # 获取陀螺仪映射
        for combo in [self.gyro_combo1, self.gyro_combo2, self.gyro_combo3]:
            idx = combo.currentIndex() - 1  # 减去空选项
            if idx >= 0:
                self.data_mapping['gyroscope'].append(idx)
        
        # 获取噪声映射
        idx = self.noise_combo.currentIndex() - 1  # 减去空选项
        if idx >= 0:
            self.data_mapping['noise'].append(idx)
    
    def import_data(self):
        """导入数据"""
        if not self.current_file or self.current_data is None:
            QMessageBox.warning(self, "警告", "请先选择并加载数据文件")
            return
        
        # 显示进度
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # 获取输出文件名
        base_name = os.path.splitext(os.path.basename(self.current_file))[0]
        output_file = os.path.join(os.path.dirname(self.current_file), f"{base_name}_converted.mat")
        
        self.progress_bar.setValue(30)
        
        # 转换文件格式
        success = self.file_handler.convert_to_mat(
            self.current_file, output_file, self.data_mapping
        )
        
        self.progress_bar.setValue(80)
        
        if success:
            # 发送数据导入完成信号
            result = {
                'original_file': self.current_file,
                'converted_file': output_file,
                'data_mapping': self.data_mapping,
                'data': self.current_data
            }
            self.data_imported.emit(result)
            
            QMessageBox.information(self, "成功", f"数据导入成功！\n转换后的文件：{output_file}")
            self.progress_bar.setValue(100)
            self.progress_bar.setVisible(False)
            self.accept()
        else:
            QMessageBox.critical(self, "错误", "数据导入失败！")
            self.progress_bar.setVisible(False)
