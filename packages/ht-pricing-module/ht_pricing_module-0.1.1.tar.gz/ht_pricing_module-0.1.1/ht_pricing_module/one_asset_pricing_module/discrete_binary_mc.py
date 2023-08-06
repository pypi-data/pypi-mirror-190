import math
import numpy as np
from .one_asset_option_base import OneAssetOptionBase
from ht_pricing_module.monte_carlo_engine.mc_path_generator import McPathGenerator
from ht_pricing_module.api_and_utils.api import OptionType


class DiscreteBinaryMc(OneAssetOptionBase):

    def __calculate_present_value__(self) -> float:
        intraday = round(math.ceil(self.param.current_date) - self.param.current_date, 4)
        return self.mc_binary(
            option_type=self.param.option_type,
            spot_price=self.param.spot_price,
            strike_price=self.param.strike_price,
            payoff=self.param.payoff,
            riskfree_rate=self.param.riskfree_rate,
            dividend=self.param.dividend,
            vol=self.param.volatility,
            intraday=intraday,
            expiry_date=self.param.expiry_date - math.ceil(self.param.current_date) + math.ceil(intraday),
            year_base=self.param.year_base,
            obs=[obs.obs_index - math.ceil(self.param.current_date) + math.ceil(intraday) for obs in self.param.obs_date]
        )

    def mc_binary(self, option_type, spot_price, strike_price, payoff, riskfree_rate, dividend, vol, intraday,
                  expiry_date, year_base, obs):

        cp = {OptionType.CALL: 1, OptionType.PUT: -1}[option_type]
        rst = 0

        if expiry_date <= 0:
            rst = payoff if cp * (spot_price - strike_price) >= 0 else 0
        else:
            residual_intraday = round(1 - intraday, 4) if round(1 - intraday, 4) < 1 else round(1 - intraday, 4) - 1
            generator = McPathGenerator(riskfree_rate=riskfree_rate, dividend=dividend, vol=vol,
                                        intraday=residual_intraday, expiry_date=expiry_date, year_base=year_base,
                                        random_seed=0)

            price = spot_price * generator.generate()
            obs_arr = np.array(obs).astype(int)
            obs_arr = obs_arr[obs_arr >= 0]

            payoff_flag = cp * (price[:, obs_arr] - strike_price) >= 0
            payoff_index = (np.insert(payoff_flag, 0, np.zeros(len(payoff_flag)), axis=1)).argmax(axis=1)
            discount_factor_arr = np.exp(-1 * riskfree_rate * (obs_arr - residual_intraday) / year_base)
            discount_factor_arr = np.insert(discount_factor_arr, 0, 0)[payoff_index]
            rst = np.mean(payoff * discount_factor_arr)
        return rst
