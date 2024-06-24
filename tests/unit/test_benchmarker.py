from unittest.mock import Mock, MagicMock, patch
import unittest

import uuid 
import datetime
import time

from custom_bench.benchmarker import Benchmarker
import custom_bench.context as context
from custom_bench.benchmark_item import BenchmarkItem

class TestBenchmarker: 
    
    #
    # Test Parent Class 
    # 
    def test_parent(self): 
        assert(issubclass(type(Benchmarker()), BenchmarkItem))

    #
    # Test .has_context() method. 
    #          
    def test_has_context_exists(self): 
        benchmarker = Benchmarker() 
        benchmarker.contexts["items"] = {}
        benchmarker.contexts["items"]["test-context"] = True 
        assert(benchmarker.has_context("test-context")) 

    def test_has_context_not_exists(self): 
        benchmarker = Benchmarker() 
        assert(not benchmarker.has_context("test-context")) 


    #
    # Test .context() method.
    # 
    def test_context_load(self):
        benchmarker = Benchmarker() 
        
        benchmarker.contexts["items"] = {}
        benchmarker.contexts["items"]["test-context"] = 1234 

        benchmarker.has_context = Mock(return_value=True) 

        assert(benchmarker.context(name="test-context") == 1234)
    
    def test_context_new(self):
        benchmarker = Benchmarker() 

        benchmarker.has_context = Mock(return_value=False) 
        benchmarker.create_context = Mock(return_value=4321)

        result = benchmarker.context(
            name="test-context",
            description="A simple test context.",
            with_units=True
        )

        assert(result == 4321)

        benchmarker.create_context.assert_called_with(
            "test-context",
            "A simple test context.",
            True
        )

    #
    # Test .create_context() 
    # 
    def test_create_context(self):

        benchmarker = Benchmarker(Context=Mock())

        benchmarker.add_children = Mock()

        result = benchmarker.create_context(
            "test-context", 
            "test-description",
            True
        )

        assert(result is not None)
        assert("test-context" in benchmarker.contexts["items"])
        assert(benchmarker.contexts["items"]["test-context"] is not None)

        benchmarker.Context.assert_called_with(
            name="test-context",
            description="test-description",
            benchmarker=benchmarker,
            with_units=True
        )

        benchmarker.add_children.assert_called()