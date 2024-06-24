from custom_bench.benchmarker import Benchmarker 
import json
import pprint as pp

benchmarker = Benchmarker(
    name="Benchmarker-Demo", 
    description="A simple customized benchmarking demo.",
    has_items=True
)

benchmarker.start() 

context_a = benchmarker.context(name="raise-by-2", has_items=True) 
context_a.start() 

for i in range(100):
    unit_a = context_a.unit(name=f"unit-{i}", description=f"{i} ** 2")

    unit_a.skip_start() 
    print(f"@ Unit {i + 1}.")
    unit_a.skip_end()

    unit_a.start()
    for j in range(10000):
        j = i ** 32
    unit_a.end()

context_a.end()


context_b = benchmarker.context(name="raise-by-3", has_items=True) 
context_b.start() 

for i in range(100):
    unit_a = context_b.unit(name=f"unit-{i}", description=f"{i} ** 3")
    unit_a.start()
    j = i ** 32
    unit_a.end()

context_b.end()


benchmarker.end() 

print(json.dumps(benchmarker.collect(), indent=4))
