from unittest.mock import Mock, MagicMock, patch
import unittest

import uuid 
import datetime
import time

from custom_bench.benchmarker import Benchmarker
from custom_bench.benchmark_item import BenchmarkItem
from custom_bench.context import Context
from custom_bench.unit import Unit

import custom_bench.context as context

class TestUnit: 

    #
    # Test Parent Class 
    # 
    def test_parent(self): 
        assert(issubclass(type(Unit()), BenchmarkItem))
