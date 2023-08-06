import math
import numpy as np
from .one_asset_option_base import OneAssetOptionBase
from ht_pricing_module.monte_carlo_engine.mc_path_generator import McPathGenerator
from .vanilla import Vanilla
from ht_pricing_module.api_and_utils.api import ExerciseType, OptionType, KnockType, BarrierType
from ht_pricing_module.api_and_utils.utils import Struct


class DiscreteBarrierMc(OneAssetOptionBase):

    def __calculate_present_value__(self) -> float:
        if self.param.is_knock_in and self.param.knock_type == KnockType.IN:
            # vanilla
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
            vanilla = Vanilla(param)
            return vanilla.present_value()
        else:
            # mc
            intraday = round(math.ceil(self.param.current_date) - self.param.current_date, 4)
            return self.mc_barrier(
                option_type=self.param.option_type,
                knock_type=self.param.knock_type,
                barrier_type=self.param.barrier_type,
                spot_price=self.param.spot_price,
                strike_price=self.param.strike_price,
                barrier_price=self.param.barrier_price,
                payoff=self.param.payoff,
                riskfree_rate=self.param.riskfree_rate,
                dividend=self.param.dividend,
                vol=self.param.volatility,
                intraday=intraday,
                expiry_date=self.param.expiry_date - math.ceil(self.param.current_date) + math.ceil(intraday),
                year_base=self.param.year_base,
                obs=[obs.obs_index - math.ceil(self.param.current_date) + math.ceil(intraday) for obs in self.param.obs_date]
            )

    def mc_barrier(self, option_type, knock_type, barrier_type, spot_price, strike_price, barrier_price, payoff,
                   riskfree_rate, dividend, vol, intraday, expiry_date, year_base, obs):

        cp = {OptionType.CALL: 1, OptionType.PUT: -1}[option_type]
        io = {KnockType.IN: 1, KnockType.OUT: -1}[knock_type]
        ud = {BarrierType.UP: 1, BarrierType.DOWN: -1}[barrier_type]
        rst = 0

        if expiry_date <= 0:
            knock = 1 if ud * (spot_price - barrier_price) >= 0 else -1
            if knock * io == 1:
                rst = max(cp * (spot_price - strike_price), 0)
            elif knock * io == -1:
                rst = (0 if io == 1 else 1) * payoff
        else:
            residual_intraday = round(1 - intraday, 4) if round(1 - intraday, 4) < 1 else round(1 - intraday, 4) - 1
            generator = McPathGenerator(riskfree_rate=riskfree_rate, dividend=dividend, vol=vol,
                                        intraday=residual_intraday, expiry_date=expiry_date, year_base=year_base,
                                        random_seed=0)

            price = spot_price * generator.generate()
            obs_arr = np.array(obs).astype(int)
            obs_arr = obs_arr[obs_arr >= 0]

            knock_flag = ud * (price[:, obs_arr] - barrier_price) >= 0
            knock_index = (np.insert(knock_flag, 0, np.zeros(len(knock_flag)), axis=1)).argmax(axis=1)

            if io == 1:
                knock_index = np.where(knock_index > 0, 1, 0)
                discount_factor = np.exp(-1 * riskfree_rate * (expiry_date - residual_intraday) / year_base)
                value = np.multiply(knock_index.T, np.maximum(cp * (price[:, -1] - strike_price), 0))
                value = value + np.multiply((1 - knock_index).T, payoff)
                rst = np.mean(discount_factor * value)
            else:
                discount_factor_arr = np.exp(-1 * riskfree_rate * (obs_arr - residual_intraday) / year_base)
                discount_factor_arr = np.insert(discount_factor_arr, 0, 0)[knock_index]
                discount_factor = np.exp(-1 * riskfree_rate * (expiry_date - residual_intraday) / year_base)
                knock_index = np.where(knock_index > 0, 1, 0)
                value = np.multiply(discount_factor_arr.T, payoff * knock_index)
                value = value + discount_factor * np.multiply((1 - knock_index).T, np.maximum(cp * (price[:, -1] - strike_price), 0))
                rst = np.mean(value)
        return rst
