# DSA Practice Tracker

A Python command-line tool I built to track my own data structures & algorithms practice, logging problems by topic and difficulty, flagging what needs review, and surfacing priorities using a custom-built heap.

Built from scratch to reinforce fundamentals while learning. Every core feature (sorting, search, priority queue) is implemented without external algorithm libraries.

## Features

- **Persistent storage** — problems are saved to and loaded from a local JSON file, so your practice history survives between sessions
- **Interactive CLI menu** — add, search, view, and edit problems without touching the code
- **Custom sorting algorithms** — merge sort (by difficulty) and quicksort with random pivot selection (by name), both implemented from scratch
- **Heap-based priority view** — surfaces your hardest problems first, using a custom min-heap comparison built on Python's `heapq`
- **Search and edit** — find problems by topic or name (case-insensitive), and update fields like topic on the fly
- **Formatted table output** — clean, aligned display via the `tabulate` library

## How to run

```bash
pip install tabulate
python3 ds\&a_tool.py
```

## What I learned building this

This project was built alongside learning core CS fundamentals — each feature was added as I learned the underlying concept (e.g., the priority view was added right after learning heaps). It's meant to be a living project that grows as I keep learning.

## Tech stack

Python 3, `heapq`, `collections.deque`, `json`, `tabulate`