from os import environ

# This module acts like a proxy, if your production enviroment uses only one of the two options you can just move delete this file and the other option

isLocal = environ.get("RUN_VECTOR_MODEL_LOCALLY", "true").lower() == "true" # Runs local by default
if isLocal:
	from embed.local import embedQuery, embedText, embedImage, embedAudio, embedVideo
else:
	from embed.cloud import embedQuery, embedText, embedImage, embedAudio, embedVideo
