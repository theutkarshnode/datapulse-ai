import re

with open("agent/nodes.py", "r") as f:
    code = f.read()

# 1. Force max_tokens=4096 so code never cuts off mid-line
if "max_tokens" in code:
    code = re.sub(r'(["\']?max_tokens["\']?\s*[:=]\s*)\d+', r'\g<1>4096', code)
elif "chat.completions.create(" in code:
    code = code.replace("chat.completions.create(", "chat.completions.create(\n        max_tokens=4096,", 1)
elif '"messages":' in code:
    code = code.replace('"messages":', '"max_tokens": 4096,\n        "messages":', 1)

# 2. Add concise numeric parsing rule so messy strings ($50,000+, $100 - $149 / hr) don't bloat code
rule = (
    "CRITICAL: Keep total Python script under 80 lines. Never write custom string-splitting helper functions. "
    "For messy currency, range, or percentage columns (e.g. '$50,000+', '$100 - $149 / hr', '10%'), "
    "always extract the first number in one line: "
    "pd.to_numeric(df[col].astype(str).str.replace(',', '').str.extract(r'(\\d+\\.?\\d*)')[0], errors='coerce'). "
)

if "CRITICAL: Keep total Python script" not in code:
    code = re.sub(r'(def coder_node[\s\S]{0,400}?"""|\'\'\')', r'\1\n' + rule + '\n', code, count=1)

with open("agent/nodes.py", "w") as f:
    f.write(code)

print("Patched agent/nodes.py successfully!")
