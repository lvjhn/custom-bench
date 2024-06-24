import json
import pprint as pp

from custom_bench.benchmarker import Benchmarker 

benchmarker = Benchmarker(
    name="Name-Of-The-Benchmark",
    description="Description-Of-The-Benchmark"
)

benchmarker.start() 

# code to benchmark

benchmarker.end() 

# get the results 

pp.pprint(benchmarker.summary)
