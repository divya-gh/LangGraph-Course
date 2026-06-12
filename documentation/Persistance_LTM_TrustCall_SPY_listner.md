## SPY - TrustCall Json Patch / Json Doc Observability

**“TrustCall is doing smart stuff under the hood—patches, self‑corrections, updates. I want to see that.”**

#### Note: extractor so every run passes through it and you can inspect what tools were called and how the JSON was patched.

## 1. Understand what TrustCall is doing internally
When you call a TrustCall extractor:
```
trust_extractor = create_extractor(...)
result = trust_extractor.invoke({...})
```
#### TrustCall may internally:
- Call your schema tool (e.g. UserProfile, Memory, Memory_collection)

#### Call its own tools:
 -PatchDoc → apply JSON Patch updates
- PatchFunctionErrors → fix validation errors
- Retry or self‑correct if the model output doesn’t match the schema
All of that happens inside a RunnableSequence.

##### Note: A listener lets you “tap into” that sequence and see each internal tool call.

## 2. Define a simple Spy class
**You want a class that:**
- Receives each run
- Stores them
- Lets you inspect tool calls later

### A beginner‑friendly version:
```
class Spy:
    def __init__(self):
        self.runs = []  # store all runs here

    def __call__(self, run):
        """
        This method will be called by TrustCall for each run.
        `run` is a dict-like object with info about tool calls, errors, etc.
        """
        self.runs.append(run)
```
#### Key idea:
- TrustCall will call spy(run) for each internal execution step.
- You just collect them.

## 3. Attach Spy to the TrustCall extractor

#### When you create the extractor, pass your Spy instance as a listener:
```
spy = Spy()

trust_extractor = create_extractor(
    llm,
    tools=[UserProfile],          # or Memory / Memory_collection
    tool_choice="UserProfile",
    enable_inserts=True,
    enable_updates=True,
    listeners=[spy],              # 👈 this is the important part
)
```
#### Now every time you do:
```
result = trust_extractor.invoke({"messages": updated_messages, "existing": existing})
```

#### TrustCall will:
- Run its internal tools
- Call spy(run) for each step
- Store all those run objects in spy.runs

## 4. What’s inside each run?

#### Each run typically contains:

    - tool_calls → which tools were called, with names and args

    - errors → any validation or patch errors

    - response_metadata → IDs, patch info, etc.

    - result → the final structured output for that step

#### So after you’ve invoked the extractor, you can inspect:
```
for i, run in enumerate(spy.runs):
    print(f"\n=== Run {i} ===")
    print("Tool calls:", run.get("tool_calls", []))
    print("Errors:", run.get("errors", []))
    print("Response metadata:", run.get("response_metadata", {}))
```

#### You’ll see things like:
- Calls to UserProfile (your schema)
- Calls to PatchDoc (JSON Patch updates)
- Calls to PatchFunctionErrors (self‑corrections)

##### Note: This is your visibility window into TrustCall’s behavior.

## 5. Example: focusing on PatchDoc and PatchFunctionErrors
If you specifically want to see how TrustCall is patching and correcting:
```
for run in spy.runs:
    for call in run.get("tool_calls", []):
        name = call.get("name")
        args = call.get("args", {})

        if name == "PatchDoc":
            print("\n🔧 PatchDoc called:")
            print("Patch args:", args)

        if name == "PatchFunctionErrors":
            print("\n⚠️ PatchFunctionErrors called:")
            print("Error fix args:", args)
```

#### bThis gives you:
- Exactly what JSON Patch was applied
- Exactly what validation errors were fixed
- How TrustCall changed the document over time
- Perfect for debugging and for building smarter agents that react to these changes.

## 6. Mental model: what you’ve built

### We have:

    - TrustCall extractor → does structured extraction + JSON Patch updates

    - Spy listener → watches every internal tool call

#### Visibility into:
- What changed
- How it changed
- When self‑corrections happened

#### This is especially useful for:
- Debugging complex schemas
- Understanding why a field was updated
- Providing observability for building responsible agents.
- Building agents that react to specific kinds of changes (e.g. “profile updated”, “memory added”, “error fixed”).

------------------------------------------------------------------------


