let searchForm = document.getElementById("searchForm");
let searchInput = document.getElementById("searchInput");
let searchButton = document.getElementById("searchButton");
let statusText = document.getElementById("status");
let results = document.getElementById("results");

let isSearching = false;

searchForm.addEventListener("submit", async (event) => {
	event.preventDefault();
	// The disabled controls already block new searches; this also covers any submit that slips through
	if (isSearching) return;

	let searchQuery = searchInput.value.trim();
	if (!searchQuery) return;

	setSearching(true);
	statusText.textContent = "Loading...";
	results.replaceChildren();

	try {
		let response = await fetch(`/api/retrive?q=${encodeURIComponent(searchQuery)}`);
		if (!response.ok) {
			throw new Error(`HTTP ${response.status}`);
		}
		let data = await response.json();
		console.log(data);

		results.replaceChildren(...data.results.map(createResultElement));
		statusText.textContent =
			data.results.length === 0 ? "No results found." : `${data.results.length} results`;
	} catch (error) {
		console.error("Search failed:", error);
		statusText.textContent = "Search failed, please try again.";
	} finally {
		setSearching(false);
		searchInput.focus();
	}
});

function setSearching(searching) {
	isSearching = searching;
	searchInput.disabled = searching;
	searchButton.disabled = searching;
}

function createResultElement(result) {
	let element = document.createElement("div");
	element.className = "element";

	let file = document.createElement("span");
	file.className = `file ${result.modality}`;
	file.append(createMedia(result));

	let meta = document.createElement("div");
	meta.className = "meta";
	meta.append(
		createSpan("modality", result.modality),
		// Cosine distance: 0 = identical, lower = more relevant
		createSpan("distance", `distance ${result.distance.toFixed(3)}`),
		createSpan("id", `#${result.id}`),
	);

	element.append(file, createSpan("title", result.title), meta);
	return element;
}

function createMedia(result) {
	// "data/images/..." is served by the app from public/data
	let src = `/${result.file}`;

	switch (result.modality) {
		case "image": {
			let image = document.createElement("img");
			image.src = src;
			image.alt = result.title;
			image.loading = "lazy";
			return image;
		}
		case "video": {
			let video = document.createElement("video");
			video.src = src;
			video.controls = true;
			video.preload = "metadata";
			return video;
		}
		case "audio": {
			let audio = document.createElement("audio");
			audio.src = src;
			audio.controls = true;
			audio.preload = "none";
			return audio;
		}
		case "text": {
			let excerpt = document.createElement("p");
			excerpt.className = "excerpt";
			excerpt.textContent = "Loading text...";
			fetch(src)
				.then((response) => (response.ok ? response.text() : Promise.reject(response.status)))
				.then((text) => (excerpt.textContent = text))
				.catch(() => (excerpt.textContent = "Could not load the text."));
			return excerpt;
		}
		default: {
			let link = document.createElement("a");
			link.href = src;
			link.textContent = "Open file";
			return link;
		}
	}
}

function createSpan(className, text) {
	let span = document.createElement("span");
	span.className = className;
	span.textContent = text;
	return span;
}
