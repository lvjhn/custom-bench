import numpy as np 
import scipy.stats as stats
import math 
from statsmodels.stats.diagnostic import normal_ad
from statsmodels.tsa.stattools import adfuller, kpss

class Summarizer: 
    """ 
        Summarizes benchmark related information.
    """ 
    def __init__(self, benchmark_item): 
        """ 
            Creates a new benchmark object.
        """ 
        self.benchmark_item = benchmark_item

        self.outlier_threshold = 2

        self.mappings = {
            "mean"                  : self.get_mean, 
            "mode_val"              : lambda X: self.get_mode(X)[0], 
            "mode_count"            : lambda X: self.get_mode(X)[1], 
            "median"                : self.get_median, 
            "variance"              : self.get_variance, 
            "std_dev"               : self.get_std_dev, 
            "coef_var"              : self.get_coef_var, 
            "skewness"              : self.get_skewness,
            "kurtosis"              : self.get_kurtosis, 
            "percentile_1"          : lambda X: self.get_percentile(X, 1),
            "percentile_5"          : lambda X: self.get_percentile(X, 5),
            "percentile_10"         : lambda X: self.get_percentile(X, 10),
            "percentile_20"         : lambda X: self.get_percentile(X, 20),
            "percentile_25"         : lambda X: self.get_percentile(X, 25),
            "percentile_50"         : lambda X: self.get_percentile(X, 50),
            "percentile_75"         : lambda X: self.get_percentile(X, 75),
            "percentile_80"         : lambda X: self.get_percentile(X, 80),
            "percentile_90"         : lambda X: self.get_percentile(X, 90),
            "percentile_95"         : lambda X: self.get_percentile(X, 95),
            "percentile_99"         : lambda X: self.get_percentile(X, 99),
            "normality_sw"          : self.get_sw_t_p_value,
            "normality_ks"          : self.get_ks_t_p_value, 
            "normality_ad"          : self.get_ad_t_p_value, 
            "stationarity_adf"      : self.get_adf_t_p_value, 
            "stationarity_kpss"     : self.get_kpss_t_p_value 
        }

    def summarize(self):
        """ 
            Summarized the results in the benchmark item.
        """ 
        # make general summary
        self.make_general_summary() 

        # make items summary (if applicable)
        if self.benchmark_item.has_items: 
            self.make_items_summary()

    def make_general_summary(self): 
        """ 
            Computes info. about general summary.
            Particularly, it computes the total duration.
        """ 
        summary = self.benchmark_item.summary 

        start = summary["start"]
        end = summary["end"]

        duration = end - start
        skipped = summary["skipped"]
        duration_trimmed = duration - skipped

        summary["duration_ws"] = duration 
        summary["duration_ns"] = duration_trimmed

    def make_items_summary(self): 
        """ 
            Computes info. about items summary.
        """ 

        # get durations
        items = \
            self.benchmark_item.state["children"]["items"]
        items_values = \
            list(items.values())
        unit_durations = \
            list(
                map(
                    lambda x: x.summary["duration_ns"], 
                    items_values
                )
            )      

        # get outliers 
        with_outliers = self.make_sub_summary(unit_durations)
        
        outliers_info, filtered = \
            self.make_outliers_info(with_outliers, unit_durations)

        no_outliers = self.make_sub_summary(filtered)

        # set in benchmark item 
        items_summary = self.benchmark_item.state["children"]["items_summary"]
        items_summary["with_outliers"] = with_outliers
        items_summary["outliers_info"] = outliers_info
        items_summary["no_outliers"]   = no_outliers

    def make_sub_summary(self, X): 
        results = {}
        for item in self.mappings:
            results[item] = self.mappings[item](X)
        return results

    def make_outliers_info(self, Xr, X): 
        Xn          = len(X)

        mean        = Xr["mean"]
        std_dev     = Xr["std_dev"]
        thres       = self.outlier_threshold
        lb          = mean - thres * std_dev
        ub          = mean + thres * std_dev
        
        within_b    = list(filter(lambda x: x > lb and x < ub, X))
        above_ub    = list(filter(lambda x: x > ub, X))
        below_lb    = list(filter(lambda x: x < lb, X))
        
        n_outside_b   = len(below_lb) + len(above_ub)
        n_within_b    = len(within_b) 
        n_below_lb    = len(below_lb)
        n_above_ub    = len(above_ub)  

        b_lb_perc_total = n_below_lb/ Xn
        a_ub_perc_total = n_above_ub / Xn
        both_perc_total = n_outside_b / Xn

        b_lb_perc_outlier = "N/A"
        a_ub_perc_outlier = "N/A"
        if n_outside_b > 0: 
            b_lb_perc_outlier = n_below_lb / n_outside_b
            a_ub_perc_outlier = n_above_ub / n_outside_b

        a_ub_perc_outlier = n_above_ub / Xn

        b_lb_perc_non_outlier    = "N/A"
        a_ub_perc_non_outlier    = "N/A"
        outlier_perc_non_outlier = "N/A" 
        if n_within_b > 0: 
            b_lb_perc_non_outlier = n_below_lb / n_within_b
            a_ub_perc_non_outlier = n_above_ub / n_within_b,
            outlier_perc_non_outlier = n_outside_b / n_within_b


        outliers_info = {   
            "thres"                         : thres, 
            "lb"                            : lb,
            "ub"                            : ub, 
            "qty_below_lb"                  : n_below_lb, 
            "qty_above_ub"                  : n_above_ub,
    
            "b_lb_perc_total"               : b_lb_perc_total, 
            "a_ub_perc_total"               : a_ub_perc_total, 
            "both_perc_total"               : both_perc_total, 
        
            "b_lb_perc_outlier"             : b_lb_perc_outlier, 
            "a_ub_perc_outlier"             : a_ub_perc_outlier, 
            
            "b_lb_perc_non_outlier"         : b_lb_perc_non_outlier, 
            "a_ub_perc_non_outlier"         : a_ub_perc_non_outlier, 
            "outlier_perc_non_outlier"      : outlier_perc_non_outlier
        }

        return outliers_info, within_b


    #
    # Computational wrappers (changeable)
    # 

    def get_mean(self, X):
        return float(np.average(X))  

    def get_mode(self, X):
        mode_res = stats.mode(X)
        mode_val = float(mode_res.mode) 
        mode_count = int(mode_res.count)
        return (mode_val, mode_count)

    def get_median(self, X): 
        return float(np.median(X))

    def get_variance(self, X): 
        return float(np.var(X))

    def get_std_dev(self, X):
        return float(np.std(X))

    def get_coef_var(self, X): 
        return float(stats.variation(X))

    def get_skewness(self, X): 
        skewness = float(stats.skew(X))
        
        if not math.isnan(skewness): 
            return skewness
        else: 
            return "N/A"

    def get_kurtosis(self, X): 
        kurtosis = float(stats.kurtosis(X))

        if not math.isnan(kurtosis):
            return kurtosis 
        else: 
            return "N/A"

    def get_percentile(self, X, p): 
        if len(X) < 2:
            return "N/A" 
        else: 
            return float(np.percentile(X, 1)) 

    def get_sw_t_p_value(self, X):
        if len(X) < 10: 
            return "N/A"
        else: 
            return float(stats.shapiro(X).pvalue)

    def get_ks_t_p_value(self, X):
        if len(X) < 5: 
            return "N/A"
        else: 
            return float(stats.kstest(X, stats.norm.cdf).pvalue)

    def get_ad_t_p_value(self, X):
        if len(X) < 10:
            return "N/A"
        else:
            return float(normal_ad(np.array(X))[1]) 

    def get_adf_t_p_value(self, X):
        if len(X) < 10:
            return "N/A" 
        else: 
            return float(adfuller(X)[1])

    def get_kpss_t_p_value(self, X):
        if len(X) < 10: 
            return "N/A"
        else: 
            return float(kpss(X)[1])

