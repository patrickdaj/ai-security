# Module 06 — Fuzzing

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/patrickdaj/ai-security?quickstart=1)

> Opens a ready-to-build cloud environment (Python + scanners pre-installed). Build in `project/`; the worked answer is in `reference/`.


Fuzzers throw mutated inputs at a target to find crashes. They're brilliant at
exploration and terrible at two human-heavy chores: *writing the harness* in the
first place, and *triaging a pile of crashes* (which are unique? which are
exploitable? what's the root cause?). Both are strong AI augmentation targets.

## Tools you tour

- **AFL++** — coverage-guided fuzzer for native code; the standard.
- **libFuzzer** — in-process, compile a `LLVMFuzzerTestOneInput` entry point.
- **Atheris** — Google's coverage-guided fuzzer for *Python*; easiest on-ramp.

### Tour tasks

```bash
# Atheris (Python) — fastest way to see fuzzing work
pip install atheris
python modules/06-fuzzing/project/example_fuzz.py    # see project/ for a stub

# libFuzzer (native)
clang -g -fsanitize=address,fuzzer target.c -o target_fuzzer && ./target_fuzzer
```

Get one crash. Look at the ASan/stack trace. That trace is dense, repetitive,
and perfect for a model to summarize and deduplicate.

## AI augmentation: harness generator + crash triage/dedup/root-cause

Two builds:

1. **Harness generator.** Given a function signature or a C/Python source file,
   generate a fuzzing harness (Atheris `TestOneInput` or libFuzzer entry point)
   that maps fuzz bytes onto the function's inputs sensibly (not just one blob —
   split into the args it actually takes). Validate it compiles/runs.
2. **Crash triage.** Ingest crash artifacts + sanitizer output, and have the
   model: deduplicate by root cause (not by input bytes), classify
   exploitability (write-what-where vs. null deref), and produce a root-cause
   paragraph pointing at the offending line.

For triage, define a `CrashAnalysis` schema (bug_class, likely_root_cause,
exploitability, dedup_key). The `dedup_key` is the clever bit — ask the model
for a stable key derived from the crashing call site so byte-different crashes
collapse to one.

## Exercises

1. Generate an Atheris harness for a function with a planted bug; confirm it
   finds the crash.
2. Triage 20 crashes from one campaign and verify the model collapses them to
   the true number of distinct bugs.
3. Have the model propose the *fix* for the root cause and a regression test
   (the crashing input as a seed).

## Done when

- You can point the generator at a buggy function and get a working harness, and
  turn a folder of crashes into a deduplicated, root-caused, exploitability-rated
  list.

## Resources

Curated entry points to learn the tools and concepts for this module — official docs and authoritative references. They get you grounded; the build is still yours.

- [AFL++](https://aflplus.plus/)
- [libFuzzer](https://llvm.org/docs/LibFuzzer.html)
- [Atheris (Python)](https://github.com/google/atheris)
- [Google fuzzing guide](https://github.com/google/fuzzing)
- [OSS-Fuzz](https://google.github.io/oss-fuzz/)
