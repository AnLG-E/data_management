import matlab.engine
import numpy as np
import os

class MatlabInterface:
    def __init__(self):
        self.eng = None
        self.matlab_functions_path = None
    
    def start_engine(self):
        """启动Matlab引擎"""
        try:
            self.eng = matlab.engine.start_matlab()
            return True
        except Exception as e:
            print(f"启动Matlab引擎失败: {e}")
            return False
    
    def stop_engine(self):
        """关闭Matlab引擎"""
        if self.eng:
            try:
                self.eng.quit()
                self.eng = None
                return True
            except Exception as e:
                print(f"关闭Matlab引擎失败: {e}")
                return False
        return True
    
    def set_functions_path(self, path):
        """设置Matlab函数路径"""
        self.matlab_functions_path = path
        if self.eng:
            try:
                # 添加主目录和子目录到Matlab路径
                self.eng.addpath(self.eng.genpath(path))
                return True
            except Exception as e:
                print(f"设置Matlab函数路径失败: {e}")
                return False
        return False
    
    def call_function(self, func_name, *args, **kwargs):
        """调用Matlab函数"""
        if not self.eng:
            print("Matlab引擎未启动")
            return None
        
        try:
            # 调用Matlab函数
            result = getattr(self.eng, func_name)(*args, **kwargs)
            return result
        except Exception as e:
            print(f"调用Matlab函数 {func_name} 失败: {e}")
            return None
    
    def numpy_to_matlab(self, np_array):
        """将NumPy数组转换为Matlab数组"""
        # 确保数组是浮点类型
        np_array = np_array.astype(float)
        
        # 转换为Matlab数组
        if len(np_array.shape) == 1:
            # 一维数组
            return matlab.double(np_array.tolist())
        elif len(np_array.shape) == 2:
            # 二维数组，Matlab是列优先，需要转置
            return matlab.double(np_array.T.tolist())
        else:
            print("不支持的数组维度")
            return None
    
    def matlab_to_numpy(self, mat_array):
        """将Matlab数组转换为NumPy数组"""
        if isinstance(mat_array, (matlab.double, matlab.single)):
            # 转换为NumPy数组，注意Matlab是列优先，需要转置
            return np.array(mat_array._data).reshape(mat_array.size, order='F')
        elif isinstance(mat_array, list):
            # 如果是列表，直接转换
            return np.array(mat_array)
        else:
            print(f"不支持的Matlab数据类型: {type(mat_array)}")
            return None
    
    def load_mat_file(self, file_path):
        """加载Matlab .mat文件"""
        if not self.eng:
            print("Matlab引擎未启动")
            return None
        
        try:
            # 使用Matlab的load函数加载文件
            data = self.eng.load(file_path, nargout=1)
            return data
        except Exception as e:
            print(f"加载Matlab文件失败: {e}")
            return None
    
    def save_mat_file(self, file_path, data_dict):
        """保存数据到Matlab .mat文件"""
        if not self.eng:
            print("Matlab引擎未启动")
            return False
        
        try:
            # 将数据字典中的所有变量传递给Matlab工作区
            for key, value in data_dict.items():
                if isinstance(value, np.ndarray):
                    # 转换NumPy数组为Matlab数组
                    mat_value = self.numpy_to_matlab(value)
                    self.eng.workspace[key] = mat_value
                else:
                    # 直接传递其他类型
                    self.eng.workspace[key] = value
            
            # 保存工作区变量到文件
            self.eng.save(file_path, '-v7.3', nargout=0)
            return True
        except Exception as e:
            print(f"保存Matlab文件失败: {e}")
            return False
    
    def plot_time_domain(self, data, sample_rate=1000, title="时域图"):
        """绘制时域图"""
        if not self.eng:
            print("Matlab引擎未启动")
            return False
        
        try:
            # 转换数据为Matlab格式
            mat_data = self.numpy_to_matlab(data)
            
            # 调用Matlab绘图函数
            self.eng.plot_time_domain(mat_data, sample_rate, title, nargout=0)
            return True
        except Exception as e:
            print(f"绘制时域图失败: {e}")
            return False
    
    def plot_freq_domain(self, data, sample_rate=1000, title="频域图"):
        """绘制频域图"""
        if not self.eng:
            print("Matlab引擎未启动")
            return False
        
        try:
            # 转换数据为Matlab格式
            mat_data = self.numpy_to_matlab(data)
            
            # 调用Matlab绘图函数
            self.eng.plot_freq_domain(mat_data, sample_rate, title, nargout=0)
            return True
        except Exception as e:
            print(f"绘制频域图失败: {e}")
            return False
