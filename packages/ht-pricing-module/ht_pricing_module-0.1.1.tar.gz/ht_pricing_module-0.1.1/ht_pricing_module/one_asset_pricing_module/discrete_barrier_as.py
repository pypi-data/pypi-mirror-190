import numpy as np
import math
from .one_asset_option_base import OneAssetOptionBase
from .barrier import Barrier
from .vanilla import Vanilla
from ht_pricing_module.api_and_utils.api import ExerciseType, KnockType, BarrierType
from ht_pricing_module.api_and_utils.utils import Struct


class DiscreteBarrierAs(OneAssetOptionBase):
    # 离散障碍解析解

    def __init__(self, param):
        super().__init__(param)
        dt = self.param.obs_freq / self.param.year_base
        if (self.param.barrier_price > self.param.spot_price) or\
                (self.param.barrier_type == BarrierType.UP and self.param.barrier_price == self.param.spot_price):
            self.param.barrier_price = self.param.barrier_price * np.exp(0.5826 * self.param.volatility * math.sqrt(dt))
        elif (self.param.barrier_price < self.param.spot_price) or\
                (self.param.barrier_type == BarrierType.DOWN and self.param.barrier_price == self.param.spot_price):
            self.param.barrier_price = self.param.barrier_price * np.exp(-0.5826 * self.param.volatility * math.sqrt(dt))

    def __calculate_present_value__(self) -> float:
        rst = 0
        if self.param.knock_type == KnockType.OUT:
            if self.param.barrier_type == BarrierType.UP and self.param.spot_price >= self.param.barrier_price:
                return self.param.payoff
            elif self.param.barrier_type == BarrierType.DOWN and self.param.spot_price <= self.param.barrier_price:
                return self.param.payoff
        elif self.param.knock_type == KnockType.IN:
            if (self.param.barrier_type == BarrierType.UP and self.param.spot_price >= self.param.barrier_price) or\
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
                vanilla = Vanilla(param)
                return vanilla.present_value()

        param = Struct({})
        param['option_type'] = self.param.option_type
        param['exercise_type'] = ExerciseType.EUROPEAN
        param['spot_price'] = self.param.spot_price
        param['strike_price'] = self.param.strike_price
        param['barrier_price'] = self.param.barrier_price
        param['riskfree_rate'] = self.param.riskfree_rate
        param['dividend'] = self.param.dividend
        param['volatility'] = self.param.volatility
        param['expiry_date'] = self.param.expiry_date
        param['current_date'] = self.param.current_date
        param['year_base'] = int(self.param.year_base)
        param['barrier_type'] = self.param.barrier_type
        param['knock_type'] = self.param.knock_type
        param['is_knock_in'] = self.param.is_knock_in
        param['payoff'] = self.param.payoff
        pricer = Barrier(param)
        return pricer.present_value()
