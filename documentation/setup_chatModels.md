# write markdown

# Chat models
In this course, we'll use Chat Models, which take a sequence of messages as input and return messages as output. 
LangChain supports many models via third-party integrations. By default, the course will use ChatOpenAI because it is both popular and performant. 
As noted, please ensure that you have an OPENAI_API_KEY.

Let's check that your OPENAI_API_KEY is set and, if not, you will be asked to enter it.

#### Code:
Run :   %%capture --no-stderr
        %pip install --quiet -U langchain_openai langchain_core langchain_community langchain-tavily

        import os, getpass

    ```def _set_env(var: str):
            if not os.environ.get(var):
            os.environ[var] = getpass.getpass(f"{var}: ")

        _set_env("OPENAI_API_KEY")```

If you've run pip install -r requirements.txt as noted in the README, then you've installed the langchain-openai package. With this, we can instantiate our ChatOpenAI model object. You can see pricing for various models here. The notebooks will default to gpt-4o because it offers a good balance of quality, price, and speed, but you can also opt for the lower-priced gpt-3.5 series or more recent models.

There are a few standard parameters that we can set with chat models. Two of the most common are:
    * model: the name of the model(ex: gpt-4o)
    * temperature: the sampling temperature
Temperature controls the randomness or creativity of the model's output where low temperature (close to 0) is more deterministic and focused outputs. This is good for tasks requiring accuracy or factual responses. High temperature (close to 1) is good for creative tasks or generating varied responses.

#### Code:
Run : from langchain_openai import ChatOpenAI
      #gpt4o_chat = ChatOpenAI(model="gpt-4o", temperature=0)
      gpt35_chat = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)

Chat models in LangChain have a number of default methods. For the most part, we'll be using:
    * stream: stream back chunks of the response    
    * invoke: call the chain on an input
And, as mentioned, chat models take messages as input. Messages have a role (that describes who is saying the message) and a content property. We'll be talking a lot more about this later, but here let's just show the basics.

#### Code:
Run :```
        from langchain_core.messages import HumanMessage

        # Create a message
        msg = HumanMessage(content="Hello world", name="Lance")

        # Message list
        messages = [msg]

        # Invoke the model with a list of messages 
        gpt35_chat.invoke(messages)    ```

OR  
We get an AIMessage response. Also, note that we can just invoke a chat model with a string. When a string is passed in as input, it is converted to a HumanMessage and then passed to the underlying model.

#### Code:
Run :```  gpt4o_chat.invoke("hello world")  ```

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