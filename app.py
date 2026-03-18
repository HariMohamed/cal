from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    result = ""
    a = request.args.get("a", "")
    b = request.args.get("b", "")
    op = request.args.get("op", "add")
    has_result = False

    if a and b:
        try:
            a_val = float(a)
            b_val = float(b)

            if op == "add":
                result = a_val + b_val
            elif op == "sub":
                result = a_val - b_val
            elif op == "mul":
                result = a_val * b_val
            elif op == "div":
                result = a_val / b_val if b_val != 0 else "Cannot divide by zero"
            else:
                result = "Invalid operation"

            has_result = True

        except Exception:
            result = "Invalid input"
            has_result = True

    op_symbols = {"add": "+", "sub": "−", "mul": "×", "div": "÷"}
    result_display = ""
    if has_result:
        if isinstance(result, float):
            result_display = int(result) if result == int(result) else round(result, 8)
        else:
            result_display = result

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calc</title>
    <link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Syne:wght@700;800&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

        :root {{
            --bg: #0a0a0f;
            --surface: #12121a;
            --border: #1e1e2e;
            --accent: #7c3aed;
            --accent-glow: rgba(124, 58, 237, 0.4);
            --accent-light: #a78bfa;
            --text: #e2e8f0;
            --muted: #4a4a6a;
            --result: #34d399;
            --result-glow: rgba(52, 211, 153, 0.3);
        }}

        @keyframes fadeUp {{
            from {{ opacity: 0; transform: translateY(24px); }}
            to   {{ opacity: 1; transform: translateY(0); }}
        }}

        @keyframes pulse-ring {{
            0%   {{ transform: scale(1);   opacity: 0.6; }}
            100% {{ transform: scale(1.6); opacity: 0; }}
        }}

        @keyframes slide-in {{
            from {{ opacity: 0; transform: translateX(-12px); }}
            to   {{ opacity: 1; transform: translateX(0); }}
        }}

        @keyframes shimmer {{
            0%   {{ background-position: -200% center; }}
            100% {{ background-position:  200% center; }}
        }}

        @keyframes blink {{
            0%, 100% {{ opacity: 1; }}
            50%       {{ opacity: 0; }}
        }}

        body {{
            font-family: 'DM Mono', monospace;
            background: var(--bg);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }}

        /* Ambient background blobs */
        body::before, body::after {{
            content: '';
            position: fixed;
            border-radius: 50%;
            filter: blur(80px);
            pointer-events: none;
            z-index: 0;
        }}
        body::before {{
            width: 500px; height: 500px;
            background: radial-gradient(circle, rgba(124,58,237,0.12) 0%, transparent 70%);
            top: -100px; left: -100px;
            animation: float-a 8s ease-in-out infinite;
        }}
        body::after {{
            width: 400px; height: 400px;
            background: radial-gradient(circle, rgba(52,211,153,0.07) 0%, transparent 70%);
            bottom: -80px; right: -80px;
            animation: float-b 10s ease-in-out infinite;
        }}

        @keyframes float-a {{
            0%, 100% {{ transform: translate(0,0); }}
            50%       {{ transform: translate(40px, 30px); }}
        }}
        @keyframes float-b {{
            0%, 100% {{ transform: translate(0,0); }}
            50%       {{ transform: translate(-30px, -20px); }}
        }}

        .card {{
            position: relative;
            z-index: 1;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 40px 36px;
            width: 360px;
            box-shadow:
                0 0 0 1px rgba(124,58,237,0.08),
                0 24px 60px rgba(0,0,0,0.6),
                inset 0 1px 0 rgba(255,255,255,0.04);
            animation: fadeUp 0.5s cubic-bezier(0.22, 1, 0.36, 1) both;
        }}

        /* Subtle top-edge accent line */
        .card::before {{
            content: '';
            position: absolute;
            top: 0; left: 20%; right: 20%;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--accent), transparent);
            border-radius: 999px;
        }}

        .header {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 32px;
        }}

        .dot {{
            position: relative;
            width: 10px; height: 10px;
            border-radius: 50%;
            background: var(--accent);
            box-shadow: 0 0 8px var(--accent-glow);
        }}
        .dot::after {{
            content: '';
            position: absolute;
            inset: 0;
            border-radius: 50%;
            background: var(--accent);
            animation: pulse-ring 2s ease-out infinite;
        }}

        h1 {{
            font-family: 'Syne', sans-serif;
            font-size: 18px;
            font-weight: 800;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            color: var(--text);
        }}

        .field-group {{
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-bottom: 16px;
        }}

        .field {{
            display: flex;
            flex-direction: column;
            gap: 6px;
            animation: fadeUp 0.5s cubic-bezier(0.22, 1, 0.36, 1) both;
        }}
        .field:nth-child(1) {{ animation-delay: 0.05s; }}
        .field:nth-child(2) {{ animation-delay: 0.10s; }}

        label {{
            font-size: 10px;
            font-weight: 500;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: var(--muted);
        }}

        input[type="text"], input:not([type]) {{
            background: var(--bg);
            border: 1px solid var(--border);
            border-radius: 10px;
            color: var(--text);
            font-family: 'DM Mono', monospace;
            font-size: 16px;
            padding: 12px 14px;
            width: 100%;
            transition: border-color 0.2s, box-shadow 0.2s;
            outline: none;
        }}
        input:focus {{
            border-color: var(--accent);
            box-shadow: 0 0 0 3px var(--accent-glow);
        }}
        input::placeholder {{ color: var(--muted); }}

        /* Operator selector as segmented control */
        .op-row {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 6px;
            margin-bottom: 20px;
            animation: fadeUp 0.5s 0.15s cubic-bezier(0.22,1,0.36,1) both;
        }}

        .op-radio {{ display: none; }}

        .op-label {{
            display: flex;
            align-items: center;
            justify-content: center;
            height: 42px;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: var(--bg);
            color: var(--muted);
            font-family: 'Syne', sans-serif;
            font-size: 18px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.18s;
            user-select: none;
        }}
        .op-label:hover {{
            border-color: var(--accent);
            color: var(--accent-light);
        }}
        .op-radio:checked + .op-label {{
            background: var(--accent);
            border-color: var(--accent);
            color: #fff;
            box-shadow: 0 0 16px var(--accent-glow);
        }}

        button[type="submit"] {{
            width: 100%;
            padding: 14px;
            background: var(--accent);
            border: none;
            border-radius: 10px;
            color: #fff;
            font-family: 'Syne', sans-serif;
            font-size: 14px;
            font-weight: 800;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            cursor: pointer;
            position: relative;
            overflow: hidden;
            transition: transform 0.15s, box-shadow 0.15s;
            animation: fadeUp 0.5s 0.2s cubic-bezier(0.22,1,0.36,1) both;
        }}
        button[type="submit"]:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 24px var(--accent-glow);
        }}
        button[type="submit"]:active {{
            transform: translateY(0);
        }}
        /* Shimmer sweep on hover */
        button[type="submit"]::after {{
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(105deg, transparent 30%, rgba(255,255,255,0.18) 50%, transparent 70%);
            background-size: 200% 100%;
            opacity: 0;
            transition: opacity 0.2s;
        }}
        button[type="submit"]:hover::after {{
            opacity: 1;
            animation: shimmer 0.7s linear;
        }}

        /* Result panel */
        .result-box {{
            margin-top: 20px;
            border-radius: 12px;
            border: 1px solid rgba(52,211,153,0.2);
            background: rgba(52,211,153,0.04);
            padding: 16px 18px;
            animation: slide-in 0.35s cubic-bezier(0.22,1,0.36,1) both;
        }}

        .result-label {{
            font-size: 10px;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: rgba(52,211,153,0.6);
            margin-bottom: 6px;
        }}

        .result-value {{
            font-family: 'Syne', sans-serif;
            font-size: 28px;
            font-weight: 800;
            color: var(--result);
            text-shadow: 0 0 20px var(--result-glow);
            word-break: break-all;
        }}

        .result-value.error {{
            font-size: 16px;
            color: #f87171;
            text-shadow: none;
        }}

        /* Cursor blink on result */
        .result-value::after {{
            content: '▮';
            font-size: 0.7em;
            margin-left: 4px;
            animation: blink 1s step-end infinite;
            color: var(--result);
        }}
        .result-value.error::after {{
            color: #f87171;
        }}

        /* Equation line */
        .equation {{
            font-size: 11px;
            color: var(--muted);
            margin-bottom: 4px;
            font-family: 'DM Mono', monospace;
        }}
    </style>
</head>
<body>
    <div class="card">
        <div class="header">
            <div class="dot"></div>
            <h1>Calculator</h1>
        </div>

        <form method="get" autocomplete="off">
            <div class="field-group">
                <div class="field">
                    <label for="a">First number</label>
                    <input id="a" name="a" placeholder="0" value="{a}">
                </div>
                <div class="field">
                    <label for="b">Second number</label>
                    <input id="b" name="b" placeholder="0" value="{b}">
                </div>
            </div>

            <div class="op-row">
                <input class="op-radio" type="radio" name="op" id="op-add" value="add" {"checked" if op=="add" else ""}>
                <label class="op-label" for="op-add">+</label>

                <input class="op-radio" type="radio" name="op" id="op-sub" value="sub" {"checked" if op=="sub" else ""}>
                <label class="op-label" for="op-sub">−</label>

                <input class="op-radio" type="radio" name="op" id="op-mul" value="mul" {"checked" if op=="mul" else ""}>
                <label class="op-label" for="op-mul">×</label>

                <input class="op-radio" type="radio" name="op" id="op-div" value="div" {"checked" if op=="div" else ""}>
                <label class="op-label" for="op-div">÷</label>
            </div>

            <button type="submit">Calculate</button>
        </form>

        {"" if not has_result else f'''
        <div class="result-box">
            <div class="equation">{a} {op_symbols.get(op, op)} {b} =</div>
            <div class="result-label">Result</div>
            <div class="result-value{"" if not isinstance(result, str) or result not in ("Invalid input", "Cannot divide by zero") else " error"}">{result_display}</div>
        </div>
        '''}
    </div>
</body>
</html>"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)