import streamlit as st
from openai import OpenAI
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
import traceback

# === API KEYS ===
TOGETHER_API_KEY = "d838deb3436704d2d686f50ec96ddd315a1406ecf94084cf94776e0bdf69c2d7"
ELEVENLABS_API_KEY = "sk_b49ec3b07b2bbdab2b3daf7afa0d19b26858671ab9c5d351"

# === VOICE IDs ===
CHRIS = "UEKYgullGqaF0keqT8Bu"   # Alex
AMELIA = "ZF6FPAbjXT4488VcRRnw"  # Jamie

# === Initialize Clients ===
openai_client = OpenAI(
    api_key=TOGETHER_API_KEY,
    base_url="https://api.together.xyz/v1"
)
eleven_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# === Generate Podcast Script ===
def generate_podcast_script(topic):
    prompt = f"""
Write a podcast script between Alex and Jamie on the topic: "{topic}".
Use a conversational, educational tone. Format:
Alex: ...
Jamie: ...
Limit to 600–800 words.
"""
    response = openai_client.chat.completions.create(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1500
    )
    return response.choices[0].message.content

# === Split Script into Lines ===
def split_script(script):
    alex_lines, jamie_lines = [], []
    for line in script.split("\n"):
        if line.strip().startswith("Alex:"):
            alex_lines.append(line.replace("Alex:", "").strip())
        elif line.strip().startswith("Jamie:"):
            jamie_lines.append(line.replace("Jamie:", "").strip())
    return alex_lines, jamie_lines

# ✅ Final Fixed Voice Generator with Streaming Audio Support
def generate_voice(lines, voice_id, name_hint="output"):
    full_text = " ".join(lines).strip()

    if not full_text:
        print(f"⚠️ No text to synthesize for voice ID: {voice_id}")
        return None

    try:
        audio_stream = eleven_client.text_to_speech.convert(
            voice_id=voice_id,
            model_id="eleven_multilingual_v2",
            text=full_text,
            voice_settings=VoiceSettings(
                stability=0.2,
                similarity_boost=0.2
            )
        )

        audio_bytes = b"".join(audio_stream)  # 🔧 Fix: Convert generator to bytes
        file_path = f"{name_hint}_{voice_id}.mp3"

        with open(file_path, "wb") as f:
            f.write(audio_bytes)

        print(f"✅ Audio saved: {file_path}")
        return file_path
    except Exception:
        print("❌ Exception occurred during voice generation:")
        traceback.print_exc()
        return None

# === Streamlit App ===
st.set_page_config(page_title="🎙️ AI Podcast Generator", layout="centered")
st.title("🎙️ AI Podcast Generator (Together.ai + ElevenLabs)")

topic = st.text_input("Enter a trending topic:", placeholder="e.g., AI in Education, SpaceX updates")

# === Test Voice Button ===
if st.button("🎧 Run Test Voice"):
    test_audio = generate_voice(["Hello! This is a test voice from Chris using ElevenLabs."], CHRIS, name_hint="test_chris")
    if test_audio:
        st.audio(test_audio, format="audio/mp3")
        st.success("✅ Test audio generated.")
    else:
        st.error("❌ Test audio generation failed. Check terminal for error details.")

# === Main Podcast Generation ===
if st.button("Generate Podcast"):
    if not topic:
        st.warning("⚠️ Please enter a topic.")
    else:
        with st.spinner("📜 Generating script using Together.ai..."):
            script = generate_podcast_script(topic)
            alex_lines, jamie_lines = split_script(script)

        st.subheader("📝 Generated Script")
        st.text_area("Podcast Script", script, height=400)

        # Alex (CHRIS)
        with st.spinner("🎧 Generating Alex's voice..."):
            alex_audio = generate_voice(alex_lines, CHRIS, name_hint="alex")
        if alex_audio:
            st.audio(alex_audio, format="audio/mp3")
            st.download_button("📥 Download Alex (Chris)", open(alex_audio, "rb"), file_name="alex_voice.mp3")
        else:
            st.warning("⚠️ Alex's voice could not be generated.")

        # Jamie (AMELIA)
        with st.spinner("🎧 Generating Jamie's voice..."):
            jamie_audio = generate_voice(jamie_lines, AMELIA, name_hint="jamie")
        if jamie_audio:
            st.audio(jamie_audio, format="audio/mp3")
            st.download_button("📥 Download Jamie (Amelia)", open(jamie_audio, "rb"), file_name="jamie_voice.mp3")
        else:
            st.warning("⚠️ Jamie's voice could not be generated.")
