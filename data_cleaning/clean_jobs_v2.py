import duckdb
import json
import re
import unicodedata
import html
from bs4 import BeautifulSoup
from ftfy import fix_text

# Load canonical skills (once)
with open("skills.json", "r", encoding="utf-8") as f:
    skills_by_category = json.load(f)

AMBIGUOUS_SKILLS = {
    "Go",
    "R",
    "C",
    "Rust",
    "Swift"
}

PROGRAMMING_CONTEXT = [
    "programming",
    "language",
    "developer",
    "engineer",
    "backend",
    "software",
    "experience with",
    "written in",
    "using"
]

CANONICAL_SKILLS = {
    skill
    for skills in skills_by_category.values()
    for skill in skills
}

# helper function to clean texts others than description
def clean_text(text):
    if text is None:
        return ""
    text = html.unescape(text)
    text = fix_text(text)
    text = unicodedata.normalize("NFKC", text)
    return text.strip()


# function to clean description
def clean_description(html_text):
    if html_text is None:
        return ""

    # 1. Unescape HTML entities
    text = html.unescape(html_text)

    # 2. Fix encoding
    text = fix_text(text)

    # 3. Strip HTML tags
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text(separator="\n", strip=True)

    # 4. Unicode normalization
    text = unicodedata.normalize("NFKC", text)

    # 5. Boilerplate removal (keep minimal)
    boilerplate_patterns = [
        r"please mention the word.*?$",
        r"this is a beta feature.*?$"
    ]
    for pattern in boilerplate_patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE | re.DOTALL)

    # 6. Whitespace cleanup
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()

def extract_skills(text):
    text_lower = text.lower()
    found = set()

    for skill in CANONICAL_SKILLS:
        skill_lower = skill.lower()

        # Normal skills: direct match
        if skill not in AMBIGUOUS_SKILLS:
            if re.search(rf"\b{re.escape(skill_lower)}\b", text_lower):
                found.add(skill)
            continue

        # Ambiguous skills: require context
        for ctx in PROGRAMMING_CONTEXT:
            pattern = rf"\b{re.escape(skill_lower)}\b.{0,40}\b{ctx}\b|\b{ctx}\b.{0,40}\b{re.escape(skill_lower)}\b"
            if re.search(pattern, text_lower):
                found.add(skill)
                break

    return sorted(found)

def main():
    con = duckdb.connect("fv/remoteok_loader.duckdb")
    con.sql("use job_listings")

    query = """
        SELECT
            id AS job_id,
            position AS title,
            company,
            location,
            description AS description_raw,
            url
        FROM remoteok_jobs
        WHERE description IS NOT NULL
    """
    rows = con.execute(query).fetchall()

    jobs = []

    for job_id, title, company, location, desc_raw, url in rows:
        desc_clean = clean_description(desc_raw)
        skills = extract_skills(desc_clean)

        jobs.append({
            "job_id": job_id,
            "title": clean_text(title),
            "company": clean_text(company),
            "location": clean_text(location),
            "description_clean": desc_clean,
            "skills": skills,
            "url": url
        })

    with open("jobs_cleaned_with_skills.json", "w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(jobs)} jobs to jobs_cleaned_with_skills.json")


if __name__ == "__main__":
    main()
