function plot_time_domain(data, sample_rate, title_str)
% 绘制时域波形图
% 输入参数：
%   data - 输入数据矩阵，每列代表一个通道
%   sample_rate - 采样率（Hz）
%   title_str - 图表标题

    % 设置默认参数
    if nargin < 2
        sample_rate = 1000;
    end
    if nargin < 3
        title_str = '时域波形图';
    end
    
    % 确保数据是矩阵形式
    if isvector(data)
        data = data(:);
    end
    
    % 获取通道数和数据点数
    [n_points, n_channels] = size(data);
    
    % 计算时间轴
    time = (0:n_points-1) / sample_rate;
    
    % 创建新的图形窗口
    figure('Name', title_str, 'NumberTitle', 'off');
    
    % 绘制每个通道的数据
    for i = 1:n_channels
        subplot(n_channels, 1, i);
        plot(time, data(:, i));
        xlabel('时间 (s)');
        ylabel(['通道 ', num2str(i)]);
        grid on;
        if i == 1
            title(title_str);
        end
    end
    
    % 调整子图间距
    % 使用内置函数替代tightfig
    set(gcf, 'Position', get(gcf, 'Position'));
    
    % 启用交互式工具
    datacursormode on;
    zoom on;
    pan on;
end
