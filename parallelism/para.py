"""
Educational Example: Concurrency vs Sequential Processing in Python

This script simulates an IO-bound task (e.g., API call) using time.sleep.
We process a list of "sentences" in two ways:
    1. Sequentially (one-by-one)
    2. Concurrently (with ThreadPoolExecutor, several at once)

Key Concepts:
-------------
- Sequential: Each task waits for the previous to finish.
- Concurrency: Several tasks are in progress at once (if one is waiting, another runs).
- In Python, ThreadPoolExecutor is ideal for IO-bound tasks (e.g., waiting for API responses).

Glossary:
---------
- IO-bound: Program spends most of its time waiting for input/output (API calls, disk/network).
- CPU-bound: Program spends most of its time doing computations (e.g., math).

NOTE:
-----
This example uses only Python's standard library (time, concurrent.futures).
**If you use external libraries (like requests, database clients, or LLM SDKs),**
their own threading, async, or connection management can affect how concurrency actually works.
**Always check the documentation and test your exact flow when using real-world libraries!**
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
import time

sentences_to_be_classified = [
    "Sentence 1",
    "Sentence 2",
    "Sentence 3",
    "Sentence 4",
    "Sentence 5",
    "Sentence 6",
    "Sentence 7",
    "Sentence 8",
    "Sentence 9",
    "Sentence 10",
]

def mock_classify(sentence):
    """Simulate an IO-bound task (e.g., network request) by sleeping for 1 second."""
    time.sleep(1)  # Simulate "waiting" for an external resource
    return sentence, "mock_result"

# ----- Way 1: Sequential -----
print("\n--- Starting Sequential Processing ---")
start_time = time.time()
for sentence in sentences_to_be_classified:
    sent, res = mock_classify(sentence)
    print(f"(Sequential) Sentence: {sent} | Result: {res}")
sequential_time = time.time() - start_time
print(f"Sequential processing completed in {sequential_time:.2f} seconds\n")

# ----- Way 2: Concurrent with threads -----
print("--- Starting Concurrent Processing ---")
start_time = time.time()
with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(mock_classify, s) for s in sentences_to_be_classified]
    for future in as_completed(futures):
        sent, res = future.result()
        print(f"(Concurrent) Sentence: {sent} | Result: {res}")
concurrent_time = time.time() - start_time
print(f"Concurrent processing completed in {concurrent_time:.2f} seconds\n")

print(f"Speed improvement: {sequential_time/concurrent_time:.2f}x faster with concurrent processing")

"""
Expected Output (timing):
- Sequential: ~10 seconds (10 sentences x 1s each)
- Concurrent: ~4 seconds (3 threads, so ~10/3 = 3-4 rounds)
"""
