
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
        benchmarker = Benchmarker()
        
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
        assert(benchmarker.summary["duration"]["with_skipped"] >= 0)
        assert(benchmarker.summary["duration"]["no_skipped"] >= 0)
        assert(
            benchmarker.summary["duration"]["with_skipped"] 
            >= 
            benchmarker.summary["duration"]["no_skipped"] 
        )

    def test_benchmarker_can_add_context(self):
        benchmarker = Benchmarker()

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
        benchmarker.start() 

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

        


    
    