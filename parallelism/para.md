# Concurrency vs. Parallelism in Python (with LLM API Example)

## Key Concepts

- **Concurrency**: Multiple tasks make progress at the same time, but not necessarily literally at the same instant. Tasks may be paused and resumed, overlapping in execution.

- **Parallelism**: Multiple tasks are executed at the exact same time, each on a different CPU core.

| Term | Definition | Example Scenario |
|------|------------|------------------|
| Concurrency | Tasks are in progress together (may quickly switch between each other) | LLM API calls, network/database calls |
| Parallelism | Tasks run truly at the same time (on separate CPU cores) | Heavy math computations, simulations |

## Why is LLM API/Network IO a Perfect Example for Concurrency?

When using LLM APIs or making network/database calls, most of the time your program is waiting for a response (IO-bound).

While waiting for one API call to finish, your code can start others—concurrent execution.

In Python, `ThreadPoolExecutor` works well for these IO-bound tasks, since threads can "take turns" when others are waiting.

## When Should You Use Parallelism?

For CPU-bound tasks—where your code spends time on computations (not waiting for IO)—use parallelism.

In Python, this means using `ProcessPoolExecutor` or `multiprocessing`, which can use multiple CPU cores.

## Summary Table

| Use-case | Executor Type | GIL Limitation? | Typical Python Tool |
|----------|---------------|-----------------|---------------------|
| IO-bound | Concurrency | No (GIL not a bottleneck) | `ThreadPoolExecutor` |
| CPU-bound | Parallelism (multi-core) | Yes (GIL blocks threads for CPU) | `ProcessPoolExecutor` |

## Visual Illustration