# AI-Powered YouTube Video Summarizer for Educational Content

An AI-powered system that analyzes and summarizes educational YouTube videos, combining text-based analysis with visual content processing to extract structured knowledge — including actual **code snippets extracted directly from video frames**.

> This project goes beyond just sending a transcript to an LLM. It explores video summarization at the frame level, using CLIP + OCR to detect and extract code shown on screen — no transcript required for that part.



---

## Project Structure

```
├── backend/
│   ├── audio_processing.py     # YouTube transcript extraction
│   ├── llm_call.py             # LLM API interaction 
│   ├── main.py                 # FastAPI app + ngrok server startup
│   ├── prompt2dict.py          # Structures summaries (steps, entities, detailed)
│   ├── prompts.py              # All prompt templates
│   ├── requirements.txt        # Python dependencies
│   ├── summary.py              # Text summarization logic
│   ├── video_processing.py     # CLIP + OCR code extraction pipeline
│   └── visual_summary.py       # Visual analysis module
```

---

## Features

- **Multi-level summarization** — high-level overview and detailed AI-generated summary
- **Step extraction** — identifies step-by-step instructions from educational content
- **Entity recognition** — automatically identifies and defines technical terms
- **Knowledge graph visualization** — interactive concept relationship maps
- **Code extraction** — detects and extracts code snippets from programming tutorials using CLIP + OCR, without relying on the transcript

---

## How the Code Extraction Works (CLIP + OCR Pipeline)

Most video summarizers just send a transcript to an LLM. The more interesting part of this project is extracting **actual code directly from video frames** there is no transcript needed for this part.

The pipeline has four stages:

### 1. Frame segmentation via histogram analysis

Instead of processing every frame, the video is sampled every 3 seconds. Consecutive frames are compared using HSV histogram differences (Bhattacharyya distance). A score above `0.6` signals a meaningful scene change, which creates a new **interval**. This avoids redundant processing and groups the video into semantically distinct segments.

### 2. CLIP-based code detection

For each interval, 4 representative frames are sampled: the start frame, 2 random frames from the middle, and the end frame. Each frame is passed to **CLIP** (`openai/clip-vit-base-patch32`) alongside 3 text prompts:

- `"programming code in a text editor"`
- `"a slide presentation"`
- `"a person or abstract background"`

CLIP computes similarity scores between the image and each prompt. If **≥ 2 out of 4 frames** score highest on the code prompt (with a threshold of `0.9`), the entire interval is flagged as a **code interval**.

### 3. OCR extraction

Within confirmed code intervals, **EasyOCR** runs on a frame every 6 seconds. Near-duplicate results are filtered using `SequenceMatcher` with an 85% similarity threshold — so the same code block appearing across multiple frames is only captured once.

### 4. LLM cleanup

The raw OCR output (which contains noise, misread characters, formatting issues) is passed to **Gemini** with a cleaning prompt to produce syntactically coherent, readable code.

```
YouTube URL
    ↓
Download video (yt-dlp)
    ↓
Frame sampling every 3s → HSV histogram diff → detect scene changes → intervals
    ↓
For each interval: sample 4 frames → CLIP classification (3 prompts)
    ↓ (≥ 2/4 votes as code)
EasyOCR every 6s within interval → deduplicate with SequenceMatcher
    ↓
Gemini LLM cleanup → clean extracted code
    ↓
Returned via /getcode API
```

> For a deeper look at the frame analysis approach, check `notes.md` in the `Video_processing/v2/` folder.

---

## Technology Stack

### Backend
- **FastAPI** — REST API framework
- **Python 3.x** — core language
- **YouTube Transcript API** — transcript extraction
- **Gemini API** — AI summarization and code cleanup
- **CLIP** (`openai/clip-vit-base-patch32`) — frame classification
- **EasyOCR** — text extraction from frames
- **yt-dlp** — video download
- **ngrok** — public tunnel for the Kaggle-hosted backend

### Frontend


---

## Setup and Installation

### Backend

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file in the `backend/` directory:

```env
GROK_API_KEY=your_gemini_api_key
YOUTUBE_API_KEY=your_youtube_api_key
ngrok_auth_token=your_ngrok_token
```

Start the server:

```bash
cd backend
python main.py
```

This starts the FastAPI server and opens a public ngrok tunnel. The tunnel URL is printed to the console you can use it as the base URL for the frontend, in the youtube-summarizer.tsx file 

### Frontend
https://github.com/NoorMajdoub/videosummarizerfronteend

```bash
cd frontend
npm install
npm start

```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/summarize` | Returns structured summary, steps, entities, and knowledge graph |
| POST | `/getcode` | Runs the CLIP + OCR pipeline and returns extracted code |

Both POST endpoints accept:
```json
{ "vid_url": "https://www.youtube.com/watch?v=..." }
```

---

## Core Modules

| File | Description |
|------|-------------|
| `audio_processing.py` | Fetches YouTube transcript |
| `summary.py` | Calls Gemini for text summarization |
| `prompt2dict.py` | Parses summaries into structured dict (steps, entities, etc.) |
| `prompts.py` | All prompt templates |
| `llm_call.py` | Gemini API wrapper |
| `video_processing.py` | Full CLIP + OCR code extraction pipeline |
| `visual_summary.py` | Visual content analysis |
| `main.py` | FastAPI app definition + ngrok server startup |

---




## Requirements

- Python 3.x
- Node.js and npm
- GPU (recommended for visual/code extraction)
- API access: Google Gemini, YouTube Data API, ngrok

---

## Contribution & Feedback

Pull requests and feature ideas are welcome! If you run into bugs or have suggestions — especially around making the code extraction faster or more accurate — feel free to open an issue.
