import sys
import os
import numpy as np

# 检查Python版本
required_versions = [3, 9], [3, 10], [3, 11], [3, 12]
current_version = [sys.version_info.major, sys.version_info.minor]

if current_version not in required_versions:
    print(f"警告：当前Python版本 {sys.version_info.major}.{sys.version_info.minor} 可能不兼容MATLAB Engine for Python")
    print(f"推荐使用Python版本：{', '.join([f'{v[0]}.{v[1]}' for v in required_versions])}")

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(__file__))

# 尝试导入自定义模块
try:
    from utils.matlab_interface import MatlabInterface
    from utils.file_handler import FileHandler
    MATLAB_AVAILABLE = True
except ImportError as e:
    print(f"警告：无法导入某些模块：{e}")
    MATLAB_AVAILABLE = False

def test_matlab_interface():
    """测试Matlab接口"""
    print("测试Matlab接口...")
    
    if not MATLAB_AVAILABLE:
        print("✗ Matlab相关模块未导入，跳过Matlab接口测试")
        return
    
    # 创建Matlab接口实例
    matlab_interface = MatlabInterface()
    
    # 启动Matlab引擎
    if matlab_interface.start_engine():
        print("✓ Matlab引擎启动成功")
        
        # 设置Matlab函数路径
        matlab_functions_path = os.path.join(os.path.dirname(__file__), "..", "matlab_functions")
        if matlab_interface.set_functions_path(matlab_functions_path):
            print("✓ Matlab函数路径设置成功")
        else:
            print("✗ Matlab函数路径设置失败")
        
        # 测试简单的Matlab函数调用
        result = matlab_interface.call_function('sqrt', 16.0)
        if result == 4.0:
            print("✓ Matlab函数调用成功")
        else:
            print(f"✗ Matlab函数调用失败，结果: {result}")
        
        # 关闭Matlab引擎
        if matlab_interface.stop_engine():
            print("✓ Matlab引擎关闭成功")
        else:
            print("✗ Matlab引擎关闭失败")
    else:
        print("✗ Matlab引擎启动失败")

def test_file_handler():
    """测试文件处理器"""
    print("\n测试文件处理器...")
    
    if not MATLAB_AVAILABLE:
        print("✗ Matlab相关模块未导入，跳过文件处理器测试")
        return
    
    # 创建Matlab接口实例
    matlab_interface = MatlabInterface()
    
    # 启动Matlab引擎
    if matlab_interface.start_engine():
        # 创建文件处理器实例
        file_handler = FileHandler(matlab_interface)
        
        # 创建测试数据
        test_data = np.random.rand(100, 6)  # 100行6列的随机数据
        
        # 测试数据映射
        data_mapping = {
            'acceleration': [0, 1, 2],  # 前3列作为加速度数据
            'gyroscope': [3, 4, 5],      # 后3列作为陀螺仪数据
            'noise': []                  # 没有噪声数据
        }
        
        # 应用数据映射
        mapped_data = file_handler._apply_data_mapping(test_data, data_mapping)
        if 'acceleration' in mapped_data and 'gyroscope' in mapped_data:
            print("✓ 数据映射功能正常")
        else:
            print("✗ 数据映射功能异常")
        
        # 关闭Matlab引擎
        matlab_interface.stop_engine()
    else:
        print("✗ 无法启动Matlab引擎，跳过文件处理器测试")

def test_data_import():
    """测试数据导入功能"""
    print("\n测试数据导入功能...")
    
    # 创建测试数据文件（CSV格式）
    test_csv_file = "test_data.csv"
    test_data = np.random.rand(100, 6)
    np.savetxt(test_csv_file, test_data, delimiter=",")
    
    if not MATLAB_AVAILABLE:
        print("✗ Matlab相关模块未导入，跳过数据导入测试")
        # 删除测试CSV文件
        if os.path.exists(test_csv_file):
            os.remove(test_csv_file)
        return
    
    # 创建Matlab接口实例
    matlab_interface = MatlabInterface()
    
    # 启动Matlab引擎
    if matlab_interface.start_engine():
        # 创建文件处理器实例
        file_handler = FileHandler(matlab_interface)
        
        # 测试读取CSV文件
        csv_data = file_handler.read_file(test_csv_file)
        if csv_data is not None and csv_data.shape == (100, 6):
            print("✓ CSV文件读取成功")
        else:
            print("✗ CSV文件读取失败")
        
        # 转换为Matlab格式
        output_mat_file = "test_data_converted.mat"
        success = file_handler.convert_to_mat(
            test_csv_file, output_mat_file, {
                'acceleration': [0, 1, 2],
                'gyroscope': [3, 4, 5],
                'noise': []
            }
        )
        
        if success and os.path.exists(output_mat_file):
            print("✓ 文件格式转换成功")
            # 删除测试文件
            os.remove(output_mat_file)
        else:
            print("✗ 文件格式转换失败")
        
        # 关闭Matlab引擎
        matlab_interface.stop_engine()
    else:
        print("✗ 无法启动Matlab引擎，跳过数据导入测试")
    
    # 删除测试CSV文件
    if os.path.exists(test_csv_file):
        os.remove(test_csv_file)

def test_python_only_features():
    """测试仅使用Python的功能"""
    print("\n测试仅使用Python的功能...")
    
    # 测试数据映射功能（不依赖Matlab）
    test_data = np.random.rand(100, 6)  # 100行6列的随机数据
    
    # 模拟数据映射逻辑
    data_mapping = {
        'acceleration': [0, 1, 2],  # 前3列作为加速度数据
        'gyroscope': [3, 4, 5],      # 后3列作为陀螺仪数据
        'noise': []                  # 没有噪声数据
    }
    
    # 应用数据映射
    mapped_data = {}
    if data_mapping['acceleration']:
        mapped_data['acceleration'] = test_data[:, data_mapping['acceleration']]
    if data_mapping['gyroscope']:
        mapped_data['gyroscope'] = test_data[:, data_mapping['gyroscope']]
    if data_mapping['noise']:
        mapped_data['noise'] = test_data[:, data_mapping['noise'][0]]
    
    if 'acceleration' in mapped_data and 'gyroscope' in mapped_data:
        print("✓ 数据映射逻辑测试成功")
    else:
        print("✗ 数据映射逻辑测试失败")
    
    # 测试数据形状
    if mapped_data['acceleration'].shape == (100, 3) and mapped_data['gyroscope'].shape == (100, 3):
        print("✓ 数据形状测试成功")
    else:
        print("✗ 数据形状测试失败")

def main():
    """主测试函数"""
    print("开始测试全周期数据管理系统...")
    print("=" * 50)
    
    # 测试仅使用Python的功能
    test_python_only_features()
    
    # 测试Matlab接口
    test_matlab_interface()
    
    # 测试文件处理器
    test_file_handler()
    
    # 测试数据导入
    test_data_import()
    
    print("\n" + "=" * 50)
    print("测试完成！")

if __name__ == "__main__":
    main()
