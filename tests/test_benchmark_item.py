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
    # Test .info() method.
    # 
    def test_info(self):
        benchmark_item = BenchmarkItem()
        info = benchmark_item.info() 
        assert("Name" in info)
        assert("Description" in info)
        assert("Run Date/Time" in info)

    #
    # Test .start()
    # 
    def test_start(self): 
        benchmark_item = BenchmarkItem()

        assert(benchmark_item.summary["start"] is None)

        benchmark_item.start() 

        assert(benchmark_item.summary["start"] is not None)
        assert(type(benchmark_item.summary["start"]) is float) 

    #
    # Test .end()
    # 
    def test_end(self): 
        benchmark_item = BenchmarkItem()

        assert(benchmark_item.summary["end"] is None)

        benchmark_item.end() 

        assert(benchmark_item.summary["end"] is not None)
        assert(type(benchmark_item.summary["end"]) is float)

    