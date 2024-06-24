from custom_bench.benchmarker import Benchmarker 
import json

benchmarker = Benchmarker(
    name="Benchmarker-Demo", 
    description="A simple customized benchmarking demo.",
    has_items=True
)

benchmarker.start() 

context_a = benchmarker.context(name="raise-by-2") 
context_a.start() 

for i in range(100):
    j = i ** 2

context_a.end()


context_b = benchmarker.context(name="raise-by-3") 
context_b.start() 

for i in range(100):
    j = i ** 3

context_b.end()


benchmarker.end() 

print(json.dumps(benchmarker.collect(), indent=4))
