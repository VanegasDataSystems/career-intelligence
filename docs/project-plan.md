# Project Plan

## Career Intelligence  
**Course:** CS467_400_W2026  
**Team Members:** Daniel Lai, Fernando Vanegas, Giang Le

---

## Change Log

Who did what and when. Helps to have an audit trail.

| Change | Author | Date |
|------|--------|------|
|      |        |      |

---

## Introduction

Figuring out what skills employers want is more confusing than it should be. Job postings are usually very long and use different words for the same jobs. Sometimes it feels like you need experience just to understand the job description. Searching by keywords helps a little, but it still misses a lot.

This project tries to make job postings easier to deal with. Instead of using expensive tools, it uses open-source software and runs locally. It also looks at jobs by skills and general meaning, not just exact keywords, which should make searching less annoying.

The goal of this project is not to build some perfect AI system. The goal is to organize messy job data and make it more useful. If things go well, users can spend less time being confused by job postings and more time learning skills that actually matter.

---

## Problem Statement

### Context
Many people use job websites to look for jobs and see what skills employers want. Job postings often have long descriptions and use different words for similar jobs. Because of this, it is hard to understand which skills are really important or how different jobs are connected.

### Issue
The main problem is that job information is messy and hard to understand. Job descriptions are not well organized and are spread across many websites. Searching by keywords does not always work well because similar jobs may use different words. This makes it hard for job seekers to know which skills they should focus on learning.

### Relevance
This problem affects students, new graduates, and people who want to change careers. These users want to learn useful skills but do not know where to start. Many of them do not have access to paid tools that analyze job market data, so they rely on searching by themselves and guessing.

### Objective
The goal of this project is to build a simple system that collects job postings and organizes the data. The system will let users search for jobs by skills or general ideas instead of exact keywords. It will also help users compare job requirements with their current skills and suggest what they can learn next. By using open-source and low-cost tools, the project aims to make job information easier to understand and more useful.

---

## Requirements

This project requires building a system that collects job postings and organizes the data so it is easier to use. The system should allow users to search jobs by skills or general ideas instead of only using keywords, and it should store job information in a structured way.

The project also includes using basic AI tools to compare job requirements with a user’s skills and suggest what they could learn next. All tools used should be low-cost or open-source, and the system should show the full process from data collection to simple recommendations.

---

## Major Requirements / Features

The main requirements of the system are:

- Automatically collect job postings from online job boards  
- Store job data locally so it can be reused later  
- Clean and organize messy job descriptions  
- Extract useful information such as skills and salary ranges if available  
- Allow searching jobs by skills or general ideas instead of exact keywords  
- Use vector search to find similar job postings  
- Use an AI model to give simple learning or skill suggestions  
- Provide a basic user interface for users to interact with the system  
- Use open-source and low-cost tools  
- Keep the system mostly written in Python  

---

## Design / Architecture

The system is designed as a simple pipeline. Each part of the system has a clear role, and data moves from one step to the next.

The main parts of the system are:

- Data Extraction  
- Data Storage  
- Data Transformation  
- Vector Search  
- AI and Recommendations  
- User Interface  

### How Each Part Works

**Data Extraction**  
Collects job postings from public job websites using Playwright and dlt.

**Data Storage**  
Stores both raw and cleaned job data locally using DuckDB.

**Data Transformation**  
Cleans and organizes job data and extracts useful fields such as skills and salary ranges.

**Vector Search**  
Converts job descriptions into embeddings and allows searching jobs by meaning.

**AI and Recommendations**  
Uses an AI model to answer user questions and suggest skills to learn.

**User Interface**  
Provides a simple way for users to search jobs and view results.

---

## Main Technologies Used and Observations

- **Python** – main programming language  
  - Pros: easy to learn, strong community support  
  - Cons: not the fastest  

- **Playwright** – crawl job postings  
  - Pros: works with JavaScript-heavy sites  
  - Cons: setup can be tricky  

- **dlt** – load crawled data  
  - Pros: simplifies data handling  
  - Cons: learning curve  

- **DuckDB** – local database  
  - Pros: simple, no server required  
  - Cons: limited scalability  

- **SQLMesh** – data transformation  
  - Pros: structured way to transform data  
  - Cons: takes time to learn  

- **DuckDB vss** – vector storage and search  
  - Pros: supports semantic search  
  - Cons: newer tool  

- **Ollama and LiteLLM** – AI models  
  - Pros: low cost  
  - Cons: models may be less advanced  

- **Python UI framework**  
  - Pros: stays in Python  
  - Cons: limited design options  

- **GitHub** – version control  
  - Pros: industry standard  
  - Cons: can be confusing at first  

---

## Important Resources

- Public job boards (Indeed, LinkedIn)
- Online documentation for Playwright, DuckDB, SQLMesh, dlt
- Open-source AI models
- Pre-trained embedding models
- GitHub for collaboration
- Personal computers
- Internet access

---

## Development Plan

### Weeks 3–4: Setup and Early Work (Progress Report 1)

**Giang — ~20 hours**
- Set up project documentation  
- Build basic scraper  
- Save data to DuckDB  

**Dependencies / Risks**
- Playwright setup → scraper runs  
- Scraper fails → delays others  

**Daniel — ~20 hours**
- Review scraped data  
- Decide useful job fields  
- Plan data cleaning  

**Dependencies / Risks**
- Needs data from Giang  

**Fernando — ~20 hours**
- Choose UI framework  
- Create basic UI layout  

**Dependencies / Risks**
- Backend not ready → mock data  

---

### Weeks 5–7: Data and Search (Progress Report 2)

**Giang — ~30 hours**
- Generate embeddings  
- Set up vector search  

**Daniel — ~30 hours**
- Clean job descriptions  
- Extract skills  

**Fernando — ~30 hours**
- Build job search UI  
- Connect UI to backend  

---

### Weeks 8–9: AI and Improvements (Progress Report 3)

**Giang — ~20 hours**
- Integrate AI model  
- Build RAG flow  

**Daniel — ~20 hours**
- Validate data  
- Improve extraction  

**Fernando — ~20 hours**
- Display AI results  
- Improve UI usability  

---

### Weeks 10–12: Final Work

**All Team Members — ~30 hours each**
- Test system  
- Fix bugs  
- Write documentation  
- Prepare demo  

---

## Conclusion

Overall, the project aims to turn messy job data into something more useful and easier to understand.

Plan is done. Code is coming. Hopefully.
