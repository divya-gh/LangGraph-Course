# Setting Up chat models

Since langgraph academy course uses OpenAi API which is paid , we will not be using openai models

## Google GenAI

# Chat models
Chat Models, which take a sequence of messages as input and return messages as output. 
LangChain supports many models via third-party integrations. In this course lets use google genai which is free

#### Set up : GenAI: Required for primary course lessons. Set up GenAI API key 
1.  Got to aistudio.google.com to create an API key
2. Activate virtual environment 
3. Install Gemini SDK : Install Google’s newer, lighter-weight SDK designed to avoid protobuf conflicts -google genai
bash
  ```
  source venv/Scripts/activate

  pip install google-genai
  pip install langchain-google-genai

```

  * Add the google API ke in .env → GOOGLE_API_KEY="your-genai-key"
  * Save and add it to .gitignore to protect the API key.
  * Reactivate your environment: Code source venv/Scripts/activate
  * 🧪 Verify it worked Run: echo $GOOGLE_API_KEY
  * If it prints your key, you're all set.

4. activate api key for genai
  * If you’re using a .env file, load it in your notebook:

  python
```
    from dotenv import load_dotenv
    load_dotenv()

```
5.connect to genai:
notebook:
```
    import google.generativeai as genai
    import os
    os.environ["GOOGLE_API_USE_V1"] = "true"     #LangChain defaults to the old API.

    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    print([m.name for m in genai.list_models()])

    ```
  prints available models. use one.

5.  LangChain’s Gemini wrapper supports:

- gemma-3-4b-it
- gemini-2.5-flash-lite
- veo-3.1-lite-generate-preview
- gemini-2.5-flash
- gemini-2.5-pro
- gemini-3.1-flash-live-preview and more!

(Use any of the above)
6. example code:
notebook:
    ```
    from dotenv import load_dotenv
    load_dotenv()
    os.environ["GOOGLE_API_USE_V1"] = "true"

    from langchain_google_genai import ChatGoogleGenerativeAI

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2
    )

    messages = [
        ("human", "Hello Gemini, how are you?")
    ]

    result = llm.invoke(messages)
    print(result.content)

    ```

# Alternatively you can make sure API key is available to use by

#### Code:
Run :   %%capture --no-stderr
        import os, getpass

    ```
        def _set_env(var: str):
            if not os.environ.get(var):
            os.environ[var] = getpass.getpass(f"{var}: ")

        _set_env("OPENAI_API_KEY")
    ```


### Parameters: 
There are a few standard parameters that we can set with chat models. Two of the most common are:

    * model: the name of the model(ex: gemini-2.5-flash)
    * temperature: the sampling temperature

Temperature controls the randomness or creativity of the model's output where low temperature (close to 0) is more deterministic and focused outputs. This is good for tasks requiring accuracy or factual responses. High temperature (close to 1) is good for creative tasks or generating varied responses.

## Calling: Chat models in LangChain have a number of default methods. For the most part, we'll be using:

    * stream: stream back chunks of the response    
    * invoke: call the chain on an input

And, as mentioned, chat models take messages as input. 
Messages have a role (that describes who is saying the message) and 
              a content property(user message or system message) 
We'll be talking a lot more about this later, but here let's just show the basics.

#### Code:
Run :```
        from langchain_core.messages import HumanMessage

        # Create a message
        msg = HumanMessage(content="Hello world", name="Lance")

        # Message list
        messages = [msg]

        # Invoke the model with a list of messages 
        llm.invoke(messages)    
    ```

OR  
We get an AIMessage response. 
Also, note that we can just invoke a chat model with a string. When a string is passed in as input, it is converted to a HumanMessage and then passed to the underlying model.

#### Code:
Run :```     result = llm.invoke("Hi Who are you")
             print(result.content)  
```

## Search Tools
You'll also see Tavily in the README, which is a search engine optimized for LLMs and RAG, aimed at efficient, quick, and persistent search results. As mentioned, it's easy to sign up and offers a generous free tier. Some lessons (in Module 4) will use Tavily by default but, of course, other search tools can be used if you want to modify the code for yourself.

#### Code:
Run :```  _set_env("TAVILY_API_KEY")

        from langchain_tavily import TavilySearch  # updated at 1.0
        tavily_search = TavilySearch(max_results=3)

        data = tavily_search.invoke({"query": "What is LangGraph?"})
        search_docs = data.get("results", data)   
        search_docs    
        ```