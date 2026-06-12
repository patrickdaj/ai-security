<!-- Example output — illustrative deliverable of module 06. -->

# Crash Triage — `parse_fuzzer` campaign

47 crash inputs → **3 distinct bugs** (deduped by root cause).

| dedup_key | bug_class | exploitability | root cause |
|-----------|-----------|----------------|------------|
| `parse:body[length]` | out-of-bounds read | medium | `parse()` indexes `body[length]` without bounds-checking the length prefix (the planted bug in `example_fuzz.py`). 41 inputs. |
| `decode_header:memcpy` | heap-buffer-overflow | **critical** | `memcpy` with attacker-controlled size into a fixed stack buffer. 5 inputs. Write-what-where. |
| `to_int:NULL` | null-deref | low | `strtol` result deref without a NULL check. 1 input. |

**Outcome:** 47 raw crashes → 3 bugs, root-caused and exploitability-rated. The
critical heap overflow (5 byte-different inputs) collapses to one entry instead
of five tickets.
