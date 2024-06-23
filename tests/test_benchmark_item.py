from unittest.mock import Mock, MagicMock, patch

import uuid 
import datetime
import time

from custom_bench.benchmark_item import BenchmarkItem
import custom_bench.context as context

class TestBenchmarkItem: 

    #
    # Test Constructor
    # 

    def test_constructor_defaults(self): 
        benchmark_item = BenchmarkItem()
        assert(type(benchmark_item.name) is uuid.UUID)
        assert(len(str(benchmark_item.name)) == 36)

    def test_constructor_params(self):
        benchmark_item = BenchmarkItem(
            name="test-benchmark",
            description="A simple benchmark used in testing."
        )

        assert(
            benchmark_item.name == "test-benchmark"
        )
        assert(
            benchmark_item.description == "A simple benchmark used in testing."
        )
        assert(
            datetime.datetime.strptime(
                benchmark_item.run_datetime, 
                "%Y-%m-%d %H:%M:%S"
            )
        )

    #
    # Test .info() 
    # 
    def test_info(self):
        benchmark_item = BenchmarkItem()
        info = benchmark_item.info() 
        assert("Name" in info)
        assert("Description" in info)
        assert("Run Date/Time" in info)

    #
    # Test .benchmark_time() 
    # 
    def test_benchmark_time(self): 
        benchmark_item = BenchmarkItem() 
        assert(type(benchmark_item.benchmark_time()) is float)

    #
    # Test .start()
    # 
    def test_start(self): 
        benchmark_item = BenchmarkItem()

        benchmark_item.benchmark_time = Mock(return_value=1.0)
        benchmark_item.after_start_fn = Mock()

        assert(benchmark_item.summary["start"] is None)

        benchmark_item.start() 

        assert(benchmark_item.summary["start"] is not None)
        assert(type(benchmark_item.summary["start"]) is float) 

        benchmark_item.benchmark_time.assert_called()
        benchmark_item.after_start_fn.assert_called()

    #
    # Test .end()
    # 
    def test_end(self): 
        benchmark_item = BenchmarkItem()

        benchmark_item.benchmark_time = Mock(return_value=1.0)
        benchmark_item.after_end_fn = Mock()

        assert(benchmark_item.summary["end"] is None)

        benchmark_item.end() 

        assert(benchmark_item.summary["end"] is not None)
        assert(type(benchmark_item.summary["end"]) is float)

        benchmark_item.benchmark_time.assert_called()
        benchmark_item.after_end_fn.assert_called()

    #
    # Test .skip_start()
    # 
    def test_skip_start(self):
        benchmark_item = BenchmarkItem()

        benchmark_item.benchmark_time = Mock(return_value=1.5)

        benchmark_item.after_skip_start_fn = Mock()

        benchmark_item.skip_start() 

        assert(benchmark_item.misc["skip_start"] == 1.5)

        benchmark_item.after_skip_start_fn.assert_called()

    # 
    # Test .skip_end() 
    # 
    def test_skip_new(self): 
        benchmark_item = BenchmarkItem() 

        benchmark_item.benchmark_time = Mock(return_value=1.0) 
        benchmark_item.after_skip_end_fn = Mock()

        benchmark_item.misc["skip_start"] = 0.2

        benchmark_item.skip_end() 

        assert(benchmark_item.summary["skipped"] == 0.8) 

        benchmark_item.after_skip_end_fn.assert_called_with(0.8)

    def test_skip_end_existing(self): 
        benchmark_item = BenchmarkItem() 

        benchmark_item.benchmark_time = Mock(return_value=1.0) 
        benchmark_item.after_skip_end_fn = Mock()
        
        benchmark_item.summary["skipped"] = 1.0
        benchmark_item.misc["skip_start"] = 0.2

        benchmark_item.skip_end() 

        assert(benchmark_item.summary["skipped"] == 1.8) 

        benchmark_item.after_skip_end_fn.assert_called_with(0.8)