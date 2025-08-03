# 🧠 Python Concurrency Model Benchmark

<!--- Add a short description about it ---->

## 📌 WHY?

I was wondered how python concurrency model performs and which one is best for IO-bound execution in practice. 
I've already had answers to my doubts and even clearly but I wanted to help someone else to understand the differences with pratical results.

Mainly:
- I wanted to know which one, between asyncio and thread perform well when performing io-bound task
- I asked myself: can we combine asyncio and thread ? What would be the result? Better, more faster or just worst ?  
- I wanted to confirm that there is any difference in term of time and resources usage between thread, asyncio, sync when performing cpu-bound execution
- Does the sentence "asyncio/thread should not be used with cpu-bound execution, they don't provide any advantage or even add overhead" correct ?
- Clear my doubts!

So I conducted this simple benchmarking.

We have two results set:
- the first result set is about cpu bound execution (character encding) wih sync, asyncio and threads
- the second one is about an io bound execution (http request) using sync, asyncio, threads, asyncio and threads combined

---

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
