# InsightHound — Detailed Working

This document provides an in-depth explanation of how every component of InsightHound works, including data flows, API interactions, AI pipelines, and service communication.

---

## Table of Contents

- [1. System Architecture](#1-system-architecture)
- [2. Frontend (Next.js)](#2-frontend-nextjs)
- [3. Backend — Node.js/Express](#3-backend--nodejsexpress)
- [4. AI Backend — FastAPI](#4-ai-backend--fastapi)
- [5. Mobile App — Expo/React Native](#5-mobile-app--exporeact-native)
- [6. Database Layer](#6-database-layer)
- [7. AI & LLM Pipelines](#7-ai--llm-pipelines)
- [8. External API Integrations](#8-external-api-integrations)
- [9. End-to-End User Flows](#9-end-to-end-user-flows)

---

## 1. System Architecture

- The **Frontend** communicates with the **Node.js Backend** for authentication, company CRUD, and trends data.
- The **Frontend** communicates with the **FastAPI AI Backend** for all AI-powered features (chat, analysis, outreach, etc.).
- Both backends share the same **MongoDB** database.
- The **Mobile App** communicates with the same backends for feedback collection.

---

## 2. Frontend (Next.js)

### Technology

- **Next.js 14** with Turbopack (`next dev --turbo`)
- **TypeScript** for type safety
- **Tailwind CSS** + **shadcn/ui** (Radix UI primitives) for the component library
- **Prisma Client** for direct MongoDB access from Next.js API routes
- **React-Leaflet** for the interactive heatmap
- **Recharts** for data visualization (charts, graphs)
- **React Three Fiber / Spline** for 3D elements on the landing page
- **Framer Motion** for animations
- **TanStack React Query** for data fetching and caching
- **Nodemailer** for sending bulk emails from the Next.js API route

### Key Routes

| Route | Purpose |
|---|---|
| `/` | Landing page with 3D visuals |
| `/auth` | Login / Signup |
| `/onboarding` | Company onboarding (PDF upload + form) |
| `/dashboard` | Main dashboard hub |
| `/dashboard/competitor-mapping` | Crunchbase-powered competitor analysis |
| `/dashboard/audience-insights` | AI-generated audience insights |
| `/dashboard/audience-segments` | Market segmentation with TAM metrics |
| `/dashboard/audience-outreach` | LinkedIn and email outreach tools |
| `/dashboard/market-intelligence` | Market research questionnaires |
| `/dashboard/product-comparison` | Product vs. competitor comparison |
| `/dashboard/hound-board` | AI-generated Kanban roadmap |
| `/dashboard/feedback-hub` | Typeform-integrated feedback collection |
| `/dashboard/strategic-insights` | AI-generated strategic insights |
| `/dashboard/reports` | Comprehensive report generation |
| `/dashboard/bulk-mail` | Bulk email sending |
| `/chat` | LangGraph AI chat assistant |
| `/chat/[id]` | Specific conversation thread |
| `/report/[id]` | View generated report |

### Data Fetching

- Uses two utility functions (`fetch-api.ts` and `fetch-api-server.ts`) that wrap `fetch` calls to the Node.js and FastAPI backends.
- The `NEXT_PUBLIC_BACKEND_URL` targets the Node.js backend.
- The `NEXT_PUBLIC_FLASK_URL` targets the FastAPI AI backend.
- Authentication tokens are stored and managed via custom hooks (`use-auth.tsx`, `use-self.ts`).

---

## 3. Backend — Node.js/Express

### Technology

- **Express.js** (ES modules)
- **Prisma ORM** with MongoDB provider
- **JWT** authentication with **bcrypt** password hashing
- **Google Trends API** for trend data

### Database Schema (Prisma)

model user {
  id        String   @id @default(auto()) @map("_id") @db.ObjectId
  email     String   @unique
  password  String
  props     String?
  company   company? @relation(fields: [companyId], references: [id])
  companyId String?  @db.ObjectId @unique
  createdAt DateTime @default(now())
}

model company {
  id          String   @id @default(auto()) @map("_id") @db.ObjectId
  name        String
  description String
  vision      String?
  mission     String?
  valuation   Int?
  linkedinUrl String?
  domain      String?
  props       String?
  user        user?
  createdAt   DateTime @default(now())
}

### API Endpoints

| Method | Route | Description |
|---|---|---|
| POST | `/user/signup` | Register a new user (hashes password, returns JWT) |
| POST | `/user/login` | Authenticate user (validates password, returns JWT) |
| GET | `/user/getMe` | Get current user profile (requires JWT) |
| PATCH | `/user/:id` | Update user |
| DELETE | `/user/:id` | Delete user |
| GET | `/company/` | List all companies |
| POST | `/company/` | Create a company (linked to authenticated user) |
| PUT | `/company/:id` | Update a company |
| DELETE | `/company/:id` | Delete a company |
| GET | `/api/trends` | Fetch Google Trends interest-by-region data for a keyword |

### Authentication Flow

1. User signs up → password hashed with bcrypt → stored in MongoDB via Prisma.
2. JWT token generated with user ID and email, expires in 1 day.
3. Token sent back to client; used in `Authorization` header for subsequent requests.
4. `authMiddleware` verifies the JWT and attaches `req.user` to protected routes.

---

## 4. AI Backend — FastAPI

### Technology

- **FastAPI** with CORS middleware (allows all origins)
- **LangChain** for LLM chain composition
- **LangGraph** for stateful AI agent with tool calling
- **OpenAI GPT-4o** (primary) and **GPT-4o-mini** (chat agent)
- **PyMongo** for direct MongoDB access
- **Pydantic** models for request/response validation

### Architecture Pattern

The AI backend follows a clean layered architecture:

endpoints/  →  API route handlers (FastAPI routers)
services/   →  Business logic and AI chain invocations
constants/  →  Prompt templates, configs, shared instances
models/     →  Pydantic data models
repository/ →  MongoDB client wrapper (CRUD operations)

### API Endpoints (FastAPI Routers)

| Router | Prefix/Route | Description |
|---|---|---|
| `agent` | `POST /chat` | LangGraph AI chat with tool calling |
| `keywords` | Keywords generation | AI-generated keywords from company profile |
| `onboard` | Company onboarding | PDF parsing + AI extraction of company data |
| `crunchbase` | Competitor data | Fetch company data from Crunchbase via Apify |
| `youtube` | YouTube search | Scrape YouTube for relevant videos |
| `marketresearch` | Market research | Generate questionnaires for market research |
| `marketsegment` | Market segmentation | Generate TAM/market segment analysis |
| `outreach` | LinkedIn outreach | Generate messages, send via Unipile |
| `trends` | Heatmap data | Google Trends heatmap via SerpAPI |
| `email` | Email generation | AI-generated cold email templates |
| `typeform` | Feedback forms | Integration with Typeform API |
| `kanban` | Kanban board | AI-generated task roadmaps |
| `product` | Product comparison | AI product comparison analysis |
| `report` | Reports | Generate comprehensive HTML reports |
| `news` | News articles | Fetch news via NewsAPI |
| `vote` | Voting | User voting on feedback |
| `aggregate` | Data aggregation | Aggregate company insights |
| `rivals` | Rival analysis | Fetch and compare rival companies |
| `summary` | Summaries | AI-generated summaries |
| `mongodb` | Database operations | Direct MongoDB read/write operations |

### LangGraph AI Chat Agent (Detailed)

The chat agent (`services/agent.py`) is the core conversational interface:

1. **State Definition**: Uses a `TypedDict` with `messages` (conversation history) and `user_id`.
2. **Graph Construction**:
   - `chatbot` node: Fetches user data and company details from MongoDB, prepends them to the conversation, then invokes GPT-4o-mini with tool bindings.
   - `tools` node: A `ToolNode` wrapping the Tavily web search tool.
   - Conditional edge: After the chatbot responds, `tools_condition` checks if the LLM requested a tool call. If yes, routes to the tools node; otherwise, ends.
   - After tool execution, routes back to the chatbot node for the final response.
3. **Memory**: Uses `MemorySaver` checkpointer for conversation persistence across turns.
4. **Available Tools**: The agent has access to multiple tools defined as LangChain `@tool` functions:
   - `TavilySearchResults` — Web search for real-time data
   - `generate_heatmap` — Google Trends geographic data
   - `generate_keywords` — AI keyword generation
   - `generate_segmentation` — Market segmentation
   - `generate_kanban` — Roadmap generation
   - `generate_product` — Product comparison
   - `generate_mail` — Email template generation
   - `generate_linkedin` — LinkedIn message generation
   - `generate_rivals` — Competitor discovery via LinkedIn
   - `generate_news` — News article fetching

### LLM Chain Pattern

Most AI services follow this pattern:

chain = PROMPT_TEMPLATE | openai_llm | OutputFixingParser.from_llm(
    parser=JsonOutputParser(pydantic_object=ResponseModel),
    llm=openai_llm
)
result = chain.invoke({"param1": value1, "param2": value2})

- A **prompt template** defines the system/human message structure.
- The **LLM** (GPT-4o) generates a response.
- The **OutputFixingParser** ensures the response conforms to the Pydantic model schema. If the initial output doesn't parse correctly, it uses the LLM to fix the format.

---

## 5. Mobile App — Expo/React Native

### Technology

- **Expo SDK 52** with **Expo Router** for file-based navigation
- **React Native** 0.76 with **NativeWind** (Tailwind for React Native)
- **React Hook Form** + **Zod** for form validation
- **AsyncStorage** for local data persistence
- **WebView** for embedded web content

### Purpose

The mobile app serves as a companion for feedback collection:
- Users can browse startups and submit ratings/reviews.
- Integrates with the same backend APIs as the web frontend.
- Provides a reward system for user participation.

---

## 6. Database Layer

### MongoDB (Shared)

All services connect to the same MongoDB database:

- **Node.js Backend**: Accesses via **Prisma ORM** with the MongoDB provider. Manages `user` and `company` collections with relational references.
- **FastAPI AI Backend**: Accesses via **PyMongo** through a custom `MongoDBClient` wrapper class (`repository/repository.py`). This client provides:
  - `create(collection, model)` — Insert a document
  - `read(collection, id)` — Find by ObjectId
  - `read_by_key_value(collection, key, value)` — Query by field
  - `update(collection, id, data)` — Update a document
  - `delete(collection, id)` — Delete a document
  - `read_all(collection)` — Fetch all documents

### Key Collections

| Collection | Used By | Description |
|---|---|---|
| `user` | Both backends | User accounts with hashed passwords |
| `company` | Both backends | Company profiles with onboarding data |
| `rivals` | FastAPI | Competitor company data from Crunchbase |
| `conversations` | FastAPI | AI chat conversation history |

---

## 7. AI & LLM Pipelines

### Onboarding Pipeline

User uploads PDF → PyPDFLoader extracts text → Text splitter chunks it →
ONBOARD_PROMPT + GPT-4o → JsonOutputParser → Company model →
Stored in MongoDB

The onboarding flow allows users to upload a pitch deck or business plan. The AI extracts structured company data (name, vision, mission, description, domain) from the document.

### Keyword Generation Pipeline

Company profile (vision, mission, description, domain) →
KEYWORD_PROMPT + GPT-4o → JsonOutputParser → List of keywords

Generated keywords are used for Google Trends analysis and heatmap generation.

### Market Segmentation Pipeline

Company profile → MARKETSEGMENT_PROMPT + GPT-4o → JsonOutputParser →
List of segments with: unit_size, urgency, benefit, potential_revenue,
market_share, growth_rate, competition_index, CAC, profit_margin

### Competitor Analysis Pipeline

Company name → Apify Crunchbase scraper → Company financial highlights,
similar orgs → Store in MongoDB → Background tasks fetch rival data →
Rival companies stored in "rivals" collection

### LinkedIn Outreach Pipeline

User selects outreach → Unipile API fetches LinkedIn company profile →
BeautifulSoup scrapes company webpage → GPT-4o generates persona →
GPT-4o generates personalized message → Unipile API sends message

### Product Comparison Pipeline

Company name + Product name → PRODUCT_TEMPLATE + GPT-4o →
JsonOutputParser → Product comparison data (pricing, features, reviews)
for the product and 3 rival products

### Report Generation Pipeline

Company details + Product comparison + Market segments +
Market research + Kanban board → REPORT_TEMPLATE + GPT-4o →
JsonOutputParser → HTML report

### Heatmap Data Pipeline

Keyword + Geographic code → SerpAPI (Google Trends engine) →
Interest by region data with coordinates → Frontend renders
on Leaflet heatmap

### News Aggregation Pipeline

Company name + Topic → NewsAPI query (last 30 days) →
Sorted by publish date → Returned to frontend

---

## 8. External API Integrations

| API | Purpose | Used In |
|---|---|---|
| **OpenAI** (GPT-4o, GPT-4o-mini) | All AI text generation, analysis, and chat | `services/*.py` |
| **Tavily** | Real-time web search for the AI chat agent | `services/agent.py` |
| **SerpAPI** | Google Trends geographic interest data for heatmaps | `services/trends.py` |
| **Apify** (Crunchbase scraper) | Competitor company data scraping from Crunchbase | `services/crunchbase.py` |
| **Unipile** | LinkedIn profile access, company search, and messaging | `services/outreach.py` |
| **NewsAPI** | Fetching recent news articles by topic | `services/news.py` |
| **Typeform** | Creating and managing feedback survey forms | `services/typeform.py` |
| **Google Trends API** (npm) | Interest-by-region keyword trends | `backend/src/routes/api.js` |

---

## 9. End-to-End User Flows

### Flow 1: New User Onboarding

1. User visits `/auth` and signs up with email and password.
2. Node.js backend hashes the password, creates the user in MongoDB, and returns a JWT.
3. User is redirected to `/onboarding`.
4. User uploads a pitch deck PDF or fills in company details manually.
5. FastAPI backend parses the PDF with PyPDFLoader, extracts text, and uses GPT-4o to generate structured company data.
6. Company is created in MongoDB and linked to the user.
7. User is redirected to the main dashboard.

### Flow 2: Competitor Analysis

1. User navigates to `/dashboard/competitor-mapping`.
2. Frontend calls the FastAPI Crunchbase endpoint with the user ID.
3. FastAPI fetches the user's company from MongoDB, then queries Apify's Crunchbase scraper.
4. Crunchbase returns company data including financial highlights and similar organizations.
5. Data is stored in MongoDB under the company's `props` field.
6. Similar organizations are processed in background tasks — each rival's data is fetched and stored in the `rivals` collection.
7. Frontend renders the competitor comparison charts and tables.

### Flow 3: AI Chat Conversation

1. User navigates to `/chat` and types a message.
2. Frontend sends a POST request to `FastAPI /chat` with the message and user ID.
3. LangGraph agent:
   a. Fetches user data and company details from MongoDB.
   b. Constructs a message list with the system prompt, conversation history, and company context.
   c. Invokes GPT-4o-mini with Tavily search as an available tool.
   d. If the LLM decides to use web search, the tool node executes the Tavily query and returns results.
   e. The chatbot node processes tool results and generates the final response.
4. Response is returned to the frontend and rendered in the chat interface.

### Flow 4: Market Heatmap

1. User navigates to the dashboard with keywords generated during onboarding.
2. Frontend sends keywords and a geographic code to the FastAPI trends endpoint.
3. FastAPI calls SerpAPI with the `google_trends` engine and `GEO_MAP_0` data type.
4. SerpAPI returns interest-by-region data with coordinates, location names, and interest values.
5. Frontend renders the data on a Leaflet map using the heatmap layer plugin.

### Flow 5: Report Generation

1. User navigates to `/dashboard/reports`.
2. Frontend aggregates data from multiple sources: company details, product comparisons, market segments, research questionnaires, and the Kanban board.
3. All data is sent to the FastAPI report endpoint.
4. GPT-4o processes the combined data through the report template prompt.
5. An HTML report is generated and returned to the frontend.
6. The report can be viewed at `/report/[id]`.
