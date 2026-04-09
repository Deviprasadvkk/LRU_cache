# Micro-Redis: High-Performance LRU Cache API

A distributed caching service built from scratch using custom data structures and FastAPI.

## Key Features
- **O(1) Performance:** Custom Doubly Linked List + Hash Map for constant-time lookups and updates.
- **Thread-Safe:** Implemented Mutex Locks to handle concurrent API requests safely.
- **Cache-Aside Architecture:** Designed to sit between an application and a database to reduce latency.

## How it Works
This project implements a Least Recently Used (LRU) eviction policy. When the cache reaches capacity, it automatically "evicts" the oldest data to make room for new entries, ensuring the system never exceeds its memory limit.
