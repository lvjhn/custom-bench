import json

from custom_bench.benchmarker import Benchmarker 

benchmarker = Benchmarker(
    name="Name-Of-The-Benchmark",
    description="Description-Of-The-Benchmark",
    has_items=True
)

benchmarker.start() 

#
# BENCHMARK PART ONE 
# 
step_1 = benchmarker.context(
    name="Step 1 : Squares with * Operator",
    has_items=True
)
step_1.start()

for i in range(3):
    unit = step_1.unit(name=f"unit-{i}")
    unit.start()
    for k in range(1000):
        j = k * k
    unit.end() 

step_1.end()

benchmarker.end() 

# get the results as a JSON serializable object 
# (serialized other classes)
results = benchmarker.collect()

print(json.dumps(results, indent=4))