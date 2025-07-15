

# Code Section Detection in Videos using CLIP and OCR


The aim of this project is to **automatically detect, extract, and analyze frames from a video that contain programming code**, specifically when code is displayed in an editor or terminal. This can be useful in:

* **Educational videos** (e.g., tutorials or lectures)
* **Software walkthroughs**
* **Livestreams or recorded screencasts**
* **Creating summaries or highlights** of code-related content

The pipeline uses:

* **Computer Vision** (OpenCV)
* **Vision-Language Models** (OpenAI CLIP)
* **Optical Character Recognition** (EasyOCR)

---

## 🧠 Pipeline Overview

### 1. 🔽 **Download the Video**

Using `yt_dlp`, a YouTube video is downloaded locally in `.mp4` format.

* YouTube download options are configured to:

  * Use the best video+audio format
  * Avoid adaptive streaming (DASH/HLS)
  * Include custom headers and a cookie file if needed

📄 *Function: `download_vid(name, url)`*

---

### 2. 🎞️ **Extract Frames at Fixed Intervals**

* The downloaded video is opened using OpenCV.
* Frames are extracted every **10 seconds**.
* The first frame is saved, and subsequent frames are saved as `d{timestamp}.png`.

🗂️ *Example filenames: `d10.png`, `d20.png`, ...*

---

### 3. 🖼️ **Detect Code-Containing Frames Using CLIP**

Each saved frame is passed through the **CLIP model** to determine if it shows code.

* CLIP compares the frame with textual prompts such as:

  * `"a code editor"`
  * `"a terminal with code"`
  * `"code"`
* If the CLIP model finds high similarity with those prompts, the frame is marked as containing code.

📄 *Function: `iscodeframe(path)`*

---

### 4. ⏱️ **Extract Time Intervals with Code**

Given the list of timestamps and which frames are labeled as code-containing:

* The script calculates the **time intervals** in the video where code appears.
* This allows skipping non-code content and **focusing only on relevant parts**.

📄 *Function: `get_code_intervals(timestamps, code)`*

---

### 5. 📸 **Re-Extract All Frames Within Code Intervals**

Once code-containing intervals are found:

* The video is replayed.
* All frames within those intervals are extracted again for **higher granularity analysis**.

📄 *Function: `re_get_frames(intervals)`*

---

### 6. 🧾 **Extract Visible Code with EasyOCR (Optional)**

The extracted code frames can optionally be passed to **EasyOCR** to read visible text/code.

* This allows building a **textual index** of code from the video
* Could support search, summaries, or dataset building

📄 *Function: `easy_ocr(image)`*

---

## 🧰 Tools and Technologies

| Tool         | Purpose                                 |
| ------------ | --------------------------------------- |
| `yt_dlp`     | Video downloading from YouTube          |
| `OpenCV`     | Frame extraction, image operations      |
| `CLIP`       | Vision-Language model to detect code    |
| `EasyOCR`    | Optical Character Recognition on frames |
| `Matplotlib` | Frame visualization                     |
| `PyTorch`    | Backend for CLIP model inference        |

---
