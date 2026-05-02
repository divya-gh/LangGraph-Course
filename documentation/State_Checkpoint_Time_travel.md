# State_History :Checkpoint - Time Travel

### LangGraph supports time travel through checkpoints:
## Replay: Retry from a prior checkpoint.
## Fork: Branch from a prior checkpoint with modified state to explore an alternative path.

- Both work by resuming from a prior checkpoint. 
- Nodes before the checkpoint are not re-executed (results are already saved). - - Nodes after the checkpoint re-execute, including any LLM calls, API requests, and interrupts (which may produce different results).

### Meaning:

LangGraph automatically creates checkpoints as your graph runs (if you’re using a checkpointer or LangSmith/Cloud):

#### Replay: Re-run from a past checkpoint to see what would happen again.

#### Fork: Start a new branch from a past checkpoint, possibly with changed input/state.

### Key idea:
- Nodes before the checkpoint are not re-executed (their results are reused).
- Nodes after the checkpoint run again—LLM calls, tools, interrupts, everything.

## To use time travel, you need:

### 1. Checkpointing enabled

- Local: pass a checkpointer (e.g. InMemorySaver, DB, etc.) to compile()
- LangSmith / LangGraph Cloud: persistence is built-in

### 2. A thread_id

- This identifies the “timeline” (conversation/run) our time-traveling within.
- We have already use thread["thread_id"] in our notebook—that’s our timeline.

## How checkpoints get created
We don’t usually create checkpoints manually—LangGraph does it for you:

    - At the start of the run
    - After nodes finish
    - Around interrupts
So every time your graph progresses, it’s leaving “save points” you can jump back to.

# Time travel via Replay (conceptual steps)
### Goal: Re-run from a previous checkpoint to see what happens again.

## Step-by-step (high level):
1. Run your graph once
- It creates checkpoints as it goes.

2. Pick a checkpoint to replay from: 
- In LangSmith Studio: select a step/checkpoint in the run UI.
- Conceptually: “I want to start again from here.”

3. Replay: 
- LangGraph loads the saved state at that checkpoint.
- Nodes before that checkpoint are not re-run.
- Nodes after that checkpoint are executed again.
- Any LLM calls / tools / interrupts after that point happen again (and may differ).

In LangSmith UI, this is usually a “Replay” action on a run/step; under the hood it’s just “resume from this checkpoint as if we were here again.”

# Time travel via Fork (conceptual steps)
### Goal: Start a new branch from a past checkpoint, possibly with changes.

## Step-by-step:
1. Run your graph once:
- Checkpoints are created.

2. Choose a checkpoint to fork from:
- In LangSmith Studio: pick a step/checkpoint.

3. Create a fork
- Start a new run/thread whose initial state is that checkpoint’s state.
- Optionally modify:
```
Input (e.g. change "input": "Tell me a joke" → "input": "Explain quantum physics")
```
- and Other state fields

4. Run the forked branch
- Nodes before the checkpoint are reused.
- Nodes after the checkpoint run fresh with your new state.
- This lets you explore “what if we had done X instead?” without touching the original run.

## Mental model to keep in your head
#### Thread = timeline
#### Checkpoint = save point
#### Replay = load save and continue same story
#### Fork = load save and start an alternate story