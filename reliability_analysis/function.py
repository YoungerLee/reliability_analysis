import numpy as np
from scipy.special import gamma

def Weibull_pdf(lamda, beta, t):
    '''
    威布尔分布概率密度函数
    :param lamda:尺度参数
    :param beta:形状参数
    :param t: 计算范围
    :return: 概率分布
    '''
    return (beta / lamda) * ((t / lamda) ** (beta - 1)) * np.exp(-(t / lamda) ** beta)

def Weibull_cdf(lamda, beta, t):
    '''
    威布尔分布累积分布函数
    :param lamda:尺度参数
    :param beta:尺度参数
    :param t: 计算范围
    :return: 概率分布
    '''
    return 1 - np.exp(-(t / lamda) ** beta)

def reliability(lamda, beta, t):
    '''
    可靠度函数
    :param lamda:尺度参数
    :param beta:尺度参数
    :param t: 计算范围
    :return: 可靠度函数
    '''
    return np.exp(-(t / lamda) ** beta)

def failure_rate(lamda, beta, t):
    '''
    失效率函数
    :param lamda:尺度参数
    :param beta:尺度参数
    :param t: 计算范围
    :return: 失效率函数
    '''
    return (beta / lamda) * ((t / lamda) ** (beta - 1))

def posterior_function(x, t, mu, sigma):
    '''
    极大后验估计目标函数
    :param x:
    :return:
    '''
    lamda, beta = np.asarray(x)
    t = np.array(t)
    n = t.size
    return -(-np.log(sigma * np.sqrt(2 * np.pi)) -
             (beta - mu) ** 2 / (2 * sigma * sigma) +
             n * (np.log(beta) - np.log(lamda)) +
             (beta - 1) * np.sum(np.log(t)) -
             n * (beta - 1) * np.log(lamda) -
             np.sum((t / lamda) ** beta))

def mtbf(lamda, beta):
    '''
    :param lamda:尺度参数
    :param beta:尺度参数
    :return: mtbf 平均无故障工作时间
    '''
    return lamda * gamma(beta)

def Weibull(x, lamda, beta):
    return 1 - np.exp(-(x / lamda) ** beta)
