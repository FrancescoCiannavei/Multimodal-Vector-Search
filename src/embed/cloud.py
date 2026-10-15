from functools import cache
from io import BytesIO
from mimetypes import guess_type

import numpy as np
from google import genai
from google.genai import types
from PIL import Image


MODEL_ID = "gemini-embedding-2"
DIMENSIONS = 768

@cache
def getClient():
	return genai.Client()

def embed(content):
	result = getClient().models.embed_content(
		model=MODEL_ID,
		contents=content,
		config=types.EmbedContentConfig(output_dimensionality=DIMENSIONS),
	)
	# A numpy array like the local model returns, which pgvector adapts to a vector in queries
	return np.array(result.embeddings[0].values, dtype=np.float32)

def embedBytes(data, mimeType):
	return embed(types.Part.from_bytes(data=data, mime_type=mimeType))

def embedFile(path):
	with open(path, "rb") as f:
		return embedBytes(f.read(), guess_type(path)[0])

def embedQuery(query):
	return embed(f"task: search result | query: {query}")

def embedText(title, content):
	return embed(f"title: {title} | text: {content}")

def embedImage(path):
	if guess_type(path)[0] in ("image/png", "image/jpeg"):
		return embedFile(path)

	with Image.open(path) as image:
		buffer = BytesIO()
		image.convert("RGB").save(buffer, format="PNG")
	return embedBytes(buffer.getvalue(), "image/png")

def embedAudio(path):
	return embedFile(path)

def embedVideo(path):
	return embedFile(path)
