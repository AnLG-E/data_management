from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, 
                            QTableWidgetItem, QPushButton, QGroupBox, QGridLayout, 
                            QComboBox, QMessageBox)
from PyQt5.QtCore import Qt
import numpy as np

class DataMappingWidget(QWidget):
    """数据映射组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_data = None
        self.data_mapping = {
            'acceleration': [],
            'gyroscope': [],
            'noise': []
        }
        
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        main_layout = QVBoxLayout()
        
        # 数据映射表格
        mapping_group = QGroupBox("当前数据映射")
        mapping_layout = QVBoxLayout()
        
        self.mapping_table = QTableWidget()
        self.mapping_table.setColumnCount(2)
        self.mapping_table.setHorizontalHeaderLabels(["数据类型", "映射列"])
        self.mapping_table.setRowCount(3)
        
        # 设置初始数据
        self._update_mapping_table()
        
        mapping_layout.addWidget(self.mapping_table)
        mapping_group.setLayout(mapping_layout)
        main_layout.addWidget(mapping_group)
        
        # 数据信息区域
        info_group = QGroupBox("数据信息")
        info_layout = QGridLayout()
        
        self.data_shape_label = QLabel("数据形状: ")
        self.accel_channels_label = QLabel("加速度通道数: 0")
        self.gyro_channels_label = QLabel("陀螺仪通道数: 0")
        self.noise_channels_label = QLabel("噪声通道数: 0")
        
        info_layout.addWidget(self.data_shape_label, 0, 0)
        info_layout.addWidget(self.accel_channels_label, 1, 0)
        info_layout.addWidget(self.gyro_channels_label, 1, 1)
        info_layout.addWidget(self.noise_channels_label, 2, 0)
        
        info_group.setLayout(info_layout)
        main_layout.addWidget(info_group)
        
        # 操作按钮区域
        btn_layout = QHBoxLayout()
        self.refresh_btn = QPushButton("刷新映射")
        self.refresh_btn.clicked.connect(self._update_mapping_table)
        
        self.clear_btn = QPushButton("清除映射")
        self.clear_btn.clicked.connect(self._clear_mapping)
        
        btn_layout.addWidget(self.refresh_btn)
        btn_layout.addWidget(self.clear_btn)
        btn_layout.addStretch()
        main_layout.addLayout(btn_layout)
        
        self.setLayout(main_layout)
    
    def set_data(self, data, mapping):
        """设置数据和映射关系"""
        self.current_data = data
        self.data_mapping = mapping
        
        # 更新数据信息
        self._update_data_info()
        
        # 更新映射表格
        self._update_mapping_table()
    
    def _update_data_info(self):
        """更新数据信息"""
        if self.current_data is not None:
            shape = self.current_data.shape
            self.data_shape_label.setText(f"数据形状: {shape[0]} 行 × {shape[1]} 列")
        
        # 更新通道数信息
        self.accel_channels_label.setText(f"加速度通道数: {len(self.data_mapping['acceleration'])}")
        self.gyro_channels_label.setText(f"陀螺仪通道数: {len(self.data_mapping['gyroscope'])}")
        self.noise_channels_label.setText(f"噪声通道数: {len(self.data_mapping['noise'])}")
    
    def _update_mapping_table(self):
        """更新映射表格"""
        # 加速度数据映射
        accel_cols = self.data_mapping['acceleration']
        accel_text = ", ".join([f"列 {col+1}" for col in accel_cols]) if accel_cols else "未映射"
        self.mapping_table.setItem(0, 0, QTableWidgetItem("加速度"))
        self.mapping_table.setItem(0, 1, QTableWidgetItem(accel_text))
        
        # 陀螺仪数据映射
        gyro_cols = self.data_mapping['gyroscope']
        gyro_text = ", ".join([f"列 {col+1}" for col in gyro_cols]) if gyro_cols else "未映射"
        self.mapping_table.setItem(1, 0, QTableWidgetItem("陀螺仪"))
        self.mapping_table.setItem(1, 1, QTableWidgetItem(gyro_text))
        
        # 噪声数据映射
        noise_cols = self.data_mapping['noise']
        noise_text = ", ".join([f"列 {col+1}" for col in noise_cols]) if noise_cols else "未映射"
        self.mapping_table.setItem(2, 0, QTableWidgetItem("噪声"))
        self.mapping_table.setItem(2, 1, QTableWidgetItem(noise_text))
        
        # 调整列宽
        self.mapping_table.resizeColumnsToContents()
    
    def _clear_mapping(self):
        """清除映射"""
        self.data_mapping = {
            'acceleration': [],
            'gyroscope': [],
            'noise': []
        }
        
        self._update_mapping_table()
        self._update_data_info()
        
        QMessageBox.information(self, "成功", "数据映射已清除")
    
    def get_mapping(self):
        """获取当前映射关系"""
        return self.data_mapping
    
    def get_data(self):
        """获取当前数据"""
        return self.current_data
