from tools import read_file

def validate_project():
    errors = []

    html = str(read_file.invoke({"path": "index.html"}) or "")
    js = str(read_file.invoke({"path": "script.js"}) or "")
    css = str(read_file.invoke({"path": "style.css"}) or "")

    html_lower = html.lower()

    def is_missing(content):
        return (not content.strip()) or content.startswith("ERROR")

    if "<!doctype html>" not in html_lower:
        errors.append("Missing DOCTYPE declaration")

    if "<html" not in html_lower:
        errors.append("HTML missing <html> tag")

    if "<body" not in html_lower:
        errors.append("HTML missing <body> tag")

    if "style.css" in html_lower and is_missing(css):
        errors.append("CSS file missing or empty")

    if "script.js" in html_lower and is_missing(js):
        errors.append("JS file missing or empty")

    if "style.css" not in html_lower:
        errors.append("CSS not linked in HTML")

    if "script.js" not in html_lower:
        errors.append("JS not linked in HTML")

    if ("import " in js or "export " in js) and 'type="module"' not in html_lower:
        errors.append("JS uses modules but HTML doesn't enable module script")

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }

# def llm_validate():
#     html = read_file.invoke({"path": "index.html"})
#     js = read_file.invoke({"path": "script.js"})
#     css = read_file.invoke({"path": "style.css"})

#     prompt = f"""
# Check if this project is valid and runnable.

# HTML:
# {html}

# JS:
# {js}

# CSS:
# {css}

# List problems only.
# """

#     return llm.invoke(prompt).content

