
import gradio as gr
from kokoro import KPipeline
import soundfile as sf
import tempfile
import numpy as np

pipeline = KPipeline(lang_code='a')

def synthesize(text, speed):
    combined_audio = np.array([], dtype=np.float32)
    generator = pipeline(text, voice="af_heart", speed=speed)
    for _, _, audio in generator:
        combined_audio = np.concatenate((combined_audio, audio))

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    sf.write(tmp_file.name, combined_audio, 24000)
    return tmp_file.name

demo = gr.Interface(
    fn=synthesize,
    inputs=[
        gr.Textbox(lines=8, label="Enter your text"),
        gr.Slider(0.5, 1.5, value=1.0, label="Speech Speed"),
    ],
    outputs=gr.Audio(type="filepath", label="Generated Audio"),
    title="🎙️ Kokoro TTS Web App",
    description="Generate speech from text using Kokoro TTS engine."
)

demo.launch()
