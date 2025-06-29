---

# 🎙️ AI Podcast Generator

This project generates AI-powered podcast conversations using **GPT-4o (Together AI)** for script generation and **ElevenLabs** for realistic voice synthesis. The generated podcast combines both speakers' voices into a single audio output via a simple **Streamlit** interface.

---

## 🚀 Features

✅ Generate dynamic podcast conversations using GPT-4o
✅ Realistic voice synthesis with ElevenLabs Text-to-Speech
✅ Combines multiple speaker voices into a single audio clip
✅ Streamlit-based web interface for easy use

---

## 📁 Project Structure

```
MY_PROJECT_IBM/
├── PODCAST.py           # Main Streamlit app
├── requirements.txt     # Required Python packages
└── README.md            # Project documentation
```

---

## 🛠️ Installation

1. **Clone the Repository**

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

2. **Create Virtual Environment (Optional but Recommended)**

```bash
python -m venv venv
source venv/bin/activate   # For Linux/Mac
venv\Scripts\activate      # For Windows
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

---

## 🔑 API Keys Setup

You need valid API keys for:

* **Together AI** (GPT-4o)
* **ElevenLabs** (Text-to-Speech)

Open the `PODCAST.py` file and update the placeholders:

```python
TOGETHER_API_KEY = "YOUR-API-KEY"
ELEVENLABS_API_KEY = "YOUR-ELEVENLABS-API-KEY"
```

---

## ▶️ Running the Application

To launch the Streamlit app:

```bash
streamlit run PODCAST.py
```

The app will open in your browser at:

```
http://localhost:8501
```

---

## ⚠️ Important Notes

* ElevenLabs API usage consumes credits based on text length. Monitor your quota at [https://elevenlabs.io](https://elevenlabs.io).
* Together AI API access may require approval or usage limits depending on your plan.
* If your ElevenLabs quota is exceeded, the app will raise an error.

---

## 💡 Future Enhancements

* Speaker selection from the UI
* Adjustable podcast duration
* Downloadable audio files
* Multilingual support

---

## 🧑‍💻 Author

Developed by **Raghuram Sivakumar**

---

**Enjoy creating AI-generated podcasts! 🎧**

---

