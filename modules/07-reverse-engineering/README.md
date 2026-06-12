# Module 07 — Reverse Engineering

RE tools turn binaries into something readable: disassembly, decompiled C,
control-flow graphs. The output is correct but *unlabeled* — `FUN_00401a20`,
`uVar3`, no comments. The slow part of RE is building a mental model of what the
code does. That summarization-and-naming work is a natural AI augmentation.

## Tools you tour

- **Ghidra** — NSA's open-source SRE suite; great decompiler, scriptable in
  Python/Java (headless mode for automation).
- **radare2 / rizin** — scriptable CLI RE framework; pipe-friendly.
- **angr** — symbolic execution and binary analysis in Python; solve for inputs
  that reach a target block.

### Tour tasks

```bash
# Ghidra headless: decompile and dump pseudo-C for scripting
analyzeHeadless ./proj ghidra_proj -import target.bin -postScript DumpDecomp.py

# radare2: decompile a function
r2 -q -c "aaa; s sym.main; pdc" target.bin
```

Grab the decompiled pseudo-C for one function. It's accurate and unreadable —
exactly the input a model can summarize and propose names for.

## AI augmentation: decompiled-function summarizer + rename suggester

Build a Ghidra/radare2 post-script that, for each interesting function, sends the
decompiled pseudo-C to the model and gets back:

- a one-line summary of what the function does,
- suggested meaningful names for the function and its variables,
- a guess at its role (parser, crypto, network, auth check), and
- any security-relevant observations (unbounded copy, hardcoded key, weak check).

Define a `FunctionAnalysis` schema. Then have the Ghidra script *apply* the
suggested names back into the database — but gate destructive/global renames
behind review, and keep the original names recoverable.

> Caution with provenance: decompiled code from an untrusted binary is untrusted
> input. You're asking the model to *describe* it, not execute it — keep it that
> way.

## Exercises

1. Summarize and rename a single function from a crackme; verify the names make
   the next function easier to read.
2. Batch over all functions and produce a call-graph-ordered "tour" of the
   binary (entry point first), so you get a narrative of the whole program.
3. Use angr to find an input reaching a `win()` block, then have the model
   explain the constraints angr solved in plain language.

## Done when

- You can take a stripped function's pseudo-C and get an accurate summary plus
  applied, meaningful names — and a binary's worth of these turns hours of
  staring into a guided read.

## Resources

Curated entry points to learn the tools and concepts for this module — official docs and authoritative references. They get you grounded; the build is still yours.

- [Ghidra](https://github.com/NationalSecurityAgency/ghidra)
- [radare2 book](https://book.rada.re/)
- [angr docs](https://docs.angr.io/)
- [crackmes.one (practice targets)](https://crackmes.one/)
