# Project Multimodal-Vector-Search

> [!WARNING]
> This project is a work in progress. Features may be incomplete, and APIs or behavior may change without notice.

Control the [progress](./TODO.md).

Read the [docs](./docs/README.md).

Switching modes on an already-seeded database silently breaks search
The two models produce vectors that can't be compared, and the Postgres volume survives rebuilds.
If you seeded locally and then flip the flag, searches won't error; they'll just return meaningless results.
You need a full re-seed after every switch.