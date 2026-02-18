from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_PATH = "models/tiny-llama"

_tokenizer = None
_model = None


def load_model():
    global _tokenizer, _model

    if _tokenizer is None or _model is None:
        _tokenizer = AutoTokenizer.from_pretrained(
            MODEL_PATH,
            local_files_only=True
        )
        _model = AutoModelForCausalLM.from_pretrained(
            MODEL_PATH,
            local_files_only=True
        )

    return _tokenizer, _model


def generate_explanation(query, skills, jobs):
    tokenizer, model = load_model()

    top_skills = skills[:10]
    job_titles = [job["title"] for job in jobs[:3]]

    prompt = f"""
You are analyzing structured job market results.

Role:
{query}

Top Ranked Skills (with relevance scores):
{top_skills}

Sample Retrieved Job Titles:
{job_titles}

Based ONLY on the skills and job titles above:

- Summarize what the data suggests about current demand for this role.
- Describe visible skill trends.
- Do NOT introduce external statistics, projections, or market numbers.
- Do NOT invent new skills.
- Do NOT reference information outside the provided data.

Write one concise professional paragraph.
Output only the paragraph text.
"""

    # ---- DEBUG INPUT ----
    print("=== LLM INPUT PROMPT ===")
    print(prompt)
    print("=== END LLM INPUT ===")

    inputs = tokenizer(prompt, return_tensors="pt")
    input_len = inputs["input_ids"].shape[1]

    outputs = model.generate(
        **inputs,
        max_new_tokens=150,
        do_sample=False
    )

    generated_tokens = outputs[0][input_len:]

    explanation = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    ).strip()

    return explanation
