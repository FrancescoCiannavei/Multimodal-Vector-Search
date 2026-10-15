let addForm = document.getElementById("addForm");
let pathInput = document.getElementById("pathInput");
let addButton = document.getElementById("addButton");
let emptyList = document.getElementById("emptyList");
let fileList = document.getElementById("fileList");
let seedSelectedButton = document.getElementById("seedSelectedButton");
let seedAllButton = document.getElementById("seedAllButton");
let statusText = document.getElementById("status");
let progress = document.getElementById("progress");
let log = document.getElementById("log");

// Paths queued for "Seed selected", in the order they were added
let selectedFiles = [];
let isSeeding = false;

addForm.addEventListener("submit", (event) => {
	event.preventDefault();
	let path = pathInput.value.trim();
	if (!path) return;

	if (!selectedFiles.includes(path)) {
		selectedFiles.push(path);
		renderSelectedFiles();
	}
	pathInput.value = "";
	pathInput.focus();
});

seedSelectedButton.addEventListener("click", () => runSeed(selectedFiles));
// No files param makes the endpoint seed every file under data/
seedAllButton.addEventListener("click", () => runSeed([]));

// Leaving closes the stream, and the server stops seeding once the file in progress is done
window.addEventListener("beforeunload", (event) => {
	if (isSeeding) event.preventDefault();
});

async function runSeed(files) {
	// The disabled controls already block a second run; this also covers any click that slips through
	if (isSeeding) return;

	setSeeding(true);
	setStatus("Starting...");
	progress.hidden = true;
	log.replaceChildren();

	let params = new URLSearchParams(files.map((file) => ["files", file]));
	let finished = false;

	try {
		let response = await fetch(`/api/seed?${params}`);
		if (!response.ok) {
			throw new Error(`HTTP ${response.status}`);
		}

		for await (let event of readEvents(response.body)) {
			handleEvent(event);
			finished ||= event.event === "done" || event.event === "error";
		}
		if (!finished) {
			throw new Error("the connection closed before seeding finished");
		}
	} catch (error) {
		console.error("Seeding failed:", error);
		setStatus(`Seeding failed: ${error.message}`, true);
	} finally {
		setSeeding(false);
	}
}

// The endpoint streams one JSON event per line, but a chunk can end mid-line,
// so the trailing partial line is kept until the rest of it arrives
async function* readEvents(body) {
	let reader = body.pipeThrough(new TextDecoderStream()).getReader();
	let buffer = "";

	while (true) {
		let { value, done } = await reader.read();
		if (done) break;

		buffer += value;
		let lines = buffer.split("\n");
		buffer = lines.pop();
		for (let line of lines) {
			if (line.trim()) yield JSON.parse(line);
		}
	}
	if (buffer.trim()) yield JSON.parse(buffer);
}

function handleEvent(event) {
	switch (event.event) {
		case "start":
			progress.max = Math.max(event.total, 1);
			progress.value = 0;
			progress.hidden = false;
			setStatus(`0 of ${event.total} seeded...`);
			break;
		case "progress":
			progress.value = event.current;
			setStatus(`${event.current} of ${event.total} seeded...`);
			appendLogEntry(event);
			break;
		case "done":
			setStatus(event.message);
			break;
		case "error":
			setStatus(event.message, true);
			break;
	}
}

function setSeeding(seeding) {
	isSeeding = seeding;
	pathInput.disabled = seeding;
	addButton.disabled = seeding;
	seedAllButton.disabled = seeding;
	seedSelectedButton.disabled = seeding || selectedFiles.length === 0;
	for (let button of fileList.querySelectorAll("button")) {
		button.disabled = seeding;
	}
}

function setStatus(text, isError = false) {
	statusText.textContent = text;
	statusText.classList.toggle("error", isError);
}

function renderSelectedFiles() {
	fileList.replaceChildren(...selectedFiles.map(createSelectedFileElement));
	emptyList.hidden = selectedFiles.length > 0;
	seedSelectedButton.textContent = `Seed ${selectedFiles.length} ${selectedFiles.length === 1 ? "file" : "files"}`;
	setSeeding(isSeeding);
}

function createSelectedFileElement(path) {
	let remove = document.createElement("button");
	remove.type = "button";
	remove.className = "remove";
	remove.textContent = "×";
	remove.setAttribute("aria-label", `Remove ${path}`);
	remove.addEventListener("click", () => {
		selectedFiles = selectedFiles.filter((file) => file !== path);
		renderSelectedFiles();
		pathInput.focus();
	});

	let item = document.createElement("li");
	item.append(createSpan("path", path), remove);
	return item;
}

function appendLogEntry(event) {
	let item = document.createElement("li");
	item.append(createSpan("modality", event.modality), createSpan("path", event.path));
	log.append(item);
	// Keeps the latest file in view once the list starts scrolling
	log.scrollTop = log.scrollHeight;
}

function createSpan(className, text) {
	let span = document.createElement("span");
	span.className = className;
	span.textContent = text;
	return span;
}
