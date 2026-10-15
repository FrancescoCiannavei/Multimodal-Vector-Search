# Demo

Every time we have a new release we need to update the demo.
This directory contains everything claude needs to implement the demo.
The main branch will be merged in the demo branch and rebased (will override anything we have ever done on this branch with the main). Claude will then read the prompt and prepare the demo: disabling seeding, adding a demo warning banner, etc.
Why this approach? I don't want to create a bunch of `if mode == "demo":` in the code, this is supposed to be a Vector Search blue print and example, the demo comes second.
