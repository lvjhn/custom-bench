from unittest.mock import Mock, MagicMock, patch

import uuid 
import datetime
import time

from custom_bench.benchmark_item import BenchmarkItem

import custom_bench.context as context
import custom_bench.templates as templates

class TestBenchmarkItem: 

    #
    # Test Constructor
    # 

    def test_constructor_defaults(self): 
        benchmark_item = BenchmarkItem()

        assert(type(benchmark_item.name) is uuid.UUID)
        assert(len(str(benchmark_item.name)) == 36)

        assert(benchmark_item.description is not None)
        assert(type(benchmark_item.description) is str)

        assert(type(benchmark_item.run_datetime) is str)

        assert(type(benchmark_item.meta) is dict)
        assert("name" in benchmark_item.meta)
        assert("description" in benchmark_item.meta)

        assert(
            tuple(benchmark_item.summary.keys())
            ==
            tuple(templates.general_summary.keys())
        )

        assert(type(benchmark_item.state) is dict)
        assert("meta" in benchmark_item.state)
        assert("summary" in benchmark_item.state)
        assert(benchmark_item.state["meta"] == benchmark_item.meta)
        assert(benchmark_item.state["summary"] == benchmark_item.summary)

        assert(hasattr(benchmark_item, "has_items"))
        assert(benchmark_item.has_items == False)
        assert(benchmark_item.items_name == None)

    def test_constructor_params(self):
        benchmark_item = BenchmarkItem(
            name="test-benchmark",
            description="A simple benchmark used in testing.",
            has_items=True,
            items_name="items"
        )

        assert(
            benchmark_item.name == "test-benchmark"
        )
        assert(
            benchmark_item.description == "A simple benchmark used in testing."
        )
        assert(
            benchmark_item.has_items == True
        )
        assert(
            benchmark_item.items_name == "items"
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

    #
    # Test .after_skip_end_fn()
    # 
    def test_after_skip_end_fn_no_parent(self): 
        benchmark_item = BenchmarkItem() 

        benchmark_item.parent = None 

        assert(benchmark_item.after_skip_end_fn(1.5) == False)

    def test_after_skip_end_fn_with_parent(self): 
        benchmark_item = BenchmarkItem() 

        benchmark_item.parent = Mock()
        benchmark_item.parent.add_skip_time = Mock()

        assert(benchmark_item.after_skip_end_fn(1.5) == True)

        benchmark_item.parent.add_skip_time.assert_called_with(1.5)

    #
    # Test .add_skip_time() 
    # 
    def test_add_skip_time(self):
        benchmark_item = BenchmarkItem() 

        benchmark_item.summary["skipped"] = 1.5

        benchmark_item.add_skip_time(1.5)

        assert(benchmark_item.summary["skipped"] == 3.0)

    #
    # Test .children() 
    # 
    def test_children_has_items(self): 
        benchmark_item = BenchmarkItem() 

        benchmark_item.has_items = True

        benchmark_item.state = {
            "children" : {
                "items" : {
                    "foo" : "bar",
                    "bar" : "baz"
                }
            }
        }

        children = benchmark_item.children() 

        assert(tuple(children.keys()) == ("foo", "bar"))

    def test_children_has_no_items(self): 
        benchmark_item = BenchmarkItem() 

        benchmark_item.has_items = False

        children = benchmark_item.children() 

        assert(type(children) == dict)
        assert(len(children.keys()) == 0)

    #
    # Test .add_children()
    # 
    def test_add_children(self): 
        benchmark_item = BenchmarkItem() 

        benchmark_item.n_children = 2

        benchmark_item.add_children() 

        assert(benchmark_item.n_children == 3)

    #
    # Test .collect() 
    #
    def test_collect(self):
        benchmark_item = BenchmarkItem() 

        class ChildItem:
            def __init__(self, val): 
                self.state = val

            def collect(self): 
                return self.state

        benchmark_item.state = {
            "children" : {
                "items" : {
                    "context-a" : ChildItem(1), 
                    "context-b" : ChildItem(2), 
                    "context-c" : ChildItem(3), 
                    "context-d" : ChildItem(4)
                }
            }
        }

        benchmark_item.has_items  = True 

        root = benchmark_item.collect()     

        assert(root["children"]["items"]["context-a"] == 1)
        assert(root["children"]["items"]["context-b"] == 2)
        assert(root["children"]["items"]["context-c"] == 3)
        assert(root["children"]["items"]["context-d"] == 4)

    #
    # Test .after_end_fn()
    # 
    def test_after_end_fn(self):
        benchmark_item = BenchmarkItem()

        benchmark_item.summarizer.summarize = Mock() 

        benchmark_item.after_end_fn() 

        benchmark_item.summarizer.summarize.assert_called()