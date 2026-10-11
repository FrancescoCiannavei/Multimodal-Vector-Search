document.getElementById("searchForm").addEventListener("submit", async (event) => {
	event.preventDefault();
	let searchInput = document.getElementById("searchInput");
	let searchQuery = searchInput.value;

	let response = await fetch(`/api/retrive?q=${encodeURIComponent(searchQuery)}`);
	if (!response.ok) {
		console.error(`Search failed: HTTP ${response.status}`);
		return;
	}
	console.log(await response.json());
});
