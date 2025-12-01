import pandas as pd
import numpy as np
import os
import matlab
from utils.matlab_interface import MatlabInterface

class FileHandler:
    def __init__(self, matlab_interface=None):
        self.matlab_interface = matlab_interface
    
    def set_matlab_interface(self, matlab_interface):
        """设置Matlab接口"""
        self.matlab_interface = matlab_interface
    
    def read_file(self, file_path):
        """读取不同格式的文件"""
        file_ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_ext in ['.xlsx', '.xls']:
                return self._read_excel(file_path)
            elif file_ext == '.csv':
                return self._read_csv(file_path)
            elif file_ext == '.mat':
                return self._read_mat(file_path)
            else:
                raise ValueError(f"不支持的文件格式: {file_ext}")
        except Exception as e:
            print(f"读取文件 {file_path} 失败: {e}")
            return None
    
    def _read_excel(self, file_path):
        """读取Excel文件"""
        try:
            # 读取所有工作表
            excel_data = pd.read_excel(file_path, sheet_name=None)
            
            # 合并所有工作表的数据
            all_data = []
            for sheet_name, df in excel_data.items():
                # 转换为NumPy数组
                data = df.values
                all_data.append(data)
            
            # 如果只有一个工作表，直接返回该工作表的数据
            if len(all_data) == 1:
                return all_data[0]
            # 否则返回所有工作表的数据列表
            return all_data
        except Exception as e:
            print(f"读取Excel文件失败: {e}")
            return None
    
    def _read_csv(self, file_path):
        """读取CSV文件"""
        try:
            df = pd.read_csv(file_path)
            return df.values
        except Exception as e:
            print(f"读取CSV文件失败: {e}")
            return None
    
    def _read_mat(self, file_path):
        """读取Matlab文件"""
        if not self.matlab_interface:
            print("Matlab接口未设置")
            return None
        
        try:
            # 使用Matlab接口读取.mat文件
            mat_data = self.matlab_interface.load_mat_file(file_path)
            
            # 提取数值数据
            numeric_data = []
            for key, value in mat_data.items():
                # 检查是否为数值数组
                if isinstance(value, (matlab.double, matlab.single)):
                    # 转换为NumPy数组
                    np_array = self.matlab_interface.matlab_to_numpy(value)
                    numeric_data.append(np_array)
            
            # 如果只有一个数值数组，直接返回该数组
            if len(numeric_data) == 1:
                return numeric_data[0]
            # 否则返回所有数值数组的列表
            return numeric_data
        except Exception as e:
            print(f"读取Matlab文件失败: {e}")
            return None
    
    def write_mat_file(self, file_path, data_dict):
        """将数据写入Matlab文件"""
        if not self.matlab_interface:
            print("Matlab接口未设置")
            return False
        
        try:
            # 使用Matlab接口保存数据
            return self.matlab_interface.save_mat_file(file_path, data_dict)
        except Exception as e:
            print(f"写入Matlab文件失败: {e}")
            return False
    
    def convert_to_mat(self, input_file, output_file, data_mapping=None):
        """将其他格式的文件转换为Matlab格式"""
        # 读取输入文件
        data = self.read_file(input_file)
        if data is None:
            return False
        
        # 如果数据是列表（多个工作表或多个变量），只取第一个
        if isinstance(data, list):
            data = data[0]
        
        # 应用数据映射
        if data_mapping:
            mapped_data = self._apply_data_mapping(data, data_mapping)
        else:
            # 默认映射：所有列作为未分类数据
            mapped_data = {'raw_data': data}
        
        # 写入Matlab文件
        return self.write_mat_file(output_file, mapped_data)
    
    def _apply_data_mapping(self, data, data_mapping):
        """应用数据映射"""
        mapped_data = {}
        
        # 加速度数据（最多3列）
        accel_columns = data_mapping.get('acceleration', [])
        if accel_columns:
            mapped_data['acceleration'] = data[:, accel_columns]
        
        # 陀螺仪数据（最多3列）
        gyro_columns = data_mapping.get('gyroscope', [])
        if gyro_columns:
            mapped_data['gyroscope'] = data[:, gyro_columns]
        
        # 噪声数据（1列）
        noise_columns = data_mapping.get('noise', [])
        if noise_columns:
            mapped_data['noise'] = data[:, noise_columns[0]]
        
        # 其他未分类数据
        all_mapped_columns = accel_columns + gyro_columns + noise_columns
        if all_mapped_columns:
            # 找出未映射的列
            all_columns = list(range(data.shape[1]))
            unmapped_columns = [col for col in all_columns if col not in all_mapped_columns]
            if unmapped_columns:
                mapped_data['other_data'] = data[:, unmapped_columns]
        else:
            # 没有映射任何列，将所有数据作为未分类数据
            mapped_data['raw_data'] = data
        
        return mapped_data
    
    def get_file_info(self, file_path):
        """获取文件信息"""
        file_ext = os.path.splitext(file_path)[1].lower()
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
        
        # 读取文件获取数据维度
        data = self.read_file(file_path)
        if data is None:
            return None
        
        if isinstance(data, list):
            # 多个工作表或变量
            data_shape = [d.shape for d in data]
        else:
            # 单个数据集
            data_shape = data.shape
        
        return {
            'file_path': file_path,
            'file_ext': file_ext,
            'file_size': file_size,
            'data_shape': data_shape
        }
