
#  AI-Powered YouTube Video Summarizer for Educational Content

An AI-powered system that analyzes and summarizes educational YouTube videos, combining text-based analysis with experimental visual content processing to enhance learning and information retrieval.

PS: I wanted to work on something tha goes beyond just using the transcript and sending it to an LLM and just print the summary.explored a bit video summary concept.
Added a features for video analysis (the visual aspect of the video not just the audio) to create a system able to extract the code from the video.

(Still in testing but works fine with videos under 20 minutes)=Detect the right frames - video sections with code in it and extract the code with OCR tools.

PS: please check notes.md in v2 folder for the video processing section(which is what is moslty interesting about this proj :3 )

---
##  Project Structure

```
├── Video_processing/
│   ├── tools/                  # Utility tools and scripts
│   ├── v1/                     # Version 1 implementation (Random frames extraction )
│   └── v2/                     # Version 2 implementation (CLIP for smarter frames analysis and code extraction)
├── backend/
│   ├── __pycache__/            # Python cache files
│   ├── tools_not_used/         # Deprecated tools
│   ├── .env                    # Environment variables
│   ├── audio_processing.py     # YouTube transcript extraction
│   ├── main.py                 # FastAPI main application
│   ├── prompt2dict.py          # Summary processing utilities (get steps , get detailed summary , get entities)
│   ├── proxy.py                # Proxy configuration (needed for youtube dlp)
│   ├── requirements.txt        # Python dependencies
│   ├── summary.py              # Text summarization logic (prompt/api call)
│   └── visual_summary.py       # Visual analysis module
├── frontend/                   # React-based user interface
├── notebooks_testing/          # Kaggle notebooks for testing
└── video_summary_testing/      # Testing materials
```
---

## ✨ Features

* **Multi-Level Summarization**: High-level and detailed AI-generated summaries.
* **Step Extraction**: Identifies and extracts step-by-step instructions from educational content.
* **Entity Recognition**: Automatically identifies and defines technical terms and concepts.
* **Knowledge Graph Visualization**: Interactive concept relationship maps.
* **Visual Analysis (Experimental)**: Extracts code snippets from programming tutorials using CLIP + OCR.

---

## ⚙️ Technology Stack

### 🔧 Backend

* **FastAPI** – Web framework for APIs
* **Python 3.x** – Core programming language
* **YouTube Transcript API** – For extracting transcripts
* **Gemini API** – AI-powered summarization
* **CLIP + OCR** – Experimental visual content analysis

### 💻 Frontend

* **React** – UI framework
* **TypeScript** – Type safety
* **Tailwind CSS** – Styling

---

## 🚀 Setup and Installation

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

### Environment Configuration

Create a `.env` file in the `backend/` directory with the following:

```
GEMINI_API_KEY=your_gemini_api_key
YOUTUBE_API_KEY=your_youtube_api_key
```

### Frontend Setup

```bash
cd frontend
npm install
```

---

## 🧪 Usage

### Start the Backend Server

```bash
cd backend
python main.py
```

### Start the Frontend Application

```bash
cd frontend
npm start
```


## 🧩 Core Modules

* **audio\_processing.py** – YouTube transcript extraction
* **summary.py** – AI-based text summarization
* **visual\_summary.py** – Visual content and code extraction (experimental)
* **prompt2dict.py** – Structures and processes summaries
* **main.py** – FastAPI app entry point

---

## 🧪 Testing

Testing resources and examples:

* **`notebooks_testing/`** – Kaggle notebooks for iterative testing and dev
* **`video_summary_testing/`** – Additional validation/test materials/old methodes that did not work

---

## 🛠 Development Notes

* The `Video_processing/` directory contains versioned pipelines (v1 (not so good), v2 (good but slow))
* Visual analysis is experimental and GPU-intensive
* Optimized for **educational content**, especially **programming tutorials**
*I would recommend running the video summary section directly from the kaggle notebook

---

## 📋 Requirements

* Python 3.x
* Node.js and npm
* GPU (recommended for visual analysis)
* API access to:

  * Google Gemini
  * YouTube Data API

---

## 📬 Contribution & Feedback

Pull requests and feature ideas are welcome! If you encounter any bugs or have suggestions, feel free to open an issue, would love any ideas on how to make this (more ) usable.


