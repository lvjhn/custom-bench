import time 
import uuid 
import json
import os 
import copy
import scipy.stats as stats
import shutil
import numpy as np
import math

from statsmodels.stats.diagnostic import normal_ad
from statsmodels.tsa.stattools import adfuller, kpss

TEMPLATES = {
    "multi_run_meta" :  {
        "outliers" : {
            "std_devs" : 2, 
            "bounds" : {
                "lower" : None, 
                "upper" : None
            }, 
            "qty" : {
                "below_lb" : None, 
                "above_up" : None
            },
            "perc_total" : {
                "below_lb" : None, 
                "above_up" : None,
                "both"     : None
            },
            "perc_outlier" : {
                "below_lb" : None, 
                "above_up" : None
            }
        }
    }, 
    "multi_run_summary" : {
        "n_items"   : None, 
        "mean"      : None, 
        "mode"      : None, 
        "med"       : None, 
        "var"       : None, 
        "std"       : None, 
        "cv"        : None,
        "skew"      : None, 
        "kurt"      : None, 
        "percentiles" : {
            "1"     : None,
            "5"     : None, 
            "10"    : None,
            "20"    : None,
            "25"    : None, 
            "50"    : None,
            "75"    : None, 
            "80"    : None,
            "90"    : None, 
            "95"    : None, 
            "99"    : None
        },
        "normality" : {
            "sw"  : None, 
            "ks"  : None, 
            "ad"  : None
        }, 
        "stationarity" : {
            "adf"   : None, 
            "kpss"  : None
        }
    }, 
    "overall_result" : {
        "start"    : 0, 
        "end"      : 0,
        "skipped"  : 0, 
        "duration" : {
            "with_skipped" : None, 
            "no_skipped"   : None
        }
    }
}

#######################################
# Get Current Time (Wrapper Function) #
####################################### 
def get_benchmark_time(): 
    return time.process_time()
 
#################
# Context Class #
################# 
class Context: 
    def __init__(self, benchmark, **kwargs):
        self.name = kwargs.get("name", uuid.uuid4())
        self.description = kwargs.get("description", "An untitled context.")
    
        self.benchmark = benchmark

        self.data = kwargs.get("data", None)
        
        # unit setup info.
        self.with_units = kwargs.get("with_units", False)
        self.units = {}

        # info. for skipping
        self._skip_start = 0

    ######################
    # BENCHMARK CONTROLS #
    ######################

    def start(self):
        time_= get_benchmark_time()
        self.data["summary"]["start"] = time_
        
    def end(self): 
        time_ = get_benchmark_time()
        self.data["summary"]["end"] = time_

        # compute durations
        self.update_durations() 

        # compute units summary
        if self.with_units: 
            self.compute_units_summary()
        
    def compute_units_summary(self): 
        meta, with_outliers, no_outliers = \
            Summarizer.summary(list(self.units.values()))

        scope = self.data["units_summary"]

        Summarizer.patch(meta, with_outliers, no_outliers, scope)

    def update_durations(self):
        start = self.data["summary"]["start"]
        end = self.data["summary"]["end"] 
        skipped = self.data["summary"]["skipped"]

        with_skipped = end - start
        no_skipped = with_skipped - skipped

        self.data["summary"]["duration"]["with_skipped"] = with_skipped 
        self.data["summary"]["duration"]["no_skipped"] = no_skipped

    def skip_start(self): 
        time_ = get_benchmark_time()
        self._skip_start = time_ 

    def skip_end(self): 
        skip_end = get_benchmark_time() 
        skip_start = self._skip_start 
        duration = skip_end - skip_start 
        self.elevate_skip(duration)
        self._skip_start = None

    def elevate_skip(self, duration):
        self.data["summary"]["skipped"] += duration
        self.benchmark.summary["skipped"] += duration

    ##################
    # UNIT CREATION #
    #################

    def create_blank_unit_data(self):
        # create record for context
        data = copy.deepcopy(TEMPLATES["overall_result"])
        return data 

    def create_unit(self, name, **kwargs):
        description = kwargs.get("description", "Some random unit.")

        # create blank unit data
        data = self.create_blank_unit_data()

        # create unit object
        unit = Unit(
            self, 
            data=data, 
            name=name, 
            description=description
        ) 

        # register unit in registry 
        self.units[name] = unit 

        return unit


    def unit(self, name, **kwargs):
        description = kwargs.get("description", "An untitled unit.")

        if name not in self.units:
            return self.create_unit(name, description=description)
        else: 
            return self.units[name] 
        
    ###################
    # UTILITY METHODS #
    ################### 

    def collect(self): 
        # create root JSON object
        root = {
            "meta" : {
                "name" : str(self.name), 
                "description" : self.description
            },
            "summary" : self.data["summary"], 
            "units_summary" :self.data["units_summary"], 
            "units" : {}
        }

        # collect data from units
        units = self.units
        for unit_name in units:
            unit = units[unit_name]
            root["units"][unit_name] = unit.collect()

        return root

    def stringify(self, **kwargs): 
        indent = kwargs.get("indent", None) 
        
        # create root JSON object
        root = self.collect()

        root = { **{ "benchmark" : self.benchmark.meta }, **root }

        # stringify root data
        stringified = "" 

        if indent:
            stringified = json.dumps(root, indent=indent)
        else: 
            stringified = json.dumps(root)

        return stringified
    
    def unit_times(self):
        pass 

########
# Unit #
########
class Unit: 
    def __init__(self, context, **kwargs): 
        self.name = kwargs.get("name", uuid.uuid4())
        self.description = kwargs.get("description", "Some random unit.") 
        
        self.data = kwargs.get("data", None) 
        
        self.context = context

        self._skip_start = 0

    ######################
    # BENCHMARK CONTROLS # 
    ######################

    def start(self): 
        time_ = get_benchmark_time()
        self.data["start"] = time_

    def end(self): 
        time_ = get_benchmark_time() 
        self.data["end"] = time_

        # compute durations
        self.update_durations()

    def update_durations(self):
        with_skipped = self.data["end"] - self.data["start"]
        no_skipped = with_skipped - self.data["skipped"]

        self.data["duration"]["with_skipped"] = with_skipped 
        self.data["duration"]["no_skipped"] = no_skipped

    def skip_start(self): 
        time_ = get_benchmark_time() 
        self._skip_start = time_ 

    def skip_end(self):
        skip_end = get_benchmark_time() 
        skip_start = self._skip_start 
        duration = skip_end - skip_start 
        self.elevate_skip(duration)     
        self._skip_start = None   

    def elevate_skip(self, duration):
        self.data["skipped"] += duration
        self.context.elevate_skip(duration)

    ###################
    # UTILITY METHODS #
    ################### 

    def collect(self): 
        # create root JSON object
        root = {
            "description" : self.description,
            "result" : self.data 
        } 
        return root


###############
# Benchmarker #
############### 
class Benchmarker: #
    def __init__(self, **kwargs):
        self.name        = kwargs.get("name", uuid.uuid4())
        self.description = "A simple benchmark."
        self.outdir      = kwargs.get("outdir", f"./benchmarks/{self.name}") 

        # meta info.
        self.meta = {
            "name"        : self.name, 
            "description" : self.description
        }

        # summary info.
        self.summary = copy.deepcopy(TEMPLATES["overall_result"])
        self.contexts_summary = {
            "meta" : copy.deepcopy(TEMPLATES["multi_run_meta"]),
            "with_outliers" : copy.deepcopy(TEMPLATES["multi_run_summary"]),
            "no_outliers" : copy.deepcopy(TEMPLATES["multi_run_summary"])
        }

        # context info.
        self.contexts = {}

        # skip data
        self._skip_start = 0

    ####################
    # CONTEXT CREATION #
    ####################

    def create_blank_context_data(self, with_units = False): 
        # create record for context
        data = {
            "summary" : copy.deepcopy(TEMPLATES["overall_result"])
        }

        # add structure for unit information if necessary
        if with_units: 
            data = {
                **data,
                "units_summary" : { 
                    "meta" : \
                        copy.deepcopy(TEMPLATES["multi_run_meta"]),
                    "with_outliers" : \
                        copy.deepcopy(TEMPLATES["multi_run_summary"]),
                    "no_outliers" : \
                        copy.deepcopy(TEMPLATES["multi_run_summary"])
                },
                "units" : {}
            }

        return data
   
    def create_context(self, name, **kwargs):
        with_units = kwargs.get("with_units", False)
        description = kwargs.get("description", "Some random context.")

        # create context data
        data = self.create_blank_context_data(with_units)
      
        # create context object with data 
        context = Context(
            self, 
            data=data,
            with_units=with_units,
            description=description
        )

        # register context to contexts map
        self.contexts[name] = context 

        return context

    def get_context(self, name): 
        return self.contexts[name]

    def context(self, name, **kwargs):
        description = kwargs.get("description", "Some random context.")
        with_units = kwargs.get("with_units", False)

        if name not in self.contexts:
            return self.create_context(
                name, 
                with_units=with_units, 
                description=description
            )
        else: 
            return self.context[name] 

    #########################
    # BENCHMARKING CONTROLS #
    ######################### 

    def start(self): 
        time_ = get_benchmark_time()
        self.summary["start"] = time_

    def end(self):
        time_ = get_benchmark_time()
        self.summary["end"] = time_

        # compute durations
        self.update_durations() 
        self.compute_contexts_summary()


    def update_durations(self): 
        with_skipped = self.summary["end"] - self.summary["start"]
        no_skipped = with_skipped - self.summary["skipped"]


        self.summary["duration"]["with_skipped"] = with_skipped 
        self.summary["duration"]["no_skipped"] = no_skipped

    def skip_start(self):
        time_ = get_benchmark_time()
        self._skip_start = time_

    def skip_end(self):
        skip_end = get_benchmark_time() 
        skip_start = self._skip_start 
        duration = skip_end - skip_start 
        self.summary["skipped"] += duration
        self._skip_start = None
        

    def compute_contexts_summary(self): 
        meta, with_outliers, no_outliers = \
            Summarizer.summary(self.contexts.values())

        scope = self.contexts_summary
        Summarizer.patch(meta, with_outliers, no_outliers, scope)

    #################
    # BASIC REPORTS #
    ################# 
    def info(self): 
        T  = ""

        T += "Benchmark Results\n" 
        T += "===============================================\n"
        T += f"Name        : {self.meta['name']}\n"
        T += f"Description : {self.meta['description']}\n"
        T += "===============================================\n"
        T += f"Contexts\n"
        
        context_no = 0
        for context in self.contexts:
            T += f"\t Context {context_no + 1} : \t{context}\n"
            context_no += 1        
            
        return T

    def apply_context_data(self, root):
        contexts = self.contexts
        for context_name in contexts: 
            context = contexts[context_name]
            root["contexts"][context_name] = context.collect()

    def stringify(self, **kwargs): 
        indent = kwargs.get("indent", None) 
        
        # create root JSON object
        root = {
            "meta" : self.meta,
            "summary" : self.summary,
            "contexts_summary" : self.contexts_summary,
            "contexts" : {}
        }

        # add context data
        self.apply_context_data(root)

        # stringify root data
        stringified = "" 

        if indent:
            stringified = json.dumps(root, indent=indent)
        else: 
            stringified = json.dumps(root)

        return stringified 

#################
# Base Reporter #
#################
class BaseReporter:
    def prepare_outdir(obj):
        outdir = None 

        if type(obj) == Benchmarker:
            outdir = obj.outdir 
        elif type(obj) == Context:
            outdir = obj.benchmark.outdir   
        else:
            raise Exception("Unknown benchmark object type.")


        BaseReporter.make_directory(outdir)

    def make_directory(outdir):
        if os.path.exists(outdir):
            shutil.rmtree(outdir)

        os.makedirs(outdir, exist_ok=True)

        os.makedirs(outdir + "/overall")
        os.makedirs(outdir + "/contexts")

        open(outdir + "/overall/.gitignore", "a").close() 
        open(outdir + "/contexts/.gitinore", "a").close()
        

########################
# File System Reporter #
######################## 

class FileSystemReporter:

    def report_context(context): 
        BaseReporter.prepare_outdir(context)


    def report_benchmark(benchmark):
        BaseReporter.prepare_outdir(context)



##############
# Summarizer #
##############

class Summarizer:
    def patch(meta, with_outliers, no_outliers, scope):
        scope["meta"] = meta 
        scope["with_outliers"] = with_outliers 
        scope["no_outliers"] = no_outliers 

    def handle_duration_item(item, durations):
        if type(item) is Context: 
            durations.append(
                item.data["summary"]["duration"]["with_skipped"]
            )
        elif type(item) is Unit:
            durations.append(
                item.data["duration"]["with_skipped"]
            )
        else:
            raise Exception("Unknown type.")

    def durations(items):
        durations = []
        for item in items:
            Summarizer.handle_duration_item(item, durations)
        return durations

    def compute_default(items):
        n_items = len(items)
        mean = float(np.average(items))
        mode_res = stats.mode(items)
        mode = float(mode_res.mode)
        mode_count = float(mode_res.count)
        median = float(np.median(items))
        variance = np.var(items)
        std_dev  = float(np.std(items))
        skewness = float(stats.skew(items))
        kurtosis = float(stats.kurtosis(items)) 

        if math.isnan(skewness):
            skewness = "N/A"
        if math.isnan(kurtosis):
            kurtosis = "N/A"

        result = {
            "n_items" : n_items, 
            "mean" : mean, 
            "mode" : mode, 
            "mode_count" : mode_count,
            "median" : median,
            "variance" : variance, 
            "std_dev" : std_dev,
            "skewness" : skewness, 
            "kurtosis" : kurtosis,
            "percentiles" : {
                "1"  : np.percentile(items, 1),
                "5"  : np.percentile(items, 5),
                "10" : np.percentile(items, 10),
                "20" : np.percentile(items, 20),
                "25" : np.percentile(items, 25),
                "50" : np.percentile(items, 50),
                "75" : np.percentile(items, 75),
                "80" : np.percentile(items, 80),
                "90" : np.percentile(items, 90),
                "95" : np.percentile(items, 90),
            }, 
            "normality" : {
                "sw" : (
                    "N/A" if n_items < 10
                    else stats.shapiro(items).pvalue
                ), 
                "ks" : (
                    "N/A" if n_items < 10
                    else stats.kstest(items, stats.norm.cdf).pvalue
                ),
                "ad" : (
                    "N/A" if n_items < 10
                    else normal_ad(np.array(items))[1]
                )
            },
            "stationarity" : {
                "adf" : (
                    "N/A" if n_items < 10 
                    else adfuller(items)[1]
                ), 
                "kpss" : (
                    "N/A" if n_items < 10 
                    else kpss(items)[1]
                )
            }
        }

        return result

    def compute_meta(items, with_outliers, outlier_thres):
        n_items = with_outliers["n_items"]
        mean = with_outliers["mean"]
        std_dev = with_outliers["std_dev"]
        
        thres = outlier_thres

        lb = mean - thres * std_dev
        ub = mean + thres * std_dev

        below_lb = 0 
        above_ub = 0 

        filtered = []

        for i in range(len(items)):
            item = items[i]
            if item < lb: 
                below_lb += 1
            elif item > ub:
                above_ub += 1
            else:
                filtered.append(item)

        total_outliers = below_lb + above_ub

        meta = {
            "outliers" : {
                "std" : thres, 
                "bounds" : {
                    "lower" : lb, 
                    "upper" : ub
                }, 
                "qty" : {
                    "below_lb" : below_lb, 
                    "above_ub" : above_ub,
                    "total" : total_outliers
                }, 
                "perc_total" : {
                    "below_lb" : below_lb / n_items, 
                    "above_ub" : above_ub / n_items, 
                    "both" : total_outliers / n_items
                }, 
                "perc_outlier" : {
                    "below_lb" : (
                        below_lb / total_outliers 
                        if total_outliers > 0 else 0
                    ), 
                    "above_ub" :  (
                        below_lb / total_outliers if total_outliers > 0
                        else 0
                    )
                }
            }
        }

        return meta, filtered

    def summary(items, outlier_thres = 2):
        items = Summarizer.durations(items)
        items = list(items)
        
        # compute for with_outliers 
        with_outliers = Summarizer.compute_default(items)

        # compute meta 
        meta, filtered_items = Summarizer.compute_meta(
            items, with_outliers, outlier_thres
        )

        # compute no outliers
        no_outliers = Summarizer.compute_default(filtered_items)

        return meta, with_outliers, no_outliers 