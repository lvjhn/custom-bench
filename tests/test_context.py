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

class TestContext: 

    #
    # Test Parent Class 
    # 
    def test_parent(self): 
        assert(issubclass(type(Context()), BenchmarkItem))

    #
    # Test Constructor
    # 

    def test_constructor_defaults(self): 
        context = Context()
        assert(type(context.name) is str)
        assert(type(context.description is str))
        assert(context.with_units == False)

    def test_constructor_params(self):
        context = Context(with_units=True)
        assert(context.with_units == True)

    #
    # Test .has_unit()
    # 
    def test_has_unit_exists(self): 
        context = Context() 
        context.units["test-unit"] = True 
        assert(context.has_unit("test-unit")) 

    def test_has_unit_not_exists(self): 
        context = Context() 
        assert(not context.has_unit("test-unit")) 

    #
    # Test .unit()
    # 

    def test_context_load(self):
        context = Context() 
        context.units["test-unit"] = "1234"

        assert(context.unit(name="test-unit") == "1234")
    
    def test_context_new(self):
        context = Context() 

        context.has_unit = Mock(return_value=False) 
        context.create_unit = Mock(return_value="4321")

        result = context.unit(
            name="test-unit",
            description="A simple test unit."
        )

        assert(result == "4321")

        context.create_unit.assert_called_with(
            "test-unit",
            "A simple test unit."
        )

    #
    # Test .create_unit() 
    # 
    def test_create_unit(self):

        context = Context(Unit=Mock())

        result = context.create_unit(
            "test-unit", 
            "test-description"
        )

        assert(result is not None)
        assert("test-unit" in context.units["items"])
        assert(context.units["items"]["test-unit"] is not None)

        context.Unit.assert_called_with(
            name="test-unit",
            description="test-description"
        )
 