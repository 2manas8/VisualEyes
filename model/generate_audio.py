import os
from gtts import gTTS

coco_classes = [
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", "traffic light",
    "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow",
    "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee",
    "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard",
    "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
    "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch",
    "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse", "remote", "keyboard", "cell phone",
    "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors", "teddy bear",
    "hair drier", "toothbrush"
]

system_phrases = [
    "no objects", 
    "a lot of objects", 
    "and", 
    "detected"
]

all_inputs = coco_classes + system_phrases

save_dir = "../assets/audio"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

print(f"Generating {len(all_inputs)} audio files in '{save_dir}'...")

for phrase in all_inputs:
    tts = gTTS(text=phrase, lang='en', slow=False)
    filename = f"{phrase.replace(' ', '_')}.mp3"
    save_path = os.path.join(save_dir, filename)
    tts.save(save_path)
    print(f"Saved: {filename}")

print("Done! All audio files are ready.")