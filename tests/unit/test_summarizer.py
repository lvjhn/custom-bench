from unittest.mock import Mock, MagicMock, patch, call

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
    # Test .summarize() 
    # 
    def test_summarize_no_items(self): 
        summarizer = Summarizer(BenchmarkItem())

        summarizer.benchmark_item.has_items = False 
        
        summarizer.make_general_summary = Mock() 
        summarizer.make_items_summary = Mock(0)

        summarizer.summarize() 

        summarizer.make_general_summary.assert_called()
        summarizer.make_items_summary.assert_not_called()

    def test_summarize_with_items(self): 
        summarizer = Summarizer(BenchmarkItem())

        summarizer.benchmark_item.has_items = True 
        
        summarizer.make_general_summary = Mock() 
        summarizer.make_items_summary = Mock(0)

        summarizer.summarize() 

        summarizer.make_general_summary.assert_called()
        summarizer.make_items_summary.assert_called()

    #
    # Test .make_general_summary()
    # 
    def test_make_general_summary(self):
        summarizer = Summarizer(BenchmarkItem())

        summarizer.benchmark_item.summary["start"] = 10
        summarizer.benchmark_item.summary["end"] = 20
        summarizer.benchmark_item.summary["skipped"] = 5

        summarizer.make_general_summary() 

        summary = summarizer.benchmark_item.summary

        assert(summary["duration_ws"] == 10)
        assert(summary["duration_ns"] == 5)

    #
    # Test .make_items_summary()
    # 
    def test_make_items_summary(self):

        class MockBenchmarkItem:
            def __init__(self, duration):
                self.summary = { "duration_ns" : duration }

        summarizer = Summarizer(BenchmarkItem())
        
        summarizer.make_sub_summary = Mock(
            side_effect=[
                "sub-summary-a", 
                "sub-summary-b"
            ]
        )

        summarizer.make_outliers_info = Mock(
            return_value=(
                "outliers-info", 
                [1, 2, 3, 4]
            )
        )

        summarizer.benchmark_item.state["children"] = {
            "items_summary" : {
                "with_outliers" : None,
                "outliers_info" : None, 
                "no_outliers" : None
            }
        } 

        summarizer.benchmark_item.state["children"]["items"] = {
            "item-a" : MockBenchmarkItem(10), 
            "item-b" : MockBenchmarkItem(20), 
            "item-c" : MockBenchmarkItem(30), 
            "item-d" : MockBenchmarkItem(10),    
            "item-e" : MockBenchmarkItem(20), 
            "item-f" : MockBenchmarkItem(30), 
            "item-g" : MockBenchmarkItem(10), 
            "item-h" : MockBenchmarkItem(20),
            "item-i" : MockBenchmarkItem(30),  
            "item-j" : MockBenchmarkItem(10),    
        }

        summarizer.make_items_summary() 

        X = [10, 20, 30, 10, 20, 30, 10, 20, 30, 10]


        items_summary = \
            summarizer.benchmark_item.state["children"]["items_summary"]
        
        assert(items_summary["with_outliers"] == "sub-summary-a")
        summarizer.make_sub_summary.has_calls([call(X)])


        assert(items_summary["outliers_info"] == "outliers-info")
        summarizer.make_outliers_info.assert_called_with(
            items_summary["with_outliers"],
            X
        )

        assert(items_summary["no_outliers"] == "sub-summary-b")
        summarizer.make_sub_summary.has_calls([call([1, 2, 3, 4])])

    #
    # Test .make_sub_summary() 
    # 
    def test_make_sub_summary(self):
        X = [10, 20, 30, 10, 20, 30, 10, 20, 30, 10]

        summarizer = Summarizer(BenchmarkItem()) 

        for item in summarizer.mappings:
            summarizer.mappings[item] = Mock() 

        summarizer.make_sub_summary(X) 

        for item in summarizer.mappings:
            summarizer.mappings[item].assert_called_with(X)

    #
    # Test .make_outliers_info()
    #
    def test_make_outliers_info(self): 
        summarizer = Summarizer(BenchmarkItem()) 

        X = [-10000, 10, 20, 30, 10, 20, 30, 10, 20, 30, 10000]
        Xr = {}

        summarizer.outlier_threshold = 2
        Xr["mean"] = 10
        Xr["std_dev"] = 5 

        keys = (
            'thres', 
            'lb', 
            'ub', 
            'qty_below_lb', 
            'qty_above_ub', 
            "n_outliers",
            'b_lb_perc_total', 
            'a_ub_perc_total', 
            'both_perc_total', 
            'b_lb_perc_outlier', 
            'a_ub_perc_outlier', 
            'b_lb_perc_non_outlier', 
            'a_ub_perc_non_outlier', 
            'outlier_perc_non_outlier'
        )


        info = summarizer.make_outliers_info(Xr, X)
        summary = info[0]
        filtered = info[1]

        assert(tuple(summary.keys()) == keys)   
        assert(len(filtered) == 3)




     