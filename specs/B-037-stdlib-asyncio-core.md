# Spec Packet B-037: stdlib-asyncio-core

**Phase**: B
**Depends on**: B-001 (alias-runtime-v1), B-002 (phase-a-compat-suite), B-040 (dictionary-v1.1-async-match)
**Estimated size**: medium
**Owner**: —

## Goal

Ship Arabic aliases for the core `asyncio` library. This allows learners to use `async/await` syntax with the standard library's asynchronous tools for concurrency, including tasks, queues, and synchronization primitives.

This packet follows the structural pattern established in **B-030** (stdlib-os-pathlib-sys).

## Files

### Files to create

- `arabicpython/aliases/asyncio.toml` — Floor: 35 entries.
- `tests/aliases/test_asyncio.py`
- `examples/B37_async_crawler.apy` — Demo: Concurrent tasks with gather and sleep.
- `examples/B37_README-ar.md`

## Translation choices (must-include floor)

**`asyncio.toml` — floor 35:**

| Arabic | Python | Notes |
|---|---|---|
| `شغل` | `run` | |
| `اجمع` | `gather` | |
| `انتظر_نمة` | `sleep` | "await-sleep" to distinguish from time.sleep |
| `انشئ_مهمة` | `create_task` | |
| `مهمة` | `Task` | |
| `طابور` | `Queue` | |
| `قفل` | `Lock` | |
| `حدث` | `Event` | |
| `سيمافور` | `Semaphore` | Transliterated |
| `انتظر` | `wait` | |
| `انتظر_لمدة` | `wait_for` | |
| `عند_الاكمال` | `as_completed` | |
| `احصل_حلقة` | `get_event_loop` | |
| `حلقة_جديدة` | `new_event_loop` | |
| `اضبط_الحلقة` | `set_event_loop` | |
| `المهمة_الحالية` | `current_task` | |
| `كل_المهام` | `all_tasks` | |
| `مستقبل` | `Future` | |
| `خطأ_الغاء` | `CancelledError` | |
| `خطأ_مهلة` | `TimeoutError` | |
| `طابور_ممتلئ` | `QueueFull` | |
| `طابور_فارغ` | `QueueEmpty` | |
| `انشئ_خادم` | `start_server` | |
| `افتح_اتصال` | `open_connection` | |
| `قارئ_تدفق` | `StreamReader` | |
| `كاتب_تدفق` | `StreamWriter` | |
| `خادم` | `Server` | |
| `اجلب` | `get` | Queue.get |
| `ضع` | `put` | Queue.put |
| `تم_المهمة` | `task_done` | Queue.task_done |
| `الغي` | `cancel` | Task.cancel |
| `هل_ملغاة` | `cancelled` | Task.cancelled |
| `النتيجة` | `result` | Task.result |
| `درع` | `shield` | |
| `انتظر_حتى` | `wait_for` | |

## Test requirements

1. **Basic Concurrency**: Run two tasks with `اجمع` (gather) and verify they run concurrently via timing.
2. **Queue**: Producers and consumers using `طابور` (Queue) via Arabic aliases.
3. **Timeout**: Use `انتظر_لمدة` (wait_for) and catch the Arabic alias of `TimeoutError`.

## Acceptance checklist

- [ ] TOML file created (floor 35 entries).
- [ ] Tests passing.
- [ ] Demo `B37_async_crawler.apy` runs.
- [ ] Depends correctly on B-040's async keywords.
- [ ] Normalization round-trip verified.
