import json
from collections import defaultdict


def aggregate_skills_for_jobs(jobs, job_skills_map):
    skill_scores = defaultdict(float)

    for job in jobs:
        job_id = int(job["job_id"])
        score = float(job["score"])

        for skill in job_skills_map.get(job_id, []):
            skill_scores[skill] += score

    ranked = sorted(
        skill_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        {"name": skill, "score": round(score, 4)}
        for skill, score in ranked[:10]
    ]


def main():
    JOB_RESULTS_FILE = "search_results_jobs.json"
    JOBS_WITH_SKILLS_FILE = "jobs_cleaned_with_skills.json"
    OUTPUT_FILE = "search_results_skills.json"

    # Load all search runs
    with open(JOB_RESULTS_FILE, "r", encoding="utf-8") as f:
        searches = json.load(f)

    if not searches:
        print("No searches found.")
        return

    # Load jobs with skills
    with open(JOBS_WITH_SKILLS_FILE, "r", encoding="utf-8") as f:
        jobs_data = json.load(f)

    # Build job_id -> skills map
    job_skills_map = {
        int(job["job_id"]): job.get("skills", [])
        for job in jobs_data
    }

    all_skill_results = []

    for search in searches:
        skills = aggregate_skills_for_jobs(
            search["jobs"],
            job_skills_map
        )

        all_skill_results.append({
            "search_id": search.get("search_id"),
            "role_query": search.get("role_query"),
            "location_filter": search.get("location_filter", ""),
            "skills": skills
        })

    # Write output (overwrite)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_skill_results, f, indent=2)

    print(f"Generated skills for {len(all_skill_results)} searches.")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
