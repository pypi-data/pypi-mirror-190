import math
import numpy as np
import pandas as pd
from ht_pricing_module.monte_carlo_engine.mc_path_generator import McPathGenerator
from .one_asset_option_base import OneAssetOptionBase
from ht_pricing_module.api_and_utils.api import DirectionType


class SnowballMc(OneAssetOptionBase):

    def __calculate_present_value__(self) -> float:
        intraday = round(math.ceil(self.param.current_date) - self.param.current_date, 4)
        return self.mc_snowball(
            notional=self.param.notional,
            spot_price=self.param.spot_price,
            entrance_price=self.param.entrance_price,
            knock_in_barrier_price=self.param.knock_in_barrier_price,
            knock_out_barrier_price=self.param.knock_out_barrier_price,
            floor_rate=self.param.floor_rate,
            margin_rate=self.param.margin_rate,
            bonus_rate=self.param.bonus_rate,
            direction=self.param.direction,
            is_knock_in=self.param.is_knock_in,
            riskfree_rate=self.param.riskfree_rate,
            dividend=self.param.dividend,
            vol=self.param.volatility,
            intraday=intraday,
            expiry_date=self.param.expiry_date - math.ceil(self.param.current_date) + math.ceil(intraday),
            year_base=self.param.year_base,
            knock_in_obs=pd.DataFrame(
                {'obs_index': [obs.obs_index - math.ceil(self.param.current_date) + math.ceil(intraday) for obs in self.param.knock_in_obs_date],
                 'adjust': [obs.adjust_rate for obs in self.param.knock_in_obs_date]}),
            knock_out_obs=pd.DataFrame(
                {'obs_index': [obs.obs_index - math.ceil(self.param.current_date) + math.ceil(intraday) for obs in self.param.knock_out_obs_date],
                 'adjust': [obs.adjust_rate for obs in self.param.knock_out_obs_date],
                 'coupon_rate': [obs.coupon_rate for obs in self.param.knock_out_obs_date]})
        )

    def mc_snowball(self, notional, spot_price, entrance_price, knock_in_barrier_price, knock_out_barrier_price,
                    floor_rate, margin_rate, bonus_rate, direction, is_knock_in, riskfree_rate, dividend, vol, intraday,
                    expiry_date, year_base, knock_in_obs, knock_out_obs, price=None):

        residual_intraday = round(1 - intraday, 4) if round(1 - intraday, 4) < 1 else round(1 - intraday, 4) - 1
        if price is None:
            generator = McPathGenerator(riskfree_rate=riskfree_rate, dividend=dividend, vol=vol,
                                        intraday=residual_intraday, expiry_date=expiry_date, year_base=year_base,
                                        random_seed=0)

            price = spot_price * generator.generate()

        direction = {DirectionType.STANDARD: 1, DirectionType.REVERSE: -1}[direction]
        knock_in_obs_idx = knock_in_obs[knock_in_obs.obs_index >= 0].obs_index.values
        ki_adj = knock_in_obs[knock_in_obs.obs_index >= 0].adjust.values
        knock_out_obs_idx = knock_out_obs[knock_out_obs.obs_index >= 0].obs_index.values
        ko_adj = knock_out_obs[knock_out_obs.obs_index >= 0].adjust.values
        ko_coupon = knock_out_obs[knock_out_obs.obs_index >= 0].coupon_rate.values
        t_arr = (knock_in_obs_idx if 0 in knock_in_obs_idx else np.hstack([0, knock_in_obs_idx])) - residual_intraday

        assert round(expiry_date - residual_intraday, 6) == round(t_arr[-1], 6)

        ki_mat_flag = np.zeros((len(price), 1), dtype=bool) if len(knock_in_obs_idx) == 0 else direction * (price[:, knock_in_obs_idx] - knock_in_barrier_price * ki_adj) <= 0
        ko_mat_flag = np.zeros((len(price), 1), dtype=bool) if len(knock_out_obs_idx) == 0 else direction * (price[:, knock_out_obs_idx] - knock_out_barrier_price * ko_adj) >= 0
        ko_idx = (np.insert(ko_mat_flag, 0, np.zeros(len(ko_mat_flag)), axis=1)).argmax(axis=1)

        dis_factor = 1 / np.exp(riskfree_rate * t_arr[knock_out_obs_idx] / year_base)
        dis_factor = np.insert(dis_factor, 0, 0)[ko_idx]

        # 敲出
        ko_payoff = dis_factor * notional * (np.where(ko_idx == 0, 0, ko_coupon[ko_idx - 1]) - margin_rate * np.where(ko_idx == 0, 0, np.exp(riskfree_rate * t_arr[knock_out_obs_idx][ko_idx - 1] / year_base) - 1))

        comp_factor = np.exp(riskfree_rate * (expiry_date - residual_intraday) / year_base)
        dis_factor = 1 / comp_factor

        # 敲入未敲出
        ki_no_ko_arr_flag = np.logical_and(np.logical_or(is_knock_in, np.max(ki_mat_flag, axis=1)), np.logical_not(np.max(ko_mat_flag, axis=1)))
        ki_no_ko_payoff = ki_no_ko_arr_flag * dis_factor * notional * (np.maximum((floor_rate - 1), np.minimum(direction * (price[:, -1] / entrance_price - 1), 0)) - margin_rate * (comp_factor - 1))

        # 未敲入未敲出
        no_ki_no_ko_arr_flag = np.logical_and(np.logical_and(1 - is_knock_in, np.logical_not(np.max(ki_mat_flag, axis=1))), np.logical_not(np.max(ko_mat_flag, axis=1)))
        no_ki_no_ko_payoff = no_ki_no_ko_arr_flag * dis_factor * notional * (bonus_rate - margin_rate * (comp_factor - 1))

        rst = np.round(np.mean(ko_payoff + ki_no_ko_payoff + no_ki_no_ko_payoff), 8)

        return rst
