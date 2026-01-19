
# Development Plan

This document outlines how project work is divided among the three team members starting from Week 3. The goal is to ensure balanced contributions (at least 10 hours per week per person) while keeping responsibilities clear and avoiding blocking dependencies where possible.

---

## Weeks 3–4: Setup and Initial Implementation

**Giang**
- Set up documentation structure  
- Build a basic Playwright scraper for one job board  
- Store raw scraped job data in DuckDB  

**Daniel**
- Review scraped job data  
- Decide which fields are important for analysis  
- Plan how job data should be cleaned and transformed  

**Fernando**
- Select a Python-based UI framework  
- Set up a basic UI skeleton  

---

## Weeks 5–7: Data Processing and Search

**Giang**
- Generate embeddings from job descriptions  
- Implement vector search using DuckDB vss  

**Daniel**
- Clean job descriptions  
- Extract and normalize technical skills  

**Fernando**
- Build job search UI  
- Connect UI to backend search functionality  

---

## Weeks 8–9: AI Integration and Refinement

**Giang**
- Integrate a local LLM  
- Build a basic retrieval-augmented generation (RAG) pipeline  

**Daniel**
- Validate transformed data  
- Improve skill extraction and data quality  

**Fernando**
- Display AI-generated results in the UI  
- Improve usability and layout  

---

## Weeks 10–12: Finalization

**All Team Members**
- End-to-end testing  
- Bug fixes and cleanup  
- Documentation  
- Demo preparation  

Stretch goals will only be attempted if core functionality is completed early.
