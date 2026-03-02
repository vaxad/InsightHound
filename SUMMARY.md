# InsightHound — Project Summary

## What is InsightHound?

**InsightHound** is an AI-powered business intelligence platform designed to help startups solve critical business challenges. It provides data-driven insights, competitor analysis, market research, and actionable strategies — all through a unified dashboard and conversational AI interface.

---

## Core Features

### 1. Customer Market Evaluation
- Interactive **world heatmap** showing customer density by region.
- Uses **Google Trends** (via SerpAPI) and **Pytrends** to analyze search volume for startup-relevant keywords.
- Helps startups identify where their potential customers are concentrated.

### 2. Competitor Analysis
- Integrates with **Crunchbase** (via Apify scraper) to fetch competitor data: funding, revenue, reviews, and USPs.
- **LinkedIn company profiling** (via Unipile API) to enrich competitor data with employee counts, descriptions, and activity.
- Identifies similar companies and generates rival comparison data automatically.

### 3. AI-Driven Cold Outreach
- Generates **personalized cold emails** using OpenAI GPT-4o based on company vision, mission, and domain.
- **LinkedIn outreach automation** — generates messages, fetches profiles, and can send messages via the Unipile API.
- Supports **bulk email sending** through Nodemailer integration.

### 4. LangGraph AI Chat Assistant
- Conversational AI assistant built with **LangGraph** and **LangChain**.
- Uses **GPT-4o-mini** with **Tavily web search** as a tool for real-time market insights.
- Context-aware: pulls the user's company details from MongoDB to personalize responses.
- Maintains conversation memory across sessions.

### 5. Market Segmentation & Analysis
- AI-generated **market segments** with metrics: TAM, unit size, growth rate, competition index, and profit margins.
- **Market research questionnaires** generated automatically from company profile data.

### 6. Product Comparison
- Generates detailed **product vs. rival product** comparisons including pricing, features, and reviews.

### 7. Strategic Insights & Kanban Board
- AI-generated **strategic insights** from aggregated company data.
- Auto-generated **Kanban board** (task roadmap) based on company vision and mission.

### 8. Reports
- Generates comprehensive **HTML reports** combining company details, product comparisons, market segments, research, and roadmaps.

### 9. Feedback Collection (Mobile App)
- **React Native / Expo** mobile app for collecting user feedback.
- Integrates with **Typeform** for structured survey forms.
- Users earn rewards for rating startups.

### 10. News & YouTube Aggregation
- Fetches relevant **news articles** via NewsAPI.
- Scrapes **YouTube search results** for related video content.

---

## Tech Stack

| Layer | Technologies |
|---|---|
| **Frontend** | Next.js 14, React 18, TypeScript, Tailwind CSS, shadcn/ui, Radix UI, Recharts, React-Leaflet, Framer Motion, Three.js |
| **Backend (Node.js)** | Express.js, Prisma ORM, MongoDB, JWT authentication, bcrypt, Google Trends API |
| **AI Backend (Python)** | FastAPI, LangChain, LangGraph, OpenAI GPT-4o/4o-mini, Tavily, SerpAPI, BeautifulSoup, Apify, Unipile |
| **Mobile App** | React Native, Expo, NativeWind, Expo Router |
| **Database** | MongoDB (shared across all services via Prisma and PyMongo) |
| **External APIs** | OpenAI, Tavily, SerpAPI, Apify (Crunchbase), Unipile (LinkedIn), NewsAPI, Typeform |

---

## Architecture Overview

InsightHound follows a **multi-service architecture** with four independently running components:

1. **Frontend (Next.js)** — The main web dashboard. Communicates with both backends via REST APIs.
2. **Backend (Node.js/Express)** — Handles user authentication (JWT), company CRUD, and Google Trends data. Uses Prisma ORM with MongoDB.
3. **AI Backend (FastAPI)** — The intelligence engine. Handles all AI-powered features: chat agent, keyword generation, competitor analysis, market segmentation, outreach, reports, and more. Uses LangChain/LangGraph with OpenAI models.
4. **Mobile App (Expo/React Native)** — A companion app for feedback collection and user surveys.

All services share the same **MongoDB database**, accessed via Prisma (Node.js services) and PyMongo (Python service).

