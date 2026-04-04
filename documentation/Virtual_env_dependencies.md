# Generate a markdown for creating vertual environment and dependencies to run langGraph code

## ✅ 1. Create the virtual environment (if you haven’t yet)
bash
```
python3 -m venv venv
```
This creates a folder named venv/ containing your isolated environment.

## 🚀 2. Activate the venv -Windows
bash
```
source venv/Scripts/activate
```
3. Confirm it worked
After activation, your shell prompt should change to something like:

Code
```
(venv) user@machine:~/project$
```

## 📦 How to install LangGraph in your venv
After activating your venv:

bash
```
source venv/bin/activate
Then install LangGraph:

bash
pip install langgraph
If you're following LangChain Academy or LangGraph tutorials, you may also need:

bash
pip install langchain langchain-core langchain-community
And if your notebook uses Jupyter:

bash
pip install ipykernel
python -m ipykernel install --user --name=venv
```
This makes your venv appear as a selectable kernel in Jupyter.

## Verify your Jupyter kernel is using your venv

### Step 1 — Check the kernel name inside Jupyter
In the top-right of your notebook, you should see something like:

Code
```
Python 3 (ipykernel)
```
This tells you the kernel, not necessarily the venv.
If your venv was properly registered, it would usually show something like:
Code
```
venv (Python 3.x)
```

### Step 2 — Verify from inside the notebook
Run this in a notebook cell:
python
```
import sys
sys.executable
```
If the output path contains your venv folder, for example:
Code
```
/home/user/project/venv/bin/python
```
then you're good.

If it shows something like:
Code
```
/usr/bin/python3
```
or a system Python path, then your notebook is not using your venv.

### Step 3 — Add your venv as a Jupyter kernel (if needed)
Activate your venv in the terminal:
bash
```
source venv/bin/activate
```
Install the kernel helper:
bash
```
pip install ipykernel
```
Register your venv as a Jupyter kernel:
bash
```
python -m ipykernel install --user --name=venv --display-name="venv"
```
Now restart Jupyter and select the kernel named venv.

### Step 4 — Re‑check inside the notebook
Run again:
python
```
sys.executable
```
You should now see your venv path.