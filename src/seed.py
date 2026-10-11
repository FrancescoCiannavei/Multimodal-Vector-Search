from os import walk
from os.path import join, splitext
from db import runSql

ALLOWED_EXTENSIONS = {".jpg", ".webp", ".avif", ".mp3", ".mp4", ".txt"}

def _raise(error):
	raise error

def retriveSeedFiles():
	mypath = "data"
	# os.walk silently skips missing or unreadable directories unless onerror raises
	files = [
		join(root, f)
		for root, _, names in walk(mypath, onerror=_raise)
		for f in names
		if splitext(f)[1].lower() in ALLOWED_EXTENSIONS
	]
	return files

def seed():
	print("Seeding...")
	files = retriveSeedFiles()
	print(files)
	runSql("""
			SELECT * FROM documents;
		""")
