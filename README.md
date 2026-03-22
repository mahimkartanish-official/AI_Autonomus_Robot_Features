# AI_Autonomus_Robot_Features
all the feature of the robo keeping ROS2 in mind

# 🤖 AI Robot Assistant

## Features
- Real-time face recognition (InsightFace)
- Face tracking + servo control
- Voice interaction system
- Modular architecture (vision + voice)

## Setup

### Vision
```bash
python -m venv envs/vision_env
pip install -r requirements_vision.txt

Voice
python -m venv envs/voice_env
pip install -r requirements_voice.txt
Run
python src/main.py

---

# 🔥 OPTIONAL (BEST PRACTICE)

Create:

### `requirements_vision.txt`
```txt
numpy==1.26.4
insightface==0.7.3
onnxruntime
opencv-python
requirements_voice.txt
numpy==1.22.0
TTS==0.22.0
vosk
sounddevice
