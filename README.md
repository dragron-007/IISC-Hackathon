# Global Article Summarization and Link Analysis Platform

## Table of Contents
- [Introduction](#introduction)
- [Problem Statement](#problem-statement)
- [Solution Overview](#solution-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)

## Introduction
Welcome to the Global Article Summarization and Link Analysis Platform. This platform leverages advanced language processing techniques to filter articles based on user inputs, provide concise, relevant summaries, and suggest related articles. The goal is to help users quickly find and understand the most important information on any given topic.

## Problem Statement
In today's fast-paced world, there is an overwhelming number of articles and updates that impact our lives. Finding the most important articles and extracting meaningful insights can be challenging. Our platform aims to address these challenges by:

- Filtering articles based on user queries.
- Providing customizable summaries.
- Analyzing relationships between articles and suggesting related content.

### Example
**User Input:** India Interim Budget Details for 2024

**Output Expectation:**

**Summarization Points:**
- Finance Minister Nirmala Sitharaman stressed on 5 ‘Disha Nirdashak’ baatein: Social justice as an effective governance model; Focus on the poor, youth, women, and the Annadata (farmers); Focus on infrastructure; Use of technology to improve productivity and High-power committee for challenges arising from demographic challenges.

**Related Articles:**
- *The Hindu* - Interim Budget 2024 Highlights
- *Times of India* - Budget 2024 Live Updates

**Keywords:** "India," "Focus on the poor," "Focus on infrastructure."

**Suggested Articles:**
- Infrastructure development in India in the previous decade
- Government Initiative to uplift the section which is Below Poverty Line in the previous 5 years

## Solution Overview
### Challenge Tasks
- **Language Processing Model:** Capable of filtering articles based on user queries.
- **Article Relationships:** Suggest related articles based on the current article's keywords.
- **Interactive UI:** Allows users to input queries and adjust the summarization length.

### Deliverables
- A robust language processing model for article filtering and summarization.
- Relevant article links related to the topic.
- Interactive UI for user interaction.
- Multi-language support for outputting queries and summaries.

### Evaluation Criteria
- **Effectiveness of Article Filtering:** 30%
- **Quality of Summarization:** 30%
- **Related Articles Suggestion:** 30%
- **User Interface Usability:** 10% Bonus

## Features
- **Interactive User Interface:** Enter a topic and receive summarized articles with relevant links.
- **Customizable Summarization Length:** Adjust the length of the summaries based on your needs.
- **Keyword Extraction and Related Articles Suggestion:** Get keywords from the summarized articles and suggestions for further reading.

## Installation
### Prerequisites
Ensure you have the following libraries installed:
- `streamlit`
- `nltk`
- `bs4`
- `requests`
- `googlesearch-python`
- `scikit-learn`

Install these libraries using pip:
```bash
pip install streamlit nltk beautifulsoup4 requests googlesearch-python scikit-learn
