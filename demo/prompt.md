# Prompt

This is the demo branch, we just merged main into it and rebased it.
The demo runs on the free Gemini API plan and we have no idea how many people are going to try it, it will cut us off when we reach the limit.
Prepare the demo by applying the steps below and nothing else. Don't add `if mode == "demo":` conditionals anywhere, `demo/README.md` explains why.

## Before you start

Run `git branch --show-current`. If it isn't `demo`, stop and tell me, these steps must never land on main.

A rebase can replay the previous demo's commits, so a step may already be applied. Check first, and never apply a step twice.

## Steps

### 1. Fake seeding

The heaviest part of this app is the seeding, it embeds every file under `data/` with Gemini.
Users still need to be able to try the seeding feature, the page shows a disclaimer (step 2) and we just pretend to seed the data.
`demo/fake_seed.py` is a full replacement for `src/seed.py`: it streams the same events, but never calls the embedding API or writes to the database.

`demo/fake_seed.py` was written against an older `src/seed.py`, so before swapping, check main hasn't drifted from it.
Compare against main's version (`git show main:src/seed.py`), the working tree copy may already be the fake:

- Every name other modules import from `seed` exists in the fake: `grep -rn "from seed import" src`. Today that's `seed` (`main.py`) and `titleFromPath` (`retrive.py`).
- `MODALITY_BY_EXTENSION` matches main's, otherwise the fake rejects files of any new type.
- `main.py` still consumes `seed()` the same way (a sync generator iterated in a for loop), and the events still have the fields `public/js/seed.js` reads.

If anything drifted, update `demo/fake_seed.py` first, so it stays current for the next release.
Then replace the contents of `src/seed.py` with `demo/fake_seed.py`.

Only seeding is faked. Search (`/api/retrive`) still calls Gemini once per query, and that's intended: leave search, the embedders (`src/embed/`) and the database code alone.

### 2. Warning banner

Insert the content of `demo/warning.html` into `public/html/seed.html`, under the `<p class="lead">` element and above the `<div class="seed-options">`.
Re-indent it with tabs to match the surrounding markup.
If either of those elements no longer exists, stop and ask me where the banner should go instead of guessing.

## When you're done

- `git diff main --stat` must only list `src/seed.py`, `public/html/seed.html` and files under `demo/`. If anything else changed, revert it or tell me why it had to.
- From the repo root, check the fake seed streams events end to end: `python3 -c "import sys; sys.path.insert(0, 'src'); from seed import seed; print(list(seed(['data/text/coffee.txt'])))"`
- Don't commit or push, leave the changes for me to review.
