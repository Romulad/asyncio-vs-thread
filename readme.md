# 🧠 Python Concurrency Benchmark — Personal Roadmap

## 📌 WHY am I doing this?

I want to **understand the real, practical difference** between:
- Synchronous I/O
- Thread-based concurrency
- Asyncio-based concurrency
- Hybrid setups (asyncio + threads)

---

## 🧪 Benchmarks To Build

### Phase 1 — Baseline (CPU-Bound)

- [x] Run CPU-bound loop (e.g. char encode sum) with:
  - sync function
  - `async def`
  - threads (TBD)
- [x] Confirm there's **no benefit from asyncio** for CPU-bound tasks
- [ ] Test threads on CPU-bound and see if any GIL constraints show

### Phase 2 — Pure I/O (Network or Filesystem)

- [ ] Fetch N URLs with `requests` (sync baseline)
- [ ] Fetch N URLs with `requests` in `ThreadPoolExecutor`
- [ ] Fetch N URLs with `aiohttp` + `asyncio.gather`
- [ ] Fetch N URLs with hybrid: `aiohttp` + thread offload (e.g. slow file I/O in async)
---

## 📈 METRICS TO COLLECT

For each test:
- ⏱️ Total wall time
- 🚀 Throughput = N / total time
- 🕒 Avg latency (if measurable per task)
- 🔁 Scale test at: [10, 50, 100, 500, 1000] tasks
- (Optional) 🔥 CPU usage or idle % (use `psutil`)
- (Optional) 💾 Memory usage for large N

## 🔧 IDEAS FOR NEXT STEPS

- Plot results with `matplotlib`
- Visualize latency histograms
- Build an internal "mini load tester"
- Add compressed response simulation (gzip / brotli)
- Write a conclusion file: **"What I learned"**
