# Development Plan

This document outlines the planned development work for the project starting from Week 3.  
Work is split across three team members, with roughly equal effort (at least 10 hours per week per person).

---

## Weeks 3–4: Setup and Early Work (Progress Report 1)

### Giang — about 20 hours
- Set up basic project documentation
- Try Playwright and build a simple scraper for one job board
- Save scraped job data into DuckDB

**Dependencies / Risks**
- Playwright setup → scraper runs
- Scraper works → data saved
- If scraping breaks → delays others

---

### Daniel — about 20 hours
- Review scraped job data
- Decide which job fields are useful (title, skills, salary, etc.)
- Think about how the data should be cleaned later

**Dependencies / Risks**
- Needs scraped data from Giang → review
- If data is incomplete → harder planning

---

### Fernando — about 20 hours
- Pick a Python UI framework
- Create a very basic UI layout

**Dependencies / Risks**
- UI choice → affects later UI work
- Backend not ready → use mock data

---

## Weeks 5–7: Data and Search (Progress Report 2)

### Giang — about 30 hours
- Turn job descriptions into embeddings
- Set up vector search using DuckDB vss

**Dependencies / Risks**
- Cleaned job text from Daniel → embeddings
- DuckDB vss setup → search works

---

### Daniel — about 30 hours
- Clean job descriptions
- Extract skills from job text
- Try to make skills more consistent

**Dependencies / Risks**
- Raw job data from Giang → cleaning
- Different job formats → harder parsing

---

### Fernando — about 30 hours
- Build job search pages in the UI
- Connect UI to backend search results

**Dependencies / Risks**
- Vector search from Giang → UI connection
- Backend changes → UI updates needed

---

## Weeks 8–9: AI and Improvements (Progress Report 3)

### Giang — about 20 hours
- Connect a local AI model
- Build a simple RAG flow

**Dependencies / Risks**
- Vector search ready → AI input
- Clean data from Daniel → better answers

---

### Daniel — about 20 hours
- Check cleaned data for errors
- Improve skill extraction results

**Dependencies / Risks**
- Earlier transformations → review
- Feedback from Giang → fixes

---

### Fernando — about 20 hours
- Display AI results in the UI
- Make the UI easier to use

**Dependencies / Risks**
- AI output from Giang → UI display
- Changes in AI responses → UI tweaks

---

## Weeks 10–12: Final Work

### All Team Members — about 30 hours each
- Test the full system
- Fix bugs
- Clean up code
- Write documentation
- Prepare demo

**Dependencies / Risks**
- All parts from Giang, Daniel, and Fernando → testing
- Time limits → skip stretch goals if needed
