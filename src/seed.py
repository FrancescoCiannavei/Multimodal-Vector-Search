from os import walk
from os.path import basename, join, splitext
from db import runSql
from embeddings import embedAudio, embedImage, embedText, embedVideo

MODALITY_BY_EXTENSION = {
	".txt": "text",
	".jpg": "image",
	".webp": "image",
	".avif": "image",
	".mp3": "audio",
	".mp4": "video",
}

MEDIA_EMBEDDERS = {
	"image": embedImage,
	"audio": embedAudio,
	"video": embedVideo,
}

def _raise(error):
	raise error

def retriveSeedFiles():
	mypath = "data"
	# os.walk silently skips missing or unreadable directories unless onerror raises
	files = [
		join(root, f)
		for root, _, names in walk(mypath, onerror=_raise)
		for f in names
		if splitext(f)[1].lower() in MODALITY_BY_EXTENSION
	]
	return sorted(files)

# "byrne-vs-fischer_game.mp4" -> "byrne vs fischer game"
def titleFromPath(path):
	return splitext(basename(path))[0].replace("-", " ").replace("_", " ")

# TODO: allow seeding of only certain files
# Example: we upload "magnus-carlsen.jpg" and we want to seed only that 1 file
def seed():
	print("Seeding...")
	files = retriveSeedFiles()
	for i, path in enumerate(files, start=1):
		modality = MODALITY_BY_EXTENSION[splitext(path)[1].lower()]

		print(f"[{i}/{len(files)}] {modality}: {path}")
		if modality == "text":
			with open(path, encoding="utf-8") as f:
				embedding = embedText(titleFromPath(path), f.read())
		else:
			embedding = MEDIA_EMBEDDERS[modality](path)

		# Upsert on path, so seeding again refreshes rows instead of duplicating them
		runSql("""
			INSERT INTO documents (path, modality, embedding)
			VALUES (%s, %s, %s)
			ON CONFLICT (path) DO UPDATE SET
				modality = EXCLUDED.modality,
				embedding = EXCLUDED.embedding
		""", (path, modality, embedding))

	print(f"Seeded {len(files)} files")
	return len(files)

if __name__ == "__main__":
	seed()
