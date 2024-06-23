from custom_bench.benchmarker import Benchmarker 

benchmark = Benchmarker(
    name="demo-benchmark",
    description="A simple demo benchmark."
)

print(benchmark.info())

