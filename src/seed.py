from errno import ENOENT
from os import strerror, walk
from os.path import basename, join, normpath, splitext
from random import uniform
from time import sleep

# Demo replacement for src/seed.py: streams the same events as the real seed, but never calls the
# embedding API or writes to the database, so visitors can't burn through the free Gemini quota.
# Keep titleFromPath, retrive.py imports it.

MODALITY_BY_EXTENSION = {
	".txt": "text",
	".jpg": "image",
	".webp": "image",
	".avif": "image",
	".mp3": "audio",
	".mp4": "video",
}

# Seconds each file pretends to take, so the progress bar moves like a real run where media embeds slower than text
FAKE_EMBED_SECONDS = {
	"text": (0.1, 0.3),
	"image": (0.2, 0.5),
	"audio": (0.4, 0.8),
	"video": (0.6, 1.2),
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

# Pretends to seed the given paths, or every file under data/ when none are given
def seed(files=None):
	seedFiles = retriveSeedFiles()
	if files is None:
		files = seedFiles
	# Paths are matched against data/ instead of checked on disk, so the public demo can't be used
	# to probe for files elsewhere; anything else fails the way a missing file does in the real seed
	knownFiles = set(seedFiles)

	total = len(files)
	yield {"event": "start", "total": total}

	for i, path in enumerate(files, start=1):
		modality = MODALITY_BY_EXTENSION[splitext(path)[1].lower()]
		if normpath(path) not in knownFiles:
			raise FileNotFoundError(ENOENT, strerror(ENOENT), path)

		print(f"[{i}/{total}] {modality}: {path} (fake)")
		sleep(uniform(*FAKE_EMBED_SECONDS[modality]))
		yield {"event": "progress", "current": i, "total": total, "modality": modality, "path": path}

	print(f"Fake seeded {total} files")
	yield {"event": "done", "message": f"Seeded {total} files", "success": True, "count": total}

if __name__ == "__main__":
	for _ in seed():
		pass
