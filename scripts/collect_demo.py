from custom_bench.benchmarker import Benchmarker 
import json

benchmarker = Benchmarker(
    name="Benchmarker-Demo", 
    description="A simple customized benchmarking demo.",
    has_items=False
)

benchmarker.start() 

for i in range(1000): 
    j = i ** 3

benchmarker.end() 


print(json.dumps(benchmarker.state, indent=4))
