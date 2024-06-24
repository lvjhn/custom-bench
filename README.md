# custom-bench

This is a simple benchmarking library for Python3 designed to be easy to
understand and use.

## Basic Usage

The API is simple and only involves one major class which is the `Benchmarker`
class from the `custom_bench.benchmarker` module.

To use the library for a simple one run benchmark, just do the folowing:

```python
import json

from custom_bench.benchmarker import Benchmarker 

benchmarker = Benchmarker(
    name="Name-Of-The-Benchmark",
    description="Description-Of-The-Benchmark"
)

benchmarker.start() 

# code to benchmark

benchmarker.end() 

# get the results 

print(json.dumps(benchmarker.summary, indent=4))
```

### Sample Result

```json
{ 
    "start": 1.423539619,
    "end": 1.423546812,
    "skipped": 0,
    "duration_ns": 7.193000000071947e-06, 
    "duration_ws": 7.193000000071947e-06,
}
```

* `start` - the starting time of the benchmark item
* `end` - the ending time of the benchmark item
* `skipped` - no. of seconds skipped (e.g. on skipping `print` functions)
* `duration_ns` - duration without skipped portions
* `duration_ws` - duration with skipped portions

## No Reporter Included

This library does not have a pre-built reporter shipped.

It just provides reusable `start` and `stop` controls for benchmarking
and some basic two-level structure.

Hence, feel free write your own reporter.

## `custom-bench-fsr` (File System Reporter)

Alternatively, you can download the "default" `custom-bench-fsr` package for a
simple file system reporter which saves results on the filesystem.

However, it may not tailor to you needs perfectly. It is upon your discretion
whether to use such reporter or not. More details about such reporter is its own package/repository page.


## Dividing Benchmark into Parts

You can divide a benchmark into parts using the `has_items` keyword parameter. 
Just set it to `true`. 

Then you can use the `.context()` method to divide the
benchmark into subsections.

```python
benchmarker = Benchmarker(
    name="Name-Of-The-Benchmark",
    description="Description-Of-The-Benchmark",
    has_items=True 
)
```

### Full Code Example
```python
import json

from custom_bench.benchmarker import Benchmarker 

benchmarker = Benchmarker(
    name="Name-Of-The-Benchmark",
    description="Description-Of-The-Benchmark",
    has_items=True
)

benchmarker.start() 

#
# BENCHMARK PART ONE 
# 
step_1 = benchmarker.context(name="Step 1 : Squares with * Operator")
step_1.start()

for i in range(100):
    j = i * i

step_1.end()

#
# BENCHMARK PART TWO 
# 
step_2 = benchmarker.context(name="Step 2 : Squares with ** Operator")
step_2.start()

for i in range(100):
    j = i ** 2

step_2.end()

benchmarker.end() 

# get the results as a JSON serializable object 
# (serialized other classes)
results = benchmarker.collect()

print(json.dumps(results, indent=4))
```

### Sample Results

`Schema`
``` json
{
    "meta" : {
        "name" : string,
        "description" : string, 
        "ran_at" : string (datetime format)
    }, 
    "summary" : {
        "start" : float (starting time of the main benchmark), 
        "end" : float (ending time of the main benchmark),
        "skipped" : float (duration of the skipped portions in the benchmark), 
        "duration_ns" : float (total time without the skipped portions), 
        "duration_ws" : float (total time with the skipped portions)
    }, 
    "children" : {
        "n_items" : int (no. of contexts/items), 

        (general summary about the contexts)
        "items_summary" : {
            
            (info. about the outliers)
            "outliers_info" : {
                "thres" : float (factor of standard deviation use to find outliers), 
                "lb" : float (lower bound of the cut off), 
                "ub" : float (upper bound of the cut off), 
                "qty_below_lb" : int (no. of outliers below lower bound),
                "qty_above_ub" : int (no. of outliers above upper bound), 
                "n_outliers" : int (no. of outliers),
                "b_lb_perc_total" : float (% of outliers below lower bound to total no. of items),
                "a_ub_perc_total" : float (% of outliers above upper bound to total no. of items), 
                "both_perc_total" : float (% of outliers to total no. of items), 
                "b_lb_perc_outlier" : float (% of outliers below lower bound to total no. of outliers), 
                "a_ub_perc_outlier" : float (% of outliers above lower bound to total numbers of outliers),
                "b_lb_perc_non_outlier" : float (% of outliers below lower bound to non-outliers),
                "a_ub_perc_non_outlier" : float (% of outliers above upper bound to non-outliers),
                "outlier_perc_non_outlier" : float (% of outliers to non-outliers)
            }, 

            "with_outliers" : {
                "mean": float (mean of the durations of all contextx),
                "mode_val": float (mode value of the durations of all contexts),
                "mode_count": int (mode count of the durations of all contexts),
                "median": float (median value of the durations of all contexts),
                "variance": float (variance value of the durations of all contexts),
                "std_dev": float (std. dev. value of the durations of all contexts),
                "coef_var": float (coef. var. of the durations of all contexts),
                "skewness": float (skewness of the durations of all contexts),
                "kurtosis": float (kurtosis of the durations of all contexts),
                "percentile_1": float (1st percentile of the durations of all contexts),
                "percentile_5": float (5th percentile of the durations of all contexts),
                "percentile_10": float (10th percentile of the durations of all contexts),
                "percentile_20": float (20th percentile of the durations of all contexts),
                "percentile_25": float (25th percentile of the durations of all contexts),
                "percentile_50": float (50th percentile of the durations of all contexts),
                "percentile_75": float (75th percentile of the durations of all contexts),
                "percentile_80": float (80th percentile of the durations of all contexts),
                "percentile_90": float (90th percentile of the durations of all contexts),
                "percentile_95": float (95th percentile of the durations of all contexts),
                "percentile_99": float (99th percentile of the durations of all contexts),
                "normality_sw": float (normality p-value for Shapiro-Wilk test),
                "normality_ks": float (normality p-value for Kolmogorov-Smirnov test),
                "normality_ad": float (normality p-value for Anderson-Darling test),
                "stationarity_adf": float (stationarity p-value using Adfuller test test),
                "stationarity_kpss": float (stationarity p-value for KPSS test)
            },

            "no_outliers" : {
                ... same as "with_outliers"
            }

        }, 

        "items" : {
            "[[context-1-name]]" : {
                "meta" : {
                    ... same as top level meta (but for context)
                },
                "summary" : {
                    ... same as top level summary (but for contexts)
                }
            },
            "[[context-2-name]]" : {
                "meta" : {
                    ... same as top level meta (but for context)
                },
                "summary" : {
                    ... same as top level summary (but for contexts)
                }
            },
            ...
        }
    }
}
```

```json
{
    "meta": {
        "name": "Name-Of-The-Benchmark",
        "description": "Description-Of-The-Benchmark",
        "ran_at": "2024-06-24 19:05:05"
    },
    "summary": {
        "start": 1.565202823,
        "end": 1.565477239,
        "skipped": 0,
        "duration_ws": 0.00027441600000011057,
        "duration_ns": 0.00027441600000011057
    },
    "children": {
        "n_items": 2,
        "items_summary": {
            "outliers_info": {
                "thres": 2,
                "lb": 1.1462500000170017e-05,
                "ub": 3.502449999970292e-05,
                "qty_below_lb": 0,
                "qty_above_ub": 0,
                "b_lb_perc_total": 0.0,
                "a_ub_perc_total": 0.0,
                "both_perc_total": 0.0,
                "b_lb_perc_outlier": "N/A",
                "a_ub_perc_outlier": 0.0,
                "b_lb_perc_non_outlier": 0.0,
                "a_ub_perc_non_outlier": 0.0,
                "outlier_perc_non_outlier": 0.0
            },
            "with_outliers": {
                "mean": 2.3243499999936468e-05,
                "mode_val": 1.7353000000053243e-05,
                "mode_count": 1,
                "median": 2.3243499999936468e-05,
                "variance": 3.469799024862428e-11,
                "std_dev": 5.890499999883225e-06,
                "coef_var": 0.2534256888979425,
                "skewness": 0.0,
                "kurtosis": -2.0,
                "percentile_1": 1.7470810000050906e-05,
                "percentile_5": 1.7470810000050906e-05,
                "percentile_10": 1.7470810000050906e-05,
                "percentile_20": 1.7470810000050906e-05,
                "percentile_25": 1.7470810000050906e-05,
                "percentile_50": 1.7470810000050906e-05,
                "percentile_75": 1.7470810000050906e-05,
                "percentile_80": 1.7470810000050906e-05,
                "percentile_90": 1.7470810000050906e-05,
                "percentile_95": 1.7470810000050906e-05,
                "percentile_99": 1.7470810000050906e-05,
                "normality_sw": "N/A",
                "normality_ks": "N/A",
                "normality_ad": "N/A",
                "stationarity_adf": "N/A",
                "stationarity_kpss": "N/A"
            },
            "no_outliers": {
                "mean": 2.3243499999936468e-05,
                "mode_val": 1.7353000000053243e-05,
                "mode_count": 1,
                "median": 2.3243499999936468e-05,
                "variance": 3.469799024862428e-11,
                "std_dev": 5.890499999883225e-06,
                "coef_var": 0.2534256888979425,
                "skewness": 0.0,
                "kurtosis": -2.0,
                "percentile_1": 1.7470810000050906e-05,
                "percentile_5": 1.7470810000050906e-05,
                "percentile_10": 1.7470810000050906e-05,
                "percentile_20": 1.7470810000050906e-05,
                "percentile_25": 1.7470810000050906e-05,
                "percentile_50": 1.7470810000050906e-05,
                "percentile_75": 1.7470810000050906e-05,
                "percentile_80": 1.7470810000050906e-05,
                "percentile_90": 1.7470810000050906e-05,
                "percentile_95": 1.7470810000050906e-05,
                "percentile_99": 1.7470810000050906e-05,
                "normality_sw": "N/A",
                "normality_ks": "N/A",
                "normality_ad": "N/A",
                "stationarity_adf": "N/A",
                "stationarity_kpss": "N/A"
            }
        },
        "items": {
            "Step 1 : Squares with * Operator": {
                "meta": {
                    "name": "Step 1 : Squares with * Operator",
                    "description": null,
                    "ran_at": "2024-06-24 19:05:05"
                },
                "summary": {
                    "start": 1.565322698,
                    "end": 1.565340051,
                    "skipped": 0,
                    "duration_ws": 1.7353000000053243e-05,
                    "duration_ns": 1.7353000000053243e-05
                }
            },
            "Step 2 : Squares with ** Operator": {
                "meta": {
                    "name": "Step 2 : Squares with ** Operator",
                    "description": null,
                    "ran_at": "2024-06-24 19:05:05"
                },
                "summary": {
                    "start": 1.565445259,
                    "end": 1.565474393,
                    "skipped": 0,
                    "duration_ws": 2.9133999999819693e-05,
                    "duration_ns": 2.9133999999819693e-05
                }
            }
        }
    }
}
```

## Units

```python
import json

from custom_bench.benchmarker import Benchmarker 

benchmarker = Benchmarker(
    name="Name-Of-The-Benchmark",
    description="Description-Of-The-Benchmark",
    has_items=True
)

benchmarker.start() 

#
# BENCHMARK PART ONE 
# 
step_1 = benchmarker.context(
    name="Step 1 : Squares with * Operator",
    with_units=True
)
step_1.start()

for i in range(3):
    unit = step_1.unit(name=f"unit-{i}")
    unit.start()
    j = i * i
    unit.end() 

step_1.end()

benchmarker.end() 

# get the results as a JSON serializable object 
# (serialized other classes)
results = benchmarker.collect()

print(json.dumps(results, indent=4))
```

### Sample Result

```json
{
    "meta": {
        ...
    },
    "summary": {
        ...
    },
    "children": {
        "n_items": 1,
        "items_summary": {
            "outliers_info": {
               ...
            },
            "with_outliers": {
                ...
            },
            "no_outliers": {
                ...
            }
        },
        "items": {
            "Step 1 : Squares with * Operator": {
                "meta": {
                    ...
                },
                "summary": {
                    ...
                },
                "children": {
                    "n_items": 3,
                    "items_summary": {
                        "outliers_info": {
                            ... same as contexts, but this time for units
                            within a context 
                        },
                        "with_outliers": {
                            ... same as contexts, but this time for units
                            within a context
                        },
                        "no_outliers": {
                            ... same as contexts, but this time for units
                            within a context
                        }
                    },
                    "items": {
                        "unit-0": {
                            "meta": {
                                "name": "unit-0",
                                "description": null,
                                "ran_at": "2024-06-24 19:31:23"
                            },
                            "summary": {
                                "start": null,
                                "end": null,
                                "skipped": 0,
                                "duration_ws": 0,
                                "duration_ns": 0
                            }
                        },
                        "unit-1": {
                            "meta": {
                                "name": "unit-1",
                                "description": null,
                                "ran_at": "2024-06-24 19:31:23"
                            },
                            "summary": {
                                "start": null,
                                "end": null,
                                "skipped": 0,
                                "duration_ws": 0,
                                "duration_ns": 0
                            }
                        },
                        "unit-2": {
                            "meta": {
                                "name": "unit-2",
                                "description": null,
                                "ran_at": "2024-06-24 19:31:23"
                            },
                            "summary": {
                                "start": null,
                                "end": null,
                                "skipped": 0,
                                "duration_ws": 0,
                                "duration_ns": 0
                            }
                        }
                    }
                }
            }
        }
    }
}
```