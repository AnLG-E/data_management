from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                            QGroupBox, QComboBox, QSpinBox, QDoubleSpinBox, QGridLayout,
                            QMessageBox, QTabWidget)
from PyQt5.QtCore import Qt
import numpy as np
from utils.matlab_interface import MatlabInterface

class VisualizationPanel(QWidget):
    """数据可视化面板"""
    
    def __init__(self, matlab_interface, parent=None):
        super().__init__(parent)
        self.matlab_interface = matlab_interface
        self.current_data = None
        self.data_mapping = None
        
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        main_layout = QVBoxLayout()
        
        # 选项卡控件
        self.tab_widget = QTabWidget()
        
        # 时域图选项卡
        self.time_domain_tab = QWidget()
        self._init_time_domain_tab()
        self.tab_widget.addTab(self.time_domain_tab, "时域图")
        
        # 频域图选项卡
        self.freq_domain_tab = QWidget()
        self._init_freq_domain_tab()
        self.tab_widget.addTab(self.freq_domain_tab, "频域图")
        
        main_layout.addWidget(self.tab_widget)
        
        # 数据选择区域
        data_group = QGroupBox("数据选择")
        data_layout = QGridLayout()
        
        self.data_type_combo = QComboBox()
        self.data_type_combo.addItems(["加速度", "陀螺仪", "噪声"])
        
        self.channel_spin = QSpinBox()
        self.channel_spin.setMinimum(1)
        self.channel_spin.setMaximum(3)
        self.channel_spin.setValue(1)
        
        data_layout.addWidget(QLabel("数据类型:"), 0, 0)
        data_layout.addWidget(self.data_type_combo, 0, 1)
        data_layout.addWidget(QLabel("通道:"), 0, 2)
        data_layout.addWidget(self.channel_spin, 0, 3)
        
        data_group.setLayout(data_layout)
        main_layout.addWidget(data_group)
        
        # 采样率设置
        sample_group = QGroupBox("采样率设置")
        sample_layout = QHBoxLayout()
        
        self.sample_rate_spin = QDoubleSpinBox()
        self.sample_rate_spin.setMinimum(1.0)
        self.sample_rate_spin.setMaximum(10000.0)
        self.sample_rate_spin.setValue(1000.0)
        self.sample_rate_spin.setSuffix(" Hz")
        
        sample_layout.addWidget(QLabel("采样率:"))
        sample_layout.addWidget(self.sample_rate_spin)
        sample_layout.addStretch()
        
        sample_group.setLayout(sample_layout)
        main_layout.addWidget(sample_group)
        
        # 按钮区域
        btn_layout = QHBoxLayout()
        
        self.plot_btn = QPushButton("绘制图表")
        self.plot_btn.clicked.connect(self._plot_current_tab)
        
        self.clear_btn = QPushButton("清除图表")
        self.clear_btn.clicked.connect(self._clear_plots)
        
        btn_layout.addWidget(self.plot_btn)
        btn_layout.addWidget(self.clear_btn)
        btn_layout.addStretch()
        
        main_layout.addLayout(btn_layout)
        
        self.setLayout(main_layout)
    
    def _init_time_domain_tab(self):
        """初始化时域图选项卡"""
        layout = QVBoxLayout()
        
        # 时域图设置
        time_settings_group = QGroupBox("时域图设置")
        time_settings_layout = QGridLayout()
        
        self.time_range_start = QDoubleSpinBox()
        self.time_range_start.setMinimum(0.0)
        self.time_range_start.setMaximum(1000.0)
        self.time_range_start.setValue(0.0)
        self.time_range_start.setSuffix(" s")
        
        self.time_range_end = QDoubleSpinBox()
        self.time_range_end.setMinimum(0.1)
        self.time_range_end.setMaximum(1000.0)
        self.time_range_end.setValue(10.0)
        self.time_range_end.setSuffix(" s")
        
        time_settings_layout.addWidget(QLabel("时间范围: 从"), 0, 0)
        time_settings_layout.addWidget(self.time_range_start, 0, 1)
        time_settings_layout.addWidget(QLabel("到"), 0, 2)
        time_settings_layout.addWidget(self.time_range_end, 0, 3)
        
        time_settings_group.setLayout(time_settings_layout)
        layout.addWidget(time_settings_group)
        
        # 说明文本
        info_label = QLabel("时域图显示原始数据的波形，可用于观察信号的时域特征。")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        self.time_domain_tab.setLayout(layout)
    
    def _init_freq_domain_tab(self):
        """初始化频域图选项卡"""
        layout = QVBoxLayout()
        
        # 频域图设置
        freq_settings_group = QGroupBox("频域图设置")
        freq_settings_layout = QGridLayout()
        
        self.freq_range_start = QDoubleSpinBox()
        self.freq_range_start.setMinimum(0.0)
        self.freq_range_start.setMaximum(5000.0)
        self.freq_range_start.setValue(0.0)
        self.freq_range_start.setSuffix(" Hz")
        
        self.freq_range_end = QDoubleSpinBox()
        self.freq_range_end.setMinimum(1.0)
        self.freq_range_end.setMaximum(5000.0)
        self.freq_range_end.setValue(500.0)
        self.freq_range_end.setSuffix(" Hz")
        
        freq_settings_layout.addWidget(QLabel("频率范围: 从"), 0, 0)
        freq_settings_layout.addWidget(self.freq_range_start, 0, 1)
        freq_settings_layout.addWidget(QLabel("到"), 0, 2)
        freq_settings_layout.addWidget(self.freq_range_end, 0, 3)
        
        freq_settings_group.setLayout(freq_settings_layout)
        layout.addWidget(freq_settings_group)
        
        # 说明文本
        info_label = QLabel("频域图使用pwelch函数计算功率谱密度，可用于观察信号的频域特征。")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        self.freq_domain_tab.setLayout(layout)
    
    def set_data(self, data, mapping):
        """设置数据和映射关系"""
        self.current_data = data
        self.data_mapping = mapping
        
        # 更新通道选择范围
        self._update_channel_range()
    
    def _update_channel_range(self):
        """更新通道选择范围"""
        data_type = self.data_type_combo.currentText()
        
        if data_type == "加速度":
            channels = len(self.data_mapping['acceleration'])
        elif data_type == "陀螺仪":
            channels = len(self.data_mapping['gyroscope'])
        elif data_type == "噪声":
            channels = len(self.data_mapping['noise'])
        else:
            channels = 0
        
        self.channel_spin.setMaximum(max(1, channels))
        if self.channel_spin.value() > channels:
            self.channel_spin.setValue(1)
    
    def _get_selected_data(self):
        """获取选中的数据"""
        if self.current_data is None or self.data_mapping is None:
            QMessageBox.warning(self, "警告", "没有可用的数据")
            return None
        
        data_type = self.data_type_combo.currentText()
        channel_idx = self.channel_spin.value() - 1  # 转换为0-based索引
        
        # 获取对应的数据列
        if data_type == "加速度":
            accel_cols = self.data_mapping['acceleration']
            if channel_idx >= len(accel_cols):
                QMessageBox.warning(self, "警告", "选择的通道超出范围")
                return None
            data_col = accel_cols[channel_idx]
        elif data_type == "陀螺仪":
            gyro_cols = self.data_mapping['gyroscope']
            if channel_idx >= len(gyro_cols):
                QMessageBox.warning(self, "警告", "选择的通道超出范围")
                return None
            data_col = gyro_cols[channel_idx]
        elif data_type == "噪声":
            noise_cols = self.data_mapping['noise']
            if channel_idx >= len(noise_cols):
                QMessageBox.warning(self, "警告", "选择的通道超出范围")
                return None
            data_col = noise_cols[channel_idx]
        else:
            QMessageBox.warning(self, "警告", "无效的数据类型")
            return None
        
        # 提取数据
        selected_data = self.current_data[:, data_col]
        
        return selected_data
    
    def _plot_current_tab(self):
        """绘制当前选项卡的图表"""
        # 获取选中的数据
        selected_data = self._get_selected_data()
        if selected_data is None:
            return
        
        # 获取采样率
        sample_rate = self.sample_rate_spin.value()
        
        # 根据当前选项卡绘制不同的图表
        current_tab = self.tab_widget.currentIndex()
        
        if current_tab == 0:  # 时域图
            self._plot_time_domain(selected_data, sample_rate)
        elif current_tab == 1:  # 频域图
            self._plot_freq_domain(selected_data, sample_rate)
    
    def _plot_time_domain(self, data, sample_rate):
        """绘制时域图"""
        if not self.matlab_interface:
            QMessageBox.critical(self, "错误", "Matlab接口未初始化")
            return
        
        try:
            # 调用Matlab函数绘制时域图
            success = self.matlab_interface.plot_time_domain(
                data, sample_rate, title="时域波形图"
            )
            
            if not success:
                QMessageBox.critical(self, "错误", "绘制时域图失败")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"绘制时域图时发生错误: {e}")
    
    def _plot_freq_domain(self, data, sample_rate):
        """绘制频域图"""
        if not self.matlab_interface:
            QMessageBox.critical(self, "错误", "Matlab接口未初始化")
            return
        
        try:
            # 调用Matlab函数绘制频域图
            success = self.matlab_interface.plot_freq_domain(
                data, sample_rate, title="频域功率谱图"
            )
            
            if not success:
                QMessageBox.critical(self, "错误", "绘制频域图失败")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"绘制频域图时发生错误: {e}")
    
    def _clear_plots(self):
        """清除所有图表"""
        if not self.matlab_interface:
            QMessageBox.critical(self, "错误", "Matlab接口未初始化")
            return
        
        try:
            # 关闭所有Matlab图形窗口
            self.matlab_interface.call_function('close', 'all')
            QMessageBox.information(self, "成功", "所有图表已清除")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"清除图表时发生错误: {e}")
    
    def get_matlab_interface(self):
        """获取Matlab接口"""
        return self.matlab_interface
    
    def set_matlab_interface(self, matlab_interface):
        """设置Matlab接口"""
        self.matlab_interface = matlab_interface
