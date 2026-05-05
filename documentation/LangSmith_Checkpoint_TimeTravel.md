# LangSmith API Time Travel

##### Time Travel the graph by replaying and forking from a checkpoint

Time travel = replaying or forking a LangGraph run from a past checkpoint.  
In local development, this is done through the LangSmith API (as in your notebook) or through LangGraph Studio.

### Checkpoint:  A checkpoint is a snapshot of your graph’s state at a specific step.
It includes:

    - values (your state)
    - next (which node(s) should run next)
    - tasks (pending node executions)
    - metadata (graph_id, run_id, step, etc.)
    - checkpoint_id (unique identifier)

## Replay: “Start a new run using the state stored in this specificcheckpoint.”

### 1. get State: get current state
```
current_state = await client.threads.get_state(thread['thread_id'])
```
Shows current state that is after a comple run

### 2. get state History:
- To replay , get the checkpoint id or config using get_state_history
- First snapshot (state_history[0]) listed is the current state
- get the checkpoint for a specific node (Ex: assistant node )
```
state_history = await client.threads.get_history(thread['thread_id'])

# get checkpoint created at assistant node  - next = assistant
replay_state = state_history[-2]
```
shows the snapshot of the specific node saved at a checkpoint

### 3.### Get checkpoint ID
```
checkpoint_id = replay_state['checkpoint_id']
```
captures specific checkpoint to replay

### Replay:
```
async for chunk in client.runs.stream(
    thread['thread_id'],
    assistant_id='agent',
    input = None,
    stream_mode="updates",
    checkpoint_id=checkpoint_id
):
    print(chunk.data)
    #messages = chunk.data.get('messages',[])
    #print(messages)
    print("\n")
```
Replay from specified checkpoint_id
    - Creates a new run-id and timeline
    - Doesnot overwrite, mutate or continue old run
    - Restores initial checkpoints and executes the graph again.
    -  may result a different outcome

### 🔍 What actually happens under the hood
When you replay:
- LangGraph loads the saved state from the original checkpoint
- It starts a new execution context
- Every node that runs writes a new checkpoint entry into the checkpointer

original run created checkpoints:
- C0 → C1 → C2 → C3

When you replay from C2:
- Original run:   C0 → C1 → C2 → C3
- Replay run:     C2' → C3' → C4'

Notice:
- C2' is a copy of C2
- C3' and C4' are new checkpoints created during replay
-----------------------------------------------------------------

## Fork - -  Forking: Creating a new run or thread starting from an existing one, usually with small changes (prompt, config, code).

    - Create a new thread
    - use messases.id to modify the content

### get state history:
- capture specific node to fork from
- modify the original state message if needed
- capture message id and checkpoint id

```
state_history =  await client.threads.get_history(thread['thread_id'])
#capture specific node
to_fork = state_history[-2]

# checkpoint id
checkpoint_id = to_fork['checkpoint_id']

# message_id 
msg_id = to_fork['values']['messages'][0]['id']
msg_id
```

### edit/Modify state
Remember how our reducer on `messages` works: 

    - It will append, unless we supply a message ID.
    - We supply the message ID to overwrite the message, rather than appending to state!
    - add id to the input message to modify the original input
```
forked_input = {"messages": HumanMessage(content="divide 10 and 3",
                                         id=msg_id)}

forked_config = await client.threads.update_state(
    thread["thread_id"],
    forked_input,
    checkpoint_id=checkpoint_id
)
forked_config
```
### Check current state
Current state must show the modified state in the node where state is updated
```
cur_state = await client.threads.get_state(thread['thread_id'])
```

### confirm next node
```
cur_state['next'] 
```
shows the next node to run

### Get checkpoint id from forked branch to re-run the graph
```
checkpoint_id = forked_config['checkpoint_id']
```
### re-run the updated graph with new checkpoint id created while branching
```
async for chunk in client.runs.stream(
    thread["thread_id"],
    assistant_id="agent",
    input=None,
    stream_mode="updates",
    checkpoint_id= forked_config['checkpoint_id']
):
    print(chunk.data)
    print("\n")
```
Graph is branched with new timeline 

------------------------------------------------------------------
# LangSmith Tracing UI forking and replay guide

## 1. Core concepts
#### Run: A single execution of your app (graph, chain, tool, or LLM call).

#### Thread: A conversation or session that groups related runs.

#### Forking: Creating a new run/branch or thread starting from an existing one, usually with small changes (prompt, config, code).

#### Replay: Re‑executing a past run (or thread) to see what happens now—often after you’ve changed code, prompts, or models.

## 2. Prerequisites
LangSmith account: You can log into the LangSmith UI.

Tracing enabled in your app:  
Typical .env vars (Python/JS): 
```
export LANGCHAIN_TRACING_V2="true"
export LANGCHAIN_API_KEY="YOUR_KEY"
export LANGCHAIN_PROJECT="my-project"
```
At least one traced run: Your app has been executed once so you can see runs in LangSmith.

## 3. Forking: step‑by‑step

### 3.1 Forking a run from LangSmith UI
- Open a run
- Go to Runs / Traces in LangSmith.
- Click on a run you want to inspect (often the root run of a thread).
- Inspect inputs and outputs

#### Look at:
- Inputs: user message, parameters, tools, config.
- Outputs: final answer, intermediate steps.
- Click “Fork” (or similar action)
- In the run detail view, find the Fork or Clone button.
- This creates a new run configuration based on the original.
- Modify what you care about

#### Common edits:
- Prompt text (e.g., clarify instructions).
- Model settings (temperature, model name).
- Tool parameters or system message.
- Keep changes small so you can clearly see their effect.
- Run the fork
- Click Run (or Replay/Fork & Run) to execute the new version.

#### Compare:
- Old vs new outputs.
- Latency, cost, and errors.
- Save as experiment or dataset (optional)

#### If this fork is promising, you can:
- Add it to an experiment for A/B testing.
- Save the input/output pair into a dataset for future evaluation.

### 3.2 Forking a thread into LangGraph Studio (if you’re using LangGraph)
- Open the root run of a thread in LangSmith.
- Click “Run in Studio” or “Clone thread locally” (wording may vary).

#### Choose:
- Remote deployment (if you have a deployed agent), or
- Local URL (if you’re running LangGraph locally).

#### LangGraph Studio opens with:
- The thread history reconstructed.
- The graph view showing nodes and edges.

#### From there you can:
- Change graph code locally.
- Re‑run the same thread to see how behavior changes.

---------------------------------------------------------------------------

## 4. Replay: step‑by‑step

### 4.1 Replaying a single run
Open the run in LangSmith.

#### Confirm:
- Inputs (user query, config).
- Environment (project, model).
- Click Replay (or Run again).

#### Observe:
- Does the output change?
- Are there new errors?
- Did latency or cost change?

#### Typical use cases:
- You updated a prompt and want to see if it fixes a bug.
- You switched models (e.g., gpt-4 → gpt-4.1) and want to compare behavior.
- You changed tool logic and want to confirm it still works on old inputs.

### 4.2 Replaying with code changes (LangGraph Studio)
Clone the thread locally from LangSmith into LangGraph Studio.

#### In your local code:
- Modify nodes, tools, or state logic.

#### In Studio:
- Re‑run the same thread.
- Step through node by node.

#### Compare:
- Old trace (from production) vs new local run.
- Where behavior diverges (different node, different tool call, different LLM output).

## 5. Usage patterns:

### 5.1 Debugging a bad answer
- Find the user report (e.g., “answer was wrong”).
- Locate the corresponding run in LangSmith.

#### Inspect:
- Prompts, tools, intermediate steps.

#### Fork the run:
- Adjust prompt to be more explicit.
- Maybe change temperature or add a guardrail.

#### Replay and compare:
- Did the answer improve?
- If yes, consider updating your production prompt.

### 5.2 Investigating timeouts or “hanging” behavior
Open the slow or failed run.

#### Look at:
- Which node/tool took the longest.
- Any errors or retries.

#### Fork with:
- Different timeout settings.
- Simplified tool call.

#### Replay:
Confirm whether the change removes the bottleneck.


### 5.3 Regression testing after a change
Collect a small dataset of important inputs (10–50 examples).

#### For each example:
- Use the existing run as a baseline.
- After changing code/prompt/model:
- Replay those runs (or re‑run the dataset).

#### Compare:
- Where outputs improved.
- Where they got worse (regressions).

#### Decide:
- Ship, tweak, or roll back.

## 6. Benefits of forking and replay
#### Faster debugging:  
You don’t have to guess what happened—you can see the exact path and re‑run it.

#### Safe experimentation:  
Try new prompts, models, or tools on real user traces without touching production.

#### Reproducibility:  
When someone says “it broke,” you can replay the exact scenario instead of approximating it.

#### Better learning:  
As a beginner, you see how small changes in prompts or configs affect behavior, step by step.

#### Continuous improvement:  
Turn real user traces into a feedback loop: fork → replay → evaluate → update.


