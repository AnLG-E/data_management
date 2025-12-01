# 全周期数据管理系统

## 系统概述

全周期数据管理系统是一个用于传感器数据（加速度、陀螺仪、噪声）的导入、处理、可视化和分析的综合平台。该系统采用Python开发用户界面，结合Matlab强大的数据处理和可视化能力，为用户提供了一个直观、高效的数据管理解决方案。

## 核心功能

### 1. 数据导入与整理
- 支持多种文件格式导入（Excel、CSV、Matlab .mat文件）
- 提供直观的数据列映射界面，允许用户指定各列数据类型
- 实现数据格式统一转换，将所有导入数据转换为Matlab .mat格式
- 支持批量导入和处理多个数据文件

### 2. 数据可视化
- 时域图绘制：显示原始数据的波形
- 频域图绘制：使用pwelch函数计算并显示功率谱密度
- 交互式图表操作：支持缩放、平移、数据游标等功能
- 支持多通道数据同时可视化

### 3. 数据处理与分析
- 数据预处理：去噪、滤波等
- 特征提取：支持多种特征提取算法
- 数据统计分析：提供基本的统计信息

### 4. 数据管理
- 数据保存与导出
- 数据查询与检索
- 项目管理功能

## 技术架构

### 整体架构
- **前端**：Python GUI（PyQt5）
- **后端**：Matlab 引擎（用于数据处理和绘图）
- **数据交互**：MATLAB Engine for Python
- **数据存储**：Matlab .mat 文件格式

### 模块划分

```
data_management_system/
├── python_gui/                 # Python GUI代码
│   ├── main_window.py          # 主界面
│   ├── data_import_dialog.py   # 数据导入对话框
│   ├── visualization_panel.py  # 可视化面板
│   ├── data_mapping_widget.py  # 数据列映射组件
│   └── utils/                  # 工具函数
│       ├── file_handler.py     # 文件处理工具
│       └── matlab_interface.py # Matlab引擎接口
├── matlab_functions/           # Matlab函数
│   ├── data_processing/        # 数据处理函数
│   └── visualization/          # 可视化函数
│       ├── plot_time_domain.m  # 时域图绘制
│       └── plot_freq_domain.m  # 频域图绘制
├── examples/                   # 示例数据和使用案例
└── README.md                   # 系统说明文档
```

## 安装与配置

### 系统要求
- Python 3.9-3.12（MATLAB Engine for Python仅支持这些版本）
- Matlab 2018a+（已安装Signal Processing Toolbox）
- Windows 10/11 操作系统
- 不使用conda进行包管理和环境管理

### 依赖包安装

1. **创建虚拟环境**（推荐使用venv）：

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

2. **安装Python依赖包**：

```bash
pip install PyQt5 numpy pandas
```

3. **安装MATLAB Engine for Python**：

```bash
# 在Matlab命令窗口中执行
cd(fullfile(matlabroot, 'extern', 'engines', 'python'))
system('python setup.py install')
```

**注意**：
- MATLAB Engine for Python仅支持Python 3.9, 3.10, 3.11和3.12版本
- 请确保您的Python版本与Matlab兼容
- 所有依赖项均使用pip安装，不使用conda

## 使用说明

### 1. 启动系统

运行主程序：

```bash
python main_window.py
```

### 2. 导入数据

1. 点击菜单栏的"文件" -> "导入数据"，或使用快捷键Ctrl+I
2. 在弹出的对话框中选择要导入的数据文件
3. 系统会自动读取文件并显示数据预览
4. 在"数据列映射"区域，为每列数据指定类型（加速度、陀螺仪或噪声）
5. 点击"导入"按钮，系统会将数据转换为Matlab .mat格式并保存

### 3. 数据可视化

1. 在左侧的"数据文件"列表中选择要可视化的数据文件
2. 在右侧的"数据映射"面板中查看数据信息
3. 在中央的"可视化面板"中选择要绘制的图表类型（时域图或频域图）
4. 设置数据类型、通道和采样率等参数
5. 点击"绘制图表"按钮，系统会调用Matlab引擎绘制图表
6. 使用Matlab的交互式工具对图表进行操作

### 4. 数据处理与分析

1. 在菜单栏的"数据"菜单中选择相应的数据处理功能
2. 根据提示设置处理参数
3. 系统会调用Matlab引擎进行数据处理
4. 处理结果会显示在界面上或保存到文件中

## 系统特点

1. **跨平台兼容性**：Python和Matlab均支持多平台
2. **强大的数据处理能力**：利用Matlab的信号处理工具箱
3. **友好的用户界面**：基于PyQt5的现代化GUI设计
4. **良好的可扩展性**：模块化设计，便于功能扩展
5. **高效的数据交互**：使用MATLAB Engine实现无缝集成
6. **支持多种数据格式**：Excel、CSV、Matlab .mat文件
7. **交互式数据可视化**：提供丰富的图表操作功能

## 开发说明

### 代码结构

- **main_window.py**：主界面，整合所有模块
- **data_import_dialog.py**：数据导入对话框，用于文件选择和数据映射
- **visualization_panel.py**：可视化面板，用于绘制时域图和频域图
- **data_mapping_widget.py**：数据映射组件，用于显示和管理数据映射关系
- **matlab_interface.py**：Matlab引擎接口，用于Python和Matlab之间的通信
- **file_handler.py**：文件处理工具，用于读取和转换不同格式的文件

### 扩展开发

1. **添加新的数据处理功能**：
   - 在matlab_functions/data_processing/目录下创建新的Matlab函数
   - 在Python GUI中添加相应的调用接口

2. **添加新的可视化类型**：
   - 在matlab_functions/visualization/目录下创建新的Matlab绘图函数
   - 在visualization_panel.py中添加相应的选项卡和参数设置

3. **支持新的文件格式**：
   - 在file_handler.py中添加相应的文件读取和转换方法

## 故障排除

### 1. Matlab引擎启动失败

- 确保Matlab已正确安装
- 确保已正确安装MATLAB Engine for Python
- 检查Matlab的安装路径是否已添加到系统环境变量

### 2. 数据导入失败

- 检查文件格式是否支持
- 检查文件内容是否符合预期格式
- 确保文件路径中不包含中文或特殊字符

### 3. 可视化功能异常

- 确保Matlab的Signal Processing Toolbox已安装
- 检查数据格式是否正确
- 确保Matlab引擎已正确启动

## 版本历史

- **v1.0.0**：初始版本
  - 实现数据导入与整理功能
  - 实现时域图和频域图可视化
  - 实现基本的数据管理功能

## 许可证

本项目采用MIT许可证，详情请参考LICENSE文件。

## 联系方式

如有问题或建议，请联系项目维护人员。

## 致谢

感谢所有为该项目做出贡献的人员。
