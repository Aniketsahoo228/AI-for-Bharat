# AI for Bharat - AI-Powered Learning Platform

An intelligent platform for analyzing documents and generating personalized learning paths using AI.

## 📽️ Video Tutorial 
[Click Here](https://youtu.be/v27Sq8aGkgA)


## 🚀 Features

- **PDF Analysis** - Upload and analyze PDF documents
- **Text Extraction** - Automatically extract text from PDFs
- **AI-Powered Insights** - Generate summaries and learning workflows
- **Modern UI** - Clean, professional interface built with React
- **Full-Stack Integration** - Integrated frontend and backend architecture
- **Type-Safe** - Full TypeScript support

## 📦 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Install frontend dependencies**
```bash
npm install
```

2. **Install backend dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup environment variables**
```bash
cp .env.example .env
# Edit .env and add your Google API key
```

### Running the Application

**Terminal 1 - Start Backend:**
```bash
python api/main.py
```

**Terminal 2 - Start Frontend:**
```bash
npm run dev
```

Visit `http://localhost:5173`!

## 🏗️ Project Structure

All development happens in the root directory. The `frontend/` subdirectory is deprecated.

```
├── api/                 # FastAPI Backend
├── services/            # AI Services
├── components/          # React Components
├── pages/              # React Pages
├── lib/                # Utilities & API client
├── INTEGRATION_GUIDE.md # Detailed documentation
```

## 🛠️ Technologies

**Frontend:** Vite, React 18, TypeScript, Tailwind CSS, Axios
**Backend:** FastAPI, SQLAlchemy, Google Gemini API

## 📖 Full Documentation

See [INTEGRATION_GUIDE.md](./INTEGRATION_GUIDE.md) for detailed setup and architecture.

## ⚠️ Important

- Backend must run on port 8000
- Frontend runs on port 5173
- Configure `.env` with your API keys

## 📝 License

MIT License
