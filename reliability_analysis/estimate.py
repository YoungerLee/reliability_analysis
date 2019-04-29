from reliability_analysis.function import *
import numpy as np
from scipy.optimize import minimize

def map_estimate(x0):
    '''
    使用极大后验估计法估计威布尔分布的参数
    :param x0: 优化初始值，带入最小二乘法的结果
    :return: 优化后的参数
    '''
    x0 = np.array(x0)
    res = minimize(posterior_function, x0, method='Nelder-Mead', tol=1e-7)
    return res.x

def map_estimate_2(x0):
    '''
    使用极大后验估计法估计威布尔分布的参数
    :param x0: 优化初始值，带入最小二乘法的结果
    :return: 优化后的参数
    '''
    x0 = np.array(x0)
    res = minimize(posterior_function_2, x0, method='Nelder-Mead', tol=1e-7)
    return res.x

def least_square(t):
    '''
    使用最小二乘法估计威布尔分布的参数
    :param t: 故障工作时间间隔
    :return:alpha尺度参数 beta形状参数
    '''
    #中位秩是在 N 个单元样本第 j 次失效时真实失效概率在 50% 的置信水平上应具有的值，或者是不可靠性的最佳估计值。此估计值是基于二项方程的解
    n = len(t)
    i = np.arange(1, n + 1 ,1)
    F = (i - 0.3) / (n + 0.4)
    # F = 1 - exp(-(t / 686.5).^1.609);
    # 取对数线性化
    x = np.log(t)
    y = np.log(np.log(1 / (1 - F)))
    # 计算最小二乘解
    loss_xx = np.dot((x - np.mean(x)), (x - np.mean(x)).T)
    loss_xy = np.dot((x - np.mean(x)), (y - np.mean(y)).T)
    b = loss_xy / loss_xx
    a = np.mean(y) - b * np.mean(x)
    beta_hat = b
    lambda_hat = np.exp(-a / b)
    beta_std = np.sqrt(1 / loss_xx * np.dot(a * x + b - y, (a * x + b - y).T) / (n - 2))
    return lambda_hat, beta_hat, beta_std


if __name__ == "__main__":
    print(map_estimate([532.94338156,1.73033109]))