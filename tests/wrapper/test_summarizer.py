from unittest.mock import Mock, MagicMock, patch

import uuid 
import datetime
import time

from custom_bench.summarizer import Summarizer
from custom_bench.benchmark_item import BenchmarkItem

class TestBenchmarkItem: 

    #
    # Test Constructor
    # 
    def test_constructor_defaults(self): 
        benchmark_item = BenchmarkItem()
        summarizer = Summarizer(benchmark_item) 
        assert(summarizer.benchmark_item == benchmark_item)

    #
    # Test computational stubs (if int)
    # 

    def test_get_mean(self): 
        benchmark_item = BenchmarkItem()
        summarizer = Summarizer(benchmark_item)
        X = list(range(1, 20))
        assert(type(summarizer.get_mean(X)) is float)

    def test_get_mode(self): 
        benchmark_item = BenchmarkItem()
        summarizer = Summarizer(benchmark_item)
        X = list(range(1, 20))
        assert(type(summarizer.get_mode(X)) is tuple)
        assert(type(summarizer.get_mode(X)[0]) is float)
        assert(type(summarizer.get_mode(X)[1]) is int)

    def test_get_median(self): 
        benchmark_item = BenchmarkItem()
        summarizer = Summarizer(benchmark_item)
        X = list(range(1, 20))
        assert(type(summarizer.get_median(X)) is float)
     
    def test_get_variance(self): 
        benchmark_item = BenchmarkItem()
        summarizer = Summarizer(benchmark_item)
        X = list(range(1, 20))
        assert(type(summarizer.get_variance(X)) is float)

    def test_get_std_dev(self): 
        benchmark_item = BenchmarkItem()
        summarizer = Summarizer(benchmark_item)
        X = list(range(1, 20))
        assert(type(summarizer.get_std_dev(X)) is float)

    def test_get_coef_var(self): 
        benchmark_item = BenchmarkItem()
        summarizer = Summarizer(benchmark_item)
        X = list(range(1, 20))
        assert(type(summarizer.get_coef_var(X)) is float)

    def test_get_skewness(self): 
        benchmark_item = BenchmarkItem()
        summarizer = Summarizer(benchmark_item)
        
        X = list(range(1, 20))
        assert(type(summarizer.get_skewness(X)) is float)
    
    def test_get_kurtosis(self): 
        benchmark_item = BenchmarkItem()
        summarizer = Summarizer(benchmark_item)
        
        X = list(range(1, 20))
        assert(type(summarizer.get_kurtosis(X)) is float)
    
    def test_get_percentile(self): 
        benchmark_item = BenchmarkItem()
        summarizer = Summarizer(benchmark_item)
        
        X = list(range(1, 20))
        assert(type(summarizer.get_percentile(X, 0)) is float)
 
    def test_get_percentile(self): 
        benchmark_item = BenchmarkItem()
        summarizer = Summarizer(benchmark_item)
        
        X = list(range(1, 20))
        assert(type(summarizer.get_percentile(X, 0)) is float)

    def test_get_sw_t_p_value(self): 
        benchmark_item = BenchmarkItem()
        summarizer = Summarizer(benchmark_item)
        
        X = list(range(1, 20))
        assert(type(summarizer.get_sw_t_p_value(X)) is float)

    def test_get_ks_t_p_value(self): 
        benchmark_item = BenchmarkItem()
        summarizer = Summarizer(benchmark_item)
        
        X = list(range(1, 20))
        assert(type(summarizer.get_ks_t_p_value(X)) is float)

    def test_get_ad_t_p_value(self): 
        benchmark_item = BenchmarkItem()
        summarizer = Summarizer(benchmark_item)
        
        X = list(range(1, 20))
        assert(type(summarizer.get_ad_t_p_value(X)) is float)

    def test_get_adf_t_p_value(self): 
        benchmark_item = BenchmarkItem()
        summarizer = Summarizer(benchmark_item)
        
        X = list(range(1, 20))
        assert(type(summarizer.get_adf_t_p_value(X)) is float)

    def test_get_kpss_t_p_value(self): 
        benchmark_item = BenchmarkItem()
        summarizer = Summarizer(benchmark_item)
        
        X = list(range(1, 20))
        assert(type(summarizer.get_kpss_t_p_value(X)) is float)
