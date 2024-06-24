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
step_1 = benchmarker.context(name="Step 1 : Squares with * Operator")
step_1.start()

for i in range(100):
    j = i * i

step_1.end()

#
# BENCHMARK PART TWO 
# 
step_2 = benchmarker.context(name="Step 2 : Squares with ** Operator")
step_2.start()

for i in range(100):
    j = i ** 2

step_2.end()

benchmarker.end() 

# get the results as a JSON serializable object 
# (serialized other classes)
results = benchmarker.collect()

print(json.dumps(results, indent=4))