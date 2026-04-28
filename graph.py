from dotenv import load_dotenv
from langgraph.graph import StateGraph
from langgraph.constants import END
from prompts import coder_system_prompt
from tools import write_file
import os
import json
import re
from groq import Groq
import webbrowser
import time

load_dotenv()

# -------------------------
# Groq Setup
# -------------------------
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# -------------------------
# Groq Call
# -------------------------
def groq_call(messages):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0,
            max_tokens=4096
        )
        return response.choices[0].message.content
    except Exception as e:
        print("❌ Groq failed:", e)
        return None


# -------------------------
# Extract JSON (LIST + OBJECT)
# -------------------------
def extract_json(text: str):
    if not text:
        return None

    text = re.sub(r"```json", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)

    # Try LIST first
    try:
        start = text.find("[")
        if start != -1:
            return json.loads(text[start:])
    except:
        pass

    # Try OBJECT
    try:
        start = text.find("{")
        if start != -1:
            return json.loads(text[start:])
    except:
        pass

    return None


# -------------------------
# Safe LLM Call
# -------------------------
def safe_llm_call(messages):
    time.sleep(2)  # 🔥 Prevent rate issues

    res = groq_call(messages)

    if not res:
        raise Exception("❌ Groq failed")

    parsed = extract_json(res)

    if not parsed:
        raise Exception("❌ Invalid JSON from Groq")

    print("⚡ GROQ used")
    return parsed


# -------------------------
# Quality Check
# -------------------------
def is_incomplete(content):
    return len(content.strip()) < 200


# -------------------------
# CODER AGENT (ONLY NODE)
# -------------------------
def coder_agent(state):
    prompt = f"""
Build a COMPLETE, visually appealing web application.

User request:
"{state["user_prompt"]}"

IMPORTANT:
IMPORTANT:
- Use ONLY relative paths
- CSS must be linked as: <link rel="stylesheet" href="style.css">
- JS must be linked as: <script src="script.js" defer></script>
- NEVER use /static or absolute paths


Requirements:

HTML:
- Full UI layout (display, buttons, structure)
- Proper semantic tags
- Link style.css and script.js

CSS:
- Modern UI (colors, spacing, shadows)
- Centered layout
- Styled buttons with hover effects

JS:
- Fully working logic
- Button click handling
- Dynamic display updates
- Handle invalid inputs

STRICT RULES:
- No minimal code
- No empty UI
- Must look like real product

Return ONLY JSON ARRAY:

[
  {{
    "tool": "write_file",
    "args": {{
      "path": "index.html",
      "content": "FULL HTML"
    }}
  }},
  {{
    "tool": "write_file",
    "args": {{
      "path": "style.css",
      "content": "FULL CSS"
    }}
  }},
  {{
    "tool": "write_file",
    "args": {{
      "path": "script.js",
      "content": "FULL JS"
    }}
  }}
]
"""

    res = safe_llm_call([
        {"role": "system", "content": coder_system_prompt()},
        {"role": "user", "content": prompt}
    ])

    if not isinstance(res, list):
        raise Exception(" Unexpected format from model")

    for item in res:
        if item.get("tool") == "write_file":
            args = item["args"]
            content = args.get("content", "")
            
            if args["path"] == "index.html" :
                content = content.replace("/static/", "")
                args["content"] = content  
            
            if is_incomplete(content):
                raise Exception(" Truncated response")

            args["path"] = args["path"].lstrip("/")
            write_file.invoke(args)

    print(" Files generated successfully")
    return state


# -------------------------
# Graph
# -------------------------
graph = StateGraph(dict)

graph.add_node("coder", coder_agent)

graph.set_entry_point("coder")
graph.add_edge("coder", END)

app = graph.compile()


# -------------------------
# RUN (for testing)
# -------------------------
if __name__ == "__main__":
    result = app.invoke({
        "user_prompt": "Build a modern currency converter from USD to INR using HTML, CSS, and JavaScript"
    })

    print("\n✅ DONE\n", result)

    # Open output
    path = os.path.abspath("generated_project/index.html")
    webbrowser.open(f"file://{path}")