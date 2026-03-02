# How to Run InsightHound

## Prerequisites

Ensure you have the following installed on your machine:

- **Node.js** (v18 or higher) and **npm**
- **Python** (v3.9 or higher) and **pip**
- **MongoDB** instance (local or cloud, e.g. MongoDB Atlas)
- **Expo CLI** (for the React Native mobile app): `npm install -g expo-cli`

---

## 1. Clone the Repository

```bash
git clone https://github.com/vaxad/InsightHound.git
cd InsightHound
```

---

## 2. Environment Variables

The project requires environment variables configured across multiple services.

### Root `.env` (for the FastAPI AI backend — place inside `aihounds/`)

Copy the example and fill in your values:

```bash
cp .env.example aihounds/.env
```

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | OpenAI API key (GPT-4o is used) |
| `DATABASE_URL` | MongoDB connection string |
| `DATABASE_NAME` | MongoDB database name |
| `APIFY_KEY` | Apify API token (for Crunchbase scraping) |
| `TAVILY_API_KEY` | Tavily API key (for web search in LangGraph agent) |
| `SERPAPI_KEY` | SerpAPI key (for Google Trends heatmap data) |
| `TYPEFORM_API_TOKEN` | Typeform API token (for feedback forms) |
| `UNIPILE_API_KEY` | Unipile API key (for LinkedIn outreach integration) |
| `NEWSAPI` | NewsAPI key (for fetching news articles) |
| `WORKSPACE_ID` | Workspace identifier |

### Frontend `.env`

```bash
cp frontend/.env.example frontend/.env
```

| Variable | Description |
|---|---|
| `DATABASE_URL` | MongoDB connection string (used by Prisma) |
| `NEXT_PUBLIC_BACKEND_URL` | URL of the Node.js backend (default: `http://localhost:5001`) |
| `NEXT_PUBLIC_FLASK_URL` | URL of the FastAPI backend (default: `http://127.0.0.1:8000`) |
| `MAIL_PASSWORD` | App password for the email account used for bulk mail |
| `MAIL_USER` | Email address used for sending bulk mail |

### Backend `.env`

```bash
cp backend/.env.example backend/.env
```

| Variable | Description |
|---|---|
| `DATABASE_URL` | MongoDB connection string (used by Prisma) |
| `PORT` | Port for the Node.js backend (default: `5001`) |

---

## 3. Install Dependencies

### Frontend (Next.js)

```bash
cd frontend
npm install
npx prisma generate
cd ..
```

### Backend (Node.js / Express)

```bash
cd backend
npm install
npx prisma generate
cd ..
```

### AI Backend (Python / FastAPI)

```bash
cd aihounds
pip install -r requirements.txt
cd ..
```

### Mobile App (React Native / Expo)

```bash
cd app
npm install
cd ..
```

---

## 4. Run the Services

You need to run **three backend services** and optionally the **mobile app**. Open separate terminal windows for each.

### Terminal 1 — Frontend (Next.js)

```bash
cd frontend
npm run dev
```

Runs on: `http://localhost:3000`

### Terminal 2 — Backend (Node.js / Express)

```bash
cd backend
npm run dev
```

Runs on: `http://localhost:5001` (or the port set in your `.env`)

### Terminal 3 — AI Backend (FastAPI)

```bash
cd aihounds
uvicorn aihounds.app:app --reload
```

Runs on: `http://127.0.0.1:8000`

### Terminal 4 (Optional) — Mobile App (Expo)

```bash
cd app
npx expo start
```

Use the Expo Go app on your phone or an emulator to preview.

---

## 5. Access the Application

Open your browser and navigate to:

```
http://localhost:3000
```

### Demo Credentials

- **Email:** `varad@gmail.com`
- **Password:** `12345678`

Or sign up with a new account to start fresh.

---

## Troubleshooting

| Issue | Solution |
|---|---|
| Prisma client errors | Run `npx prisma generate` in both `frontend/` and `backend/` |
| MongoDB connection failures | Verify your `DATABASE_URL` is correct and the cluster allows your IP |
| FastAPI module not found | Make sure you run `uvicorn` from the project root or have `aihounds` in your Python path |
| CORS errors in browser | Ensure all three services are running and the URLs in `.env` match |
| API key errors (OpenAI, Tavily, etc.) | Double-check all API keys in your `aihounds/.env` file |

