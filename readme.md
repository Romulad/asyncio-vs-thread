# 🧠 Python Concurrency Model Benchmark

A comprehensive, benchmarking suite that empirically compares Python's concurrency models (sync, asyncio, threading, and hybrid approaches) across CPU-bound and IO-bound workloads. 

This project provides real-world performance data with detailed metrics on execution time, CPU usage, memory consumption, and network throughput to help myself(and/or you) make informed decisions about which concurrency model to use for their specific use cases.


## 📌 WHY?

I wondered how Python's concurrency models perform and which one is best for IO-bound execution in practice. 
I already had answers to my doubts, but I wanted to help others understand the differences with practical results.

Mainly:
- I wanted to know which one, between asyncio and threads, performs well when executing IO-bound tasks
- I asked myself: can we combine asyncio and threads? What would be the result? Better, faster, or just worse?  
- I wanted to confirm whether there is any difference in terms of time and resource usage between threads, asyncio, and sync when performing CPU-bound execution
- Is the sentence "asyncio/threads should not be used with CPU-bound execution, they don't provide any advantage or even add overhead" correct?
- Clear my doubts!

So I conducted this benchmarking with multiple test runs to ensure consistency and reliability of the results.

We have two result sets:
- The first result set is about CPU-bound execution (character encoding) with sync, asyncio, and threads
- The second one is about IO-bound execution (HTTP requests) using sync, asyncio, threads, and asyncio + threads combined

## Quick recall

**CPU-bound execution**: Tasks that are limited by the speed of the CPU (like heavy calculations, data processing). The program spends most of its time using the processor rather than waiting for external resources like network.

**IO-bound execution**: Tasks that are limited by input/output operations (like network requests). The program spends most of its time waiting for external resources rather than using the CPU.

## Experiments

### CPU-Bound Task: Character Encoding
This experiment evaluates how different concurrency models handle CPU-intensive operations by counting the byte size of each character in 100,000 generated URLs. The task involves iterating through each character in every URL and encoding it to calculate its byte representation—a purely computational workload.

The synchronous version of the script can be found [here (synchronous version)](./cpu-bound/sync.py). Other implementations are available in the same directory: [asyncio.py](./cpu-bound/asyncio.py) and [thread.py](./cpu-bound/thread.py).

#### Synchronous Execution Results

| Metric | Value | Unit |
|--------|-------|------|
| **Execution Time** | 9.77 | seconds |
| **Total Bytes Processed** | 51,258,766 | bytes |
| **CPU Usage (Process)** | 95.01% (avg) / 104.2% (max) | % |
| **CPU Usage (System)** | 24.67% (avg) / 28.5% (max) | % |
| **Memory Usage** | 15.79 | MB |
| **CPU Cores** | 4 | cores |

**Key Observations:**
- The process utilized nearly 100% of a single CPU core on average (95.01%), with peaks at 104.2%
- System-wide CPU usage remained low (24.67% average), indicating single-core execution
- Memory usage was constant at 15.79 MB throughout execution
- Completed processing 100,000 URLs in approximately 9.77 seconds

#### Asyncio Execution Results

| Metric | Value | Unit |
|--------|-------|------|
| **Execution Time** | 9.78 | seconds |
| **Total Bytes Processed** | 51,258,766 | bytes |
| **CPU Usage (Process)** | 95.89% (avg) / 102.6% (max) | % |
| **CPU Usage (System)** | 24.47% (avg) / 26.8% (max) | % |
| **Memory Usage** | 22.72 | MB |
| **CPU Cores** | 4 | cores |

**Key Observations:**
- Similar to sync execution, the process utilized nearly 100% of a single CPU core (95.89% average)
- System-wide CPU usage remained low (24.47% average), confirming single-core execution
- Memory usage was constant at 22.72 MB (44% higher than sync due to asyncio event loop overhead)
- Execution time (9.78 seconds) is virtually identical to synchronous execution
- **Asyncio provides no performance advantage for CPU-bound tasks** and adds memory overhead

#### Threading Execution Results (10 Threads)

| Metric | Value | Unit |
|--------|-------|------|
| **Execution Time** | 12.35 | seconds |
| **Total Bytes Processed** | 51,145,360 | bytes |
| **CPU Usage (Process)** | 109.59% (avg) / 172.1% (max) | % |
| **CPU Usage (System)** | 27.03% (avg) / 27.9% (max) | % |
| **Memory Usage** | 16.01 | MB |
| **CPU Cores** | 4 | cores |
| **Thread Count** | 10 | threads |

**Key Observations:**
- Process CPU usage averaged 109.59%, indicating utilization of ~1.1 CPU cores across 10 threads
- Peak CPU usage reached 172.1%, showing some multi-core utilization but limited by Python's GIL
- System-wide CPU usage (27.03% average) remained similar to sync/asyncio approaches
- Memory usage (16.01 MB) was comparable to sync execution, lower than asyncio
- **Execution time was 26% slower** (12.35s vs 9.77s) than sync/asyncio due to thread context switching overhead
- **Threading provides no benefit for CPU-bound tasks** and actually degrades performance due to GIL contention and context switching

#### Visual Performance Analysis

The following plots provide a comprehensive visual comparison of the CPU-bound execution performance:

**Execution Time Comparison:**

![Execution Time](./plots/cpu_bound_execution_time.png)

This plot clearly shows that synchronous and asyncio approaches have nearly identical execution times (~9.77s), while threading with 10 threads is significantly slower (12.35s).

**CPU Usage Comparison:**

![CPU Usage](./plots/cpu_bound_cpu_usage.png)

The CPU usage analysis reveals that all approaches utilize approximately one CPU core (process CPU ~95-110%), with system-wide CPU usage remaining low (~24-27%). This confirms that Python's GIL prevents true parallel execution for CPU-bound tasks.

**Memory Usage Comparison:**

![Memory Usage](./plots/cpu_bound_memory_usage.png)

Memory consumption is relatively consistent across all approaches, with asyncio showing the highest usage (22.72 MB) probably due to event loop overhead, while sync and threading remain similar (~15-16 MB).

**My Take:** For CPU-bound tasks, use synchronous execution or multiprocessing. Asyncio adds memory overhead without performance benefits, and threading actively degrades performance as the thread count increases.

# task type name
# description of the experiment conducted
# sync version of the script and where to find the rest
# summary table
# plot per metrics and a conclusion under each one
# A global conclusion for the task type among execution type
    - when to use What
    - what to avoid

Describe the environment used for server for io: cpu, memory

---
# title: how to execute
# project cloning
# environment set up needed software
# for cpu task, where to find script and where are the results output
# for io task, server setup using httbin docker image, where are scripts and where are the output
# result data can vary based on environement and compute resources, but if execute in the same environement, the trends will be the sameg
