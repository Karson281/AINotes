// Detect platform and grab content from current tab
async function detectPage() {
	const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
	const tab = tabs[0];
	if (!tab) return;

	const url = tab.url || "";
	const host = new URL(url).hostname || "";
	let platform = "web";
	if (host.includes("perplexity")) platform = "Perplexity";
	else if (host.includes("gemini")) platform = "Gemini";
	else if (host.includes("deepseek")) platform = "DeepSeek";
	else if (host.includes("copilot")) platform = "Copilot";
	else if (host.includes("doubao")) platform = "豆包";
	else if (host.includes("qwen") || host.includes("tongyi")) platform = "千問";
	else platform = host.split(".").slice(-2, -1)[0] || "web";

	document.getElementById("platform").textContent = "Platform: " + platform;

	// Try to get page content
	try {
		const [result] = await chrome.scripting.executeScript({
			target: { tabId: tab.id },
			func: () => {
				// Try common selectors for different AI platforms
				let text = "";
				const selectors = [
					"article", "main", 'pre', 'textarea',
					'[class*="message"]', '[class*="chat"]',
					'conversation-container', '[class*="conversation"]',
					'[class*="content"]', '[class*="output"]',
					'[class*="dialog"]', "section"
				];
				for (const sel of selectors) {
					const el = document.querySelector(sel);
					if (el && el.innerText.length > 100) {
						text = el.innerText;
						break;
					}
				}
				if (!text) text = document.body.innerText;
				return text.substring(0, 8000);
			}
		});
		if (result && result.result) {
			document.getElementById("content").value = result.result;
		}
	} catch (e) {
		document.getElementById("content").value = "Error: " + e.message;
	}

	// Use page title as default
	document.getElementById("title").value = tab.title || "untitled";
}

detectPage();

document.getElementById("saveBtn").addEventListener("click", () => {
	const title = document.getElementById("title").value.trim();
	if (!title) { document.getElementById("status").textContent = "Please enter a title"; return; }

	const platform = document.getElementById("platform").textContent.replace("Platform: ", "");
	const content = document.getElementById("content").value;
	const tagsStr = document.getElementById("tags").value.trim();
	const tags = tagsStr ? tagsStr.split(",").map(t => t.trim()).filter(Boolean) : [];

	const now = new Date();
	const ds = now.toISOString().slice(0, 10);
	const dt = now.toISOString().slice(11, 16);
	const tagY = tags.length ? tags.map(t => "  - " + t).join("\n") : "  - topic/untagged";

	const filename = title.replace(/[^a-zA-Z0-9一-鿿]/g, "-").replace(/-+/g, "-").replace(/^-|-$/g, "").slice(0, 40) || "note";

	const note = [
		"---",
		"creation_date: " + ds,
		'source: "' + platform + '"',
		"tags:",
		tagY,
		"status: inbox",
		"---",
		"",
		"# " + title,
		"",
		"**Date:** " + ds + " " + dt,
		"**Source:** " + platform,
		"",
		"---",
		"",
		content,
		""
	].join("\n");

	const blob = new Blob([note], { type: "text/markdown" });
	const url = URL.createObjectURL(blob);
	const a = document.createElement("a");
	a.href = url;
	a.download = ds + "-" + filename + ".md";
	document.body.appendChild(a);
	a.click();
	document.body.removeChild(a);
	URL.revokeObjectURL(url);

	document.getElementById("status").textContent = "Downloaded! Move to vault 1-AI-Conversations/";
	document.getElementById("saveBtn").disabled = true;
	setTimeout(() => { window.close(); }, 2000);
});
