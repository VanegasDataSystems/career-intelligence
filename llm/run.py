import json
from llm.model import generate_explanation


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def run():
    print("=== LLM STAGE START ===")

    jobs_list = load_json("search_results_jobs.json")
    skills_list = load_json("search_results_skills.json")

    if not jobs_list or not skills_list:
        raise ValueError("Search result files are empty.")

    latest_jobs = jobs_list[-1]
    latest_skills = skills_list[-1]

    search_id = latest_jobs["search_id"]
    role_query = latest_jobs["role_query"]
    location = latest_jobs["location_filter"]

    print(f"[DEBUG] Processing search_id: {search_id}")
    print(f"[DEBUG] Role query: {role_query}")
    print(f"[DEBUG] Location filter: {location}")

    # Validate search_id match
    if latest_jobs["search_id"] != latest_skills["search_id"]:
        raise ValueError(
            f"Mismatch detected: jobs search_id={latest_jobs['search_id']} "
            f"!= skills search_id={latest_skills['search_id']}"
        )

    print("[DEBUG] Search ID validation passed")
    print("[DEBUG] Entering LLM stage")

    # --- Build explanation ---
    explanation = generate_explanation(
        role_query,
        latest_skills["skills"],
        latest_jobs["jobs"]
    )

    print("[DEBUG] LLM OUTPUT:")
    print(explanation)
    print("=== END LLM OUTPUT ===")

    final_output = {
        "search_id": search_id,
        "role_query": role_query,
        "location_filter": location,
        "jobs": latest_jobs["jobs"],
        "skills": latest_skills["skills"],
        "ai_summary": explanation
    }

    with open("final_results.json", "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=2)

    print("[DEBUG] final_results.json written successfully")
    print("=== LLM STAGE COMPLETE ===")


if __name__ == "__main__":
    run()
