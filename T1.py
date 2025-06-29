import streamlit as st
from openai import OpenAI
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
import os
import traceback
from pydub import AudioSegment
import re
import uuid

# === KEYS & IDs ===
TOGETHER_API_KEY = "d838deb3436704d2d686f50ec96ddd315a1406ecf94084cf94776e0bdf69c2d7"
ELEVENLABS_API_KEY = "sk_b49ec3b07b2bbdab2b3daf7afa0d19b26858671ab9c5d351"
CHRIS = "UEKYgullGqaF0keqT8Bu"
AMELIA = "ZF6FPAbjXT4488VcRRnw"

# === CLIENT SETUP ===
openai_client = OpenAI(api_key=TOGETHER_API_KEY, base_url="https://api.together.xyz/v1")
eleven_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# === SCRIPT GENERATOR ===
def generate_podcast_script(topic):
    prompt = f"""
Write a podcast script between Alex and Jamie on the topic: "{topic}".
Use a natural, educational tone. Alternate lines like:
Alex: ...
Jamie: ...
Keep it around 600–800 words.
"""
    response = openai_client.chat.completions.create(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1500
    )
    return response.choices[0].message.content

# === LINE SPLITTER ===
def split_script(script):
    segments = []
    for line in script.strip().split("\n"):
        match = re.match(r"^(Alex|Jamie):\s*(.+)$", line.strip())
        if match:
            speaker, text = match.groups()
            segments.append((speaker, text))
    return segments

# === VOICE SYNTHESIS PER LINE ===
def synthesize_line(text, speaker):
    voice_id = CHRIS if speaker == "Alex" else AMELIA
    try:
        audio_stream = eleven_client.text_to_speech.convert(
            voice_id=voice_id,
            model_id="eleven_multilingual_v2",
            text=text,
            voice_settings=VoiceSettings(stability=0.3, similarity_boost=0.3)
        )
        audio_bytes = b"".join(audio_stream)
        file_name = f"{speaker}_{uuid.uuid4().hex[:6]}.mp3"
        file_path = os.path.join("segments", file_name)

        os.makedirs("segments", exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(audio_bytes)

        return file_path
    except Exception:
        traceback.print_exc()
        return None

# === COMBINE ALL AUDIO SEGMENTS ===
def combine_segments(segment_paths):
    combined = AudioSegment.empty()
    for path in segment_paths:
        if path and os.path.exists(path):
            combined += AudioSegment.from_file(path, format="mp3")
    output_path = "combined_podcast.mp3"
    combined.export(output_path, format="mp3")
    return output_path

# === STREAMLIT APP ===
st.set_page_config(page_title="🎙️ Podcast Generator", layout="centered")
st.title("🎧 AI Podcast Generator (Alternating Voices)")

topic = st.text_input("Enter a trending topic:", placeholder="e.g., Quantum Computing, Global Conflicts")

if st.button("🎤 Generate Podcast"):
    if not topic:
        st.warning("Please enter a topic.")
    else:
        with st.spinner("Generating script..."):
            script = generate_podcast_script(topic)
            segments = split_script(script)

        st.subheader("📜 Podcast Script")
        st.text_area("Generated Script", script, height=400)

        segment_paths = []
        with st.spinner("Synthesizing voices..."):
            for speaker, text in segments:
                file_path = synthesize_line(text, speaker)
                segment_paths.append(file_path)

        final_audio = combine_segments(segment_paths)

        if os.path.exists(final_audio):
            st.audio(final_audio, format="audio/mp3")
            st.download_button("📥 Download Full Podcast", open(final_audio, "rb"), file_name="ai_podcast.mp3")
            st.success("✅ Podcast generated with alternating voices.")
        else:
            st.error("❌ Failed to generate combined podcast.")
