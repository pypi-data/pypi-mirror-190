import numpy as np
import math
from scipy.stats import norm
from .one_asset_option_base import OneAssetOptionBase
from .vanilla import Vanilla
from ht_pricing_module.api_and_utils.api import ExerciseType, OptionType, KnockType, BarrierType
from ht_pricing_module.api_and_utils.utils import Struct


class Barrier(OneAssetOptionBase):

    def __calculate_present_value__(self) -> float:
        rst = 0
        cp = {OptionType.CALL: 1, OptionType.PUT: -1}[self.param.option_type]
        du = {BarrierType.DOWN: 1, BarrierType.UP: -1}[self.param.barrier_type]
        time_to_expiry = float(self.param.expiry_date - self.param.current_date) / float(self.param.year_base)

        if time_to_expiry <= 0:
            if self.param.knock_type == KnockType.IN:
                if self.param.is_knock_in:
                    return max(cp * (self.param.spot_price - self.param.strike_price), 0)
                else:
                    if self.param.barrier_type == BarrierType.DOWN:
                        if self.param.spot_price <= self.param.barrier_price:
                            return max(cp * (self.param.spot_price - self.param.strike_price), 0)
                        else:
                            return self.param.payoff
                    elif self.param.barrier_type == BarrierType.UP:
                        if self.param.spot_price >= self.param.barrier_price:
                            return max(cp * (self.param.spot_price - self.param.strike_price), 0)
                        else:
                            return self.param.payoff
            elif self.param.knock_type == KnockType.OUT:
                if self.param.barrier_type == BarrierType.DOWN:
                    if self.param.spot_price > self.param.barrier_price:
                        return max(cp * (self.param.spot_price - self.param.strike_price), 0)
                    else:
                        return self.param.payoff
                elif self.param.barrier_type == BarrierType.UP:
                    if self.param.spot_price < self.param.barrier_price:
                        return max(cp * (self.param.spot_price - self.param.strike_price), 0)
                    else:
                        return self.param.payoff
        else:
            if self.param.knock_type == KnockType.IN:
                if self.param.is_knock_in or\
                        (self.param.barrier_type == BarrierType.UP and self.param.spot_price >= self.param.barrier_price) or\
                        (self.param.barrier_type == BarrierType.DOWN and self.param.spot_price <= self.param.barrier_price):

                    param = Struct({})
                    param['option_type'] = self.param.option_type
                    param['exercise_type'] = ExerciseType.EUROPEAN
                    param['spot_price'] = self.param.spot_price
                    param['strike_price'] = self.param.strike_price
                    param['expiry_date'] = self.param.expiry_date
                    param['current_date'] = self.param.current_date
                    param['volatility'] = self.param.volatility
                    param['riskfree_rate'] = self.param.riskfree_rate
                    param['dividend'] = self.param.dividend
                    param['year_base'] = int(self.param.year_base)
                    pricer = Vanilla(param)
                    return pricer.present_value()
            elif self.param.knock_type == KnockType.OUT:
                if (self.param.barrier_type == BarrierType.UP and self.param.spot_price >= self.param.barrier_price) or\
                        (self.param.barrier_type == BarrierType.DOWN and self.param.spot_price <= self.param.barrier_price):
                    return self.param.payoff

            t_adj_vol = self.param.volatility * math.sqrt(time_to_expiry)
            exp_q_t = np.exp(-1 * self.param.dividend * time_to_expiry)
            exp_r_t = np.exp(-1 * self.param.riskfree_rate * time_to_expiry)
            vol_sq = math.pow(self.param.volatility, 2)
            ba_d_sp = self.param.barrier_price / self.param.spot_price

            mu = (self.param.riskfree_rate - self.param.dividend - vol_sq / 2) / vol_sq
            lamda = math.sqrt(math.pow(mu, 2) + 2 * self.param.riskfree_rate / vol_sq)

            x1 = np.log(self.param.spot_price / self.param.strike_price) / t_adj_vol + (1 + mu) * t_adj_vol
            x2 = np.log(self.param.spot_price / self.param.barrier_price) / t_adj_vol + (1 + mu) * t_adj_vol
            y1 = np.log(math.pow(self.param.barrier_price, 2) / (self.param.spot_price * self.param.strike_price)) / t_adj_vol + (1 + mu) * t_adj_vol
            y2 = np.log(ba_d_sp) / t_adj_vol + (1 + mu) * t_adj_vol
            z = np.log(ba_d_sp) / t_adj_vol + lamda * t_adj_vol

            A = cp * self.param.spot_price * exp_q_t * norm.cdf(cp * x1) - \
                cp * self.param.strike_price * exp_r_t * norm.cdf(cp * x1 - cp * t_adj_vol)
            B = cp * self.param.spot_price * exp_q_t * norm.cdf(cp * x2) - \
                cp * self.param.strike_price * exp_r_t * norm.cdf(cp * x2 - cp * t_adj_vol)

            C = cp * self.param.spot_price * exp_q_t * math.pow(ba_d_sp, 2 * (mu + 1)) * norm.cdf(du * y1) - \
                cp * self.param.strike_price * exp_r_t * math.pow(ba_d_sp, 2 * mu) * norm.cdf(du * y1 - du * t_adj_vol)
            D = cp * self.param.spot_price * exp_q_t * math.pow(ba_d_sp, 2 * (mu + 1)) * norm.cdf(du * y2) - \
                cp * self.param.strike_price * exp_r_t * math.pow(ba_d_sp, 2 * mu) * norm.cdf(du * y2 - du * t_adj_vol)

            E = self.param.payoff * exp_r_t * (norm.cdf(du * x2 - du * t_adj_vol) -
                                               math.pow(ba_d_sp, 2 * mu) * norm.cdf(du * y2 - du * t_adj_vol))
            F = self.param.payoff * (math.pow(ba_d_sp, mu + lamda) * norm.cdf(du * z) +
                                     math.pow(ba_d_sp, mu - lamda) * norm.cdf(du * z - 2 * du * lamda * t_adj_vol))

            cp = {OptionType.CALL: 'c', OptionType.PUT: 'p'}[self.param.option_type]
            du = {BarrierType.DOWN: 'd', BarrierType.UP: 'u'}[self.param.barrier_type]
            io = {KnockType.IN: 'i', KnockType.OUT: 'o'}[self.param.knock_type]

            rst = {'cdi': C + E if self.param.strike_price >= self.param.barrier_price else A - B + D + E,
                   'cui': A + E if self.param.strike_price >= self.param.barrier_price else B - C + D + E,
                   'pdi': B - C + D + E if self.param.strike_price >= self.param.barrier_price else A + E,
                   'pui': A - B + D + E if self.param.strike_price >= self.param.barrier_price else C + E,
                   'cdo': A - C + F if self.param.strike_price >= self.param.strike_price else B - D + F,
                   'cuo': F if self.param.strike_price >= self.param.barrier_price else A - B + C - D + F,
                   'pdo': A - B + C - D + F if self.param.strike_price >= self.param.barrier_price else F,
                   'puo': B - D + F if self.param.strike_price >= self.param.barrier_price else A - C + F}[f'{cp}{du}{io}']
        return rst
