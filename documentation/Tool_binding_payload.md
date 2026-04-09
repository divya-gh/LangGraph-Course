# How do the LLM model coommunicate with external Tools?

### Analogy:
- Talking to an LLM is like talking to a person.
- Talking to an API is like filling out a form.

The “payload” is the filled-out form.

#### Humans talk in natural language.
You can say: “Book me a flight to New York tomorrow.”

#### APIs do NOT understand natural language.
They expect a structured payload, like:
```
json
{
  "destination": "New York",
  "date": "2026-04-10",
  "seat_class": "economy"
}
```
# Payload : Input schema
This is what “input schema or payload” means:

    - A strict, machine-readable structure that an API requires.
    - If you send natural language to an API, it will fail.

## 🌟 Why this matters for agents and LangGraph
When an LLM calls a tool (like a weather API, database, calculator, or search engine), it must output structured data, not a sentence.

Example: ❌ Bad (natural language)
Code
```
Can you check the weather in Austin for me?
```

✅ Good (payload) :
```
json
{
  "location": "Austin, TX",
  "units": "metric"
}
```
##### LangChain, LangGraph, and MCP all rely on this idea: The LLM must produce a payload that matches the tool’s schema.

## 🌟 Why LLMs need schemas ?
APIs are strict.
If the schema says:
```
json
{
  "city": "string",
  "date": "string"
}
```
Then this will fail:
json
```
{
  "location": "Austin"
}
```

##### this is why tools define schemas to ensure:
- predictable inputs
- correct types
- no missing fields
- no extra fields
- no ambiguity

This is why LangChain uses Pydantic models, and MCP uses JSON schemas.

## Example from LangGraph
If you define a tool like: python
```
class WeatherInput(BaseModel):
    city: str
    date: str
```
Then the LLM must output: json
```
{
  "city": "San Antonio",
  "date": "2026-04-10"
}
```
NOT: “What’s the weather in San Antonio tomorrow?”

That’s the difference between natural language and payload.

## 🌟 Why this matters for you right now
We’re learning:
- LangGraph
- Gemini
- Tools
- Agents
- MCP

All of these require the LLM to produce structured payloads when interacting with external systems. This is the core idea behind tool calling.
