import math
from scipy.stats import norm
from .one_asset_option_base import OneAssetOptionBase
from .exceptions import *
from ht_pricing_module.api_and_utils.api import ExerciseType, OptionType


class Binary(OneAssetOptionBase):

    def __european(self):
        rst = 0
        cp = {OptionType.CALL: 1, OptionType.PUT: -1}[self.param.option_type]
        time_to_expiry = float(self.param.expiry_date - self.param.current_date) / float(self.param.year_base)
        if time_to_expiry <= 0:
            rst = self.param.payoff if cp * (self.param.spot_price - self.param.strike_price) >= 0 else 0
        else:
            t_adj_vol = self.param.volatility * math.sqrt(time_to_expiry)
            d1 = (math.log(self.param.spot_price / self.param.strike_price) + (self.param.riskfree_rate - self.param.dividend + math.pow(self.param.volatility, 2) / 2.0) * time_to_expiry) / t_adj_vol
            d2 = d1 - t_adj_vol
            rst = self.param.payoff * math.exp(-1 * self.param.riskfree_rate * time_to_expiry) * norm.cdf(cp * d2)
        return rst

    def __american(self):
        rst = 0
        cp = {OptionType.CALL: 1, OptionType.PUT: -1}[self.param.option_type]
        time_to_expiry = float(self.param.expiry_date - self.param.current_date) / float(self.param.year_base)
        if time_to_expiry <= 0:
            rst = self.param.payoff if cp * (self.param.spot_price - self.param.strike_price) >= 0 else 0
        elif cp * (self.param.spot_price - self.param.strike_price) >= 0:
            rst = self.param.payoff
        else:
            t_adj_vol = self.param.volatility * math.sqrt(time_to_expiry)
            v = self.param.riskfree_rate - self.param.dividend - math.pow(self.param.volatility, 2) / 2.0
            ar = math.sqrt(math.pow(v, 2) + 2 * self.param.riskfree_rate * math.pow(self.param.volatility, 2))
            qr1 = (v + ar) / math.pow(self.param.volatility, 2)
            qr2 = (v - ar) / math.pow(self.param.volatility, 2)
            Qr1 = (math.log(self.param.strike_price / self.param.spot_price) + time_to_expiry * ar) / t_adj_vol
            Qr2 = (math.log(self.param.strike_price / self.param.spot_price) - time_to_expiry * ar) / t_adj_vol
            rst = self.param.payoff * math.pow(self.param.strike_price / self.param.spot_price, qr1) * norm.cdf(-1 * cp * Qr1) +\
                  self.param.payoff * math.pow(self.param.strike_price / self.param.spot_price, qr2) * norm.cdf(-1 * cp * Qr2)
        return rst

    def __calculate_present_value__(self):
        if self.param.option_type not in (OptionType.CALL, OptionType.PUT):
            raise InvalidOptionTypeError()

        if self.param.exercise_type == ExerciseType.EUROPEAN:
            return self.__european()
        elif self.param.exercise_type == ExerciseType.AMERICAN:
            return self.__american()
        else:
            raise InvalidExerciseTypeError()