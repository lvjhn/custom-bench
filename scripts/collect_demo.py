from custom_bench.benchmarker import Benchmarker 
import json

benchmarker = Benchmarker(
    name="Benchmarker-Demo", 
    description="A simple customized benchmarking demo.",
    has_items=False
)

benchmarker.start() 

benchmarker.skip_start()

for i in range(500):
    j = i ** 32

benchmarker.skip_end()

for i in range(1000): 
    j = i ** 3

benchmarker.end() 


print(json.dumps(benchmarker.state, indent=4))
