# Module conventions

Every module follows the same three-part structure so the curriculum is
consistent end to end. When you open any module you'll find:

```
modules/NN-name/
├── README.md          # the tour, the build tasks, exercises, done-when
├── project/           # YOUR build. Starter stubs with TODOs / NotImplementedError.
│   └── *.py           # complete these — this is the work.
├── reference/         # a worked solution. Study it; don't copy it before you try.
│   └── *.py
└── example-output/    # the target: what a good run produces.
```

## How to use a module

1. **Read `README.md`** — concepts, the tool tour, and the build tasks.
2. **Look at `example-output/`** — this is the artifact you're aiming to produce.
3. **Build in `project/`** — fill in the TODOs. Run your tool, normalize into
   `aug.Finding`, reason with a typed schema via the `aug` library.
4. **Check `reference/`** — when you're stuck, or to compare after you're done.
   The reference is correct and runnable, but the learning is in writing your own.

## The rule of thumb

- **`aug/` and `automation/`** at the repo root are *shared infrastructure /
  reference* — given complete, like a standard library you build on.
- **`modules/*/project/`** is *yours to build*. If a file there has no TODOs,
  it's an input fixture (sample data) or a deliberately-complete example (e.g. a
  planted-bug fuzz target), not a solution to a build task.
- **`modules/*/reference/`** mirrors the project — it's the worked answer.

Inputs the project needs (sample flows, recorded events, vulnerable Terraform)
live alongside the stub in `project/`; they're fixtures, not work.
