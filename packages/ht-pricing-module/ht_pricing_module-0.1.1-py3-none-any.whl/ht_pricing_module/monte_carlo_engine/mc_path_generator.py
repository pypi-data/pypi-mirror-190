import numpy as np
from scipy.stats import qmc


class McPathGenerator:
    def __init__(self,
                 riskfree_rate,
                 dividend,
                 vol,
                 intraday,  # 日内时间
                 expiry_date,  # 到日期离当前日收盘天数
                 year_base,
                 path_num=100000,  # 路径数量
                 antithetic_flag=True,  # 对偶变量
                 qmc_flag=True,  # quasi-monte carlo
                 random_seed=None
                 ):
        self.year_base = float(year_base)
        self.path_num = path_num
        self.antithetic_flag = antithetic_flag
        self.qmc_flag = qmc_flag
        self.random_seed = random_seed

        self.drift = riskfree_rate - dividend - 0.5 * vol ** 2
        self.sigma = vol
        self.t_arr = np.arange(1, expiry_date + 1, 1) - intraday
        self.t_arr = np.hstack([0, self.t_arr])
        self.dt_arr = (self.t_arr[1:] - self.t_arr[:-1]) / self.year_base

    def generate_randn(self, qmc_flag, antithetic_flag, random_seed, M, N):
        if qmc_flag:
            _mean_dem = [0] * N
            _qmc_engine = qmc.Sobol(N, seed=random_seed)
            _randn = qmc.MultivariateNormalQMC(mean=_mean_dem, cov=np.eye(len(_mean_dem)), seed=random_seed,
                                               engine=_qmc_engine).random(M)
        else:
            np.random.seed(random_seed)
            _randn = np.random.randn(M, N)
        if antithetic_flag:
            _randn = np.vstack([_randn, -_randn])
        return _randn

    def generate(self):
        randn = self.generate_randn(self.qmc_flag, self.antithetic_flag, self.random_seed, self.path_num, len(self.dt_arr))
        log_rtn = self.drift * self.dt_arr + self.sigma * np.sqrt(self.dt_arr) * randn
        cum_log_rtn = np.cumsum(log_rtn, axis=1)
        cum_log_rtn = np.hstack([np.zeros([len(cum_log_rtn), 1]), cum_log_rtn])
        return np.exp(cum_log_rtn)
