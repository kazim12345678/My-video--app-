from moviepy.editor import *
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

# -----------------------------
# 1. FAKE SCRIPT (Dr. Shadé style)
# -----------------------------
script = """
You are not stuck because you lack talent.
You are stuck because you repeat the same habits every day.

Today, I want to share three micro-shifts
that can help you break the cycle
and rebuild your momentum.

Number one:
Change your self-talk.
Your words shape your identity.

Number two:
Take one small action.
Momentum is built, not found.

Number three:
Ask yourself:
What is one thing I can do today
that my future self will thank me for?

Small changes create big transformation.
Start today.
"""

# -----------------------------
# 2. Generate Fake Voice
# -----------------------------
tts = gTTS(script, lang='en')
tts.save("voice.mp3")

audio = AudioFileClip("voice.mp3")
duration = audio.duration

# -----------------------------
# 3. Create Animated Text Slides
# -----------------------------
def create_text_image(text, filename):
    W, H = 1080, 1920
    img = Image.new("RGB", (W, H), color=(20, 20, 20))
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype("arial.ttf", 70)
    lines = textwrap.wrap(text, width=18)

    y_text = 600
    for line in lines:
        w, h = draw.textsize(line, font=font)
        draw.text(((W - w) / 2, y_text), line, font=font, fill="white")
        y_text += h + 10

    img.save(filename)

# Break script into scenes
scenes = script.split("\n\n")
image_files = []

for i, scene in enumerate(scenes):
    filename = f"scene_{i}.png"
    create_text_image(scene, filename)
    image_files.append(filename)

# -----------------------------
# 4. Convert Images → Video Clips
# -----------------------------
clips = []
scene_duration = duration / len(image_files)

for img in image_files:
    clip = ImageClip(img).set_duration(scene_duration)

    # Add slow zoom-in effect
    clip = clip.resize(lambda t: 1 + 0.02 * t)

    clips.append(clip)

video = concatenate_videoclips(clips, method="compose")

# -----------------------------
# 5. Add Voice to Video
# -----------------------------
final_video = video.set_audio(audio)

# -----------------------------
# 6. Export Final Video
# -----------------------------
final_video.write_videofile(
    "dr_shade_style_demo.mp4",
    fps=30,
    codec="libx264",
    audio_codec="aac"
)

print("Video created: dr_shade_style_demo.mp4")
