# 🧩 What “summarizing messages” means (simple explanation)
When a chatbot talks for a long time, the message history becomes huge.
LLMs can’t read unlimited history, so we summarize older messages and keep only the important parts.

#### Think of it like compressing a long chat into a short memory.

## Why “summarize?

- Reducers like RemoveMessages , TrimMessages can reduce the no. of messages in the state and help latency and cost but However, can not preserve context. 

- They cut down the cpount of messages or reduce token usage but that can kill context whihc will lead to llm underperformance with qaulity.

### Summerizing the state['messages']:

- With persistant memory, as message hystory grows, latency increases and model performance decrease. 

- By using llms to summerize the past conversations, we can preserve the context and increase performance along with latency. 

## Chatbot Message Summarization (Simple Example):

## 🗂️ Full Conversation (Before Summarization)

1. **User:** Hi, my name is Diya.
2. **Bot:** Nice to meet you, Diya! How can I help?
3. **User:** My favorite color is pink.
4. **Bot:** Great! I’ll remember that.
5. **User:** What can you do?
6. **Bot:** I can answer questions, help you learn, and assist with tasks.

As the conversation grows, we don't want to keep all 6 messages forever.
So we create a short summary.

---

## 📝 Summary Created by the Summarizer Node

**Summary:**  
Diya introduced herself and said her favorite color is pink.  
The assistant greeted her and explained its abilities.

This summary replaces the older messages.

---

## 🗂️ Conversation After Summarization

- **Summary stored in memory**  
- **Only the last 1–2 messages kept**

Example:

**Stored summary:**  
"Diya’s name is Diya, her favorite color is pink, and she asked what the assistant can do."

**Recent messages kept:**  
- User: What is my fav color?  
- Bot: Your favorite color is pink.

---

## 🎯 Why we do this

- Keeps the chatbot fast  
- Prevents token overflow  
- Maintains important facts (name, preferences, goals)  
- Removes unnecessary details  

Live Example: Check the [Chatbot Summarization Notebook](Code/Lesson_2/chat_bot_summerization.ipynb) in the folder Lesson_2



