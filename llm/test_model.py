from llm.model import load_model, generate

def main():
    tokenizer, model = load_model()

    prompt = """<|system|>
You are a backend API.
Return ONLY valid JSON.

<|user|>
Return exactly:
{"status": "ok"}

<|assistant|>
"""

    output = generate(tokenizer, model, prompt)

    print("RAW OUTPUT:")
    print(output)

if __name__ == "__main__":
    main()
