from custom_bench.benchmark import Benchmarker, FileSystemReporter

# create benchmarker 
benchmarker = Benchmarker(
    name = "benchmark-a",
    description = "Custom benchmark example."
) 

benchmarker.start()

#############
# CONTEXT 1 #
#############
context_1 = benchmarker.context("context-1", with_units=True)

context_1.start()

for i in range(5):
    unit = context_1.unit("unit-" + str(i))
    
    unit.start()
    
    unit.skip_start()
    for k in range(i):
        o = k ** 10
    unit.skip_end()
    
    j = i ** 32
    
    unit.end()


context_1.end() 

benchmarker.end()

print(benchmarker.stringify(indent=4))