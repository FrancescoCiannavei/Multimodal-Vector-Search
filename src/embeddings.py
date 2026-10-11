from functools import cache

import torch
from PIL import Image
from sentence_transformers import SentenceTransformer

MODEL_ID = "google/embeddinggemma-2"

@cache
def getModel():
	# Loaded on first use, then reused. With no config_kwargs this is the full 740M model:
	# text backbone plus the vision and audio encoders.
	# float32 because most CPUs lack fast bfloat16, and float16 silently produces NaNs with this model.
	return SentenceTransformer(MODEL_ID, model_kwargs={"torch_dtype": torch.float32})


# All embeddings come back L2-normalized (the model ends in a Normalize layer), so cosine distance works directly.

def embedQuery(query):
	return getModel().encode(query, prompt_name="SearchQuery")

def embedText(title, content):
	# Text needs a task prefix; documents with a title use this format (per the model card)
	return getModel().encode(f"title: {title} | text: {content}")

def embedImage(path):
	# Opened with Pillow because torchvision's decoder can't read .avif
	with Image.open(path) as image:
		return getModel().encode({"image": image.convert("RGB")})

def embedAudio(path):
	# Decoded and resampled to 16 kHz mono by torchcodec; the model accepts up to ~327 seconds
	return getModel().encode({"audio": path})

def embedVideo(path):
	# Frames only (the audio track is ignored), sampled at 1 fps. Videos longer than 32 seconds
	# get 32 frames spread evenly across their whole length (the processor's default overflow_strategy)
	return getModel().encode({"video": path})
