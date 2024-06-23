
outliers_info = {
    "std" : 2, 
    "bounds" : {
        "lower" : None,
        "upper" : None
    }, 
    "qty" : {
        "below_lb"  : None, 
        "above_ub"  : None, 
        "total"     : None
    },
    "perc_total" : {
        "below_lb" : None, 
        "above_ub" : None,
        "both"     : None
    },
    "perc_outlier" : {
        "below_lb" : None, 
        "above_ub" : None
    }
}

items_summary_details = {
    "mean"      : None, 
    "mode"      : None, 
    "median"    : None, 
    "variance"  : None, 
    "std_dev"   : None, 
    "coef_var"  : None,
    "skewness"  : None, 
    "kurtosis"  : None, 
    "percentiles" : {
        "1"     : None,
        "5"     : None, 
        "10"    : None,
        "20"    : None,
        "25"    : None, 
        "50"    : None,
        "75"    : None, 
        "90"    : None, 
        "95"    : None, 
        "99"    : None
    },
    "normality" : {
        "sw"  : None, 
        "ks"  : None, 
        "ad"  : None
    }, 
    "stationarity" : {
        "adf"   : None, 
        "kpss"  : None
    }
}

general_summary = {
    "start" : None, 
    "end" : None, 
    "skipped" : 0, 
    "duration" : {
        "with_skipped" : 0, 
        "no_skipped" : 0
    } 
}

multi_items = {
    "general_summary" : general_summary.copy(),
    "n_items" : 0,
    "items_summary" : {
        "outliers_info" : outliers_info.copy(), 
        "with_outliers" : items_summary_details.copy(),
        "no_outliers" : items_summary_details.copy()
    }, 
    "items" : {}
}