
outliers_info = {
    "thres"              : 2, 

    "lb"                 : None, 
    "ub"                 : None,
    
    "qty_below_lb"       : None,
    "qty_above_ub"       : None,
    
    "b_lb_perc_total"    : None, 
    "a_ub_perc_total"    : None,
    "both_perc_total"    : None,
    
    "b_lb_perc_outlier"  : None, 
    "a_ub_perc_outlier"  : None, 

    "b_lb_perc_non_outlier"     : None, 
    "a_ub_perc_non_outlier"     : None, 
    "outlier_perc_non_outlier"  : None, 
}

items_summary_details = {
    "mean"              : None, 
    "mode_val"          : None, 
    "mode_count"        : None,
    "median"            : None, 
    "variance"          : None, 
    "std_dev"           : None, 
    "coef_var"          : None,
    "skewness"          : None, 
    "kurtosis"          : None, 
    "percentile_1"      : None, 
    "percentile_5"      : None,
    "percentile_10"     : None,
    "percentile_20"     : None,
    "percentile_25"     : None,
    "percentile_50"     : None,
    "percentile_75"     : None,
    "percentile_80"     : None,
    "percentile_90"     : None,
    "percentile_95"     : None,
    "percentile_99"     : None,
    "normality_sw"      : None, 
    "normality_ks"      : None, 
    "normality_ad"      : None, 
    "stationarity_adf"  : None, 
    "stationarity_kpss" : None    
}

general_summary = {
    "start" : None, 
    "end" : None, 
    "skipped" : 0, 
    "duration_ws" : 0, 
    "duration_ns" : 0
}

multi_items = {
    "n_items" : 0,
    "items_summary" : {
        "outliers_info" : outliers_info.copy(), 
        "with_outliers" : items_summary_details.copy(),
        "no_outliers" : items_summary_details.copy()
    }, 
    "items" : {}
}