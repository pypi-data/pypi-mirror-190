import math
import numpy as np
from .one_asset_option_base import OneAssetOptionBase
from ht_pricing_module.monte_carlo_engine.mc_path_generator import McPathGenerator
from ht_pricing_module.api_and_utils.api import OptionType


class DiscreteAsianMc(OneAssetOptionBase):

    def __calculate_present_value__(self) -> float:
        intraday = round(math.ceil(self.param.current_date) - self.param.current_date, 4)
        return self.mc_asian(
            option_type=self.param.option_type,
            spot_price=self.param.spot_price,
            strike_price=self.param.strike_price,
            running_avg=self.param.running_avg,
            riskfree_rate=self.param.riskfree_rate,
            dividend=self.param.dividend,
            vol=self.param.volatility,
            intraday=intraday,
            expiry_date=self.param.expiry_date - math.ceil(self.param.current_date) + math.ceil(intraday),
            year_base=self.param.year_base,
            obs=[[obs.obs_index - math.ceil(self.param.current_date) + math.ceil(intraday), obs.obs_price]for obs in self.param.obs_date]
        )

    def mc_asian(self, option_type, spot_price, strike_price, running_avg, riskfree_rate, dividend, vol, intraday,
                 expiry_date, year_base, obs):

        cp = 1 if option_type == OptionType.CALL else - 1
        rst = 0
        if expiry_date <= 0:
            rst = max(cp * (np.mean(running_avg) - strike_price), 0)
        else:
            residual_intraday = round(1 - intraday, 4) if round(1 - intraday, 4) < 1 else round(1 - intraday, 4) - 1
            generator = McPathGenerator(riskfree_rate=riskfree_rate, dividend=dividend, vol=vol,
                                        intraday=residual_intraday, expiry_date=expiry_date, year_base=year_base,
                                        random_seed=0)
            price = spot_price * generator.generate()
            obs = np.array(obs)
            obs_price_arr = obs[obs[:, 0] < 0][:, 1]
            obs_index_arr = obs[obs[:, 0] >= 0][:, 0].astype(int)

            discount_factor = np.exp(-1 * riskfree_rate * (expiry_date - residual_intraday) / year_base)
            avg_price_arr = np.mean(np.concatenate((np.tile(obs_price_arr, (len(price), 1)), price[:, obs_index_arr]), axis=1), axis=1)
            rst = np.mean(discount_factor * np.maximum(cp * (avg_price_arr - strike_price), 0))
        return rst
