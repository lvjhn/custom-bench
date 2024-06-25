
from unittest.mock import Mock, MagicMock, patch
import unittest

import uuid 
import datetime
import time

from custom_bench.benchmarker import Benchmarker
import custom_bench.context as context
from custom_bench.benchmark_item import BenchmarkItem

class TestBenchmarker_Feature: 
    
    #
    # Test that one can create a Benchmarker object, start it,
    # skip some portion, and end time.
    # 
    def test_benchmarker_setup(self):
        benchmarker = Benchmarker(
            has_items=False
        )
        
        # start the benchmarker
        benchmarker.start() 

        # first part of benchmark 
        for i in range(1000): 
            j = i ** 2

        # skip some part 
        benchmarker.skip_start()  
        for i in range(300):
            j = i ** 6
        benchmarker.skip_end()

        # second part of benchmark 
        for i in range(200):
            j = i ** 4

        benchmarker.end()

        # assert some stuff 
        assert(benchmarker.summary["start"] > 0)
        assert(benchmarker.summary["end"] > 0)
        assert(
            benchmarker.summary["end"] 
            >
            benchmarker.summary["start"]
        )
        assert(benchmarker.summary["skipped"] >= 0)
        assert(benchmarker.summary["duration_ws"] >= 0)
        assert(benchmarker.summary["duration_ns"] >= 0)
        assert(
            benchmarker.summary["duration_ws"] 
            >= 
            benchmarker.summary["duration_ns"] 
        )

    def test_benchmarker_can_add_context(self):
        benchmarker = Benchmarker(
            has_items=True
        )

        # assert contexts do not exist yet
        assert(benchmarker.n_children == 0)
        assert(len(list(benchmarker.children().keys())) == 0)
        assert(not benchmarker.has_context("context-a"))
        assert(not benchmarker.has_context("context-b"))

        # start the benchmarker
        benchmarker.start() 

        # create a context 
        context_a = benchmarker.context(name="context-a") 
        
        # start the first context
        context_a.start()

        # something to increase the duration
        for i in range(100):
            j = i * 100 

        # end the first context 
        context_a.end()

        # create another context 
        context_b = benchmarker.context(name="context-b") 

        # start the second context
        context_b.start() 

        # something to increase the duration
        for i in range(100):
            j = i * 100 

        # end the second context
        context_b.end() 

        # end the benchmarker 
        benchmarker.end()

        # assert that we have registered some context 
        assert(benchmarker.n_children == 2)
        assert(len(list(benchmarker.children().keys())) == 2)
        assert(benchmarker.has_context("context-a"))
        assert(benchmarker.has_context("context-b"))

        
    def test_benchmarker_can_add_unit(self):
        benchmarker = Benchmarker(
            has_items=True
        )

        # assert contexts do not exist yet
        assert(benchmarker.n_children == 0)
        assert(len(list(benchmarker.children().keys())) == 0)
        assert(not benchmarker.has_context("context-a"))
        assert(not benchmarker.has_context("context-b"))

        # start the benchmarker
        benchmarker.start() 

        # create a context 
        context = benchmarker.context(name="context", has_items=True) 
        
        # start the first context
        context.start()

        # something to increase the duration
        for i in range(3):
            unit = context.unit(name=f"unit-{i}")
            unit.start()
            for k in range(100 * i):
                j = k * 100 
            unit.end()


        # end the first context 
        context.end()

        # create another context 
        context = benchmarker.context(name="context-b") 

        # end the benchmarker 
        benchmarker.end()

        # assert that we have registered some context 
        assert(benchmarker.has_context("context"))
        # assert(context.has_unit("unit-0"))
        # assert(context.has_unit("unit-1"))
        # assert(context.has_unit("unit-2"))


    
    

    
    