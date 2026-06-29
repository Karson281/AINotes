// Save to Vault — POST to local vault-server instead of download

const VAULT_SERVER = "http://100.98.113.30:18765";
const TOKEN = "kn-save-token-2026";

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

	document.getElementById("platform").textContent = "📡 " + platform;

	// Try to get page content
	try {
		const [result] = await chrome.scripting.executeScript({
			target: { tabId: tab.id },
			func: () => {
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

	document.getElementById("title").value = tab.title || "untitled";
}

detectPage();

document.getElementById("saveBtn").addEventListener("click", async () => {
	const title = document.getElementById("title").value.trim();
	if (!title) { document.getElementById("status").textContent = "Please enter a title"; return; }

	const platform = document.getElementById("platform").textContent.replace("📡 ", "");
	const content = document.getElementById("content").value;
	const tagsStr = document.getElementById("tags").value.trim();
	const tags = tagsStr ? tagsStr.split(",").map(t => t.trim()).filter(Boolean) : [];

	const btn = document.getElementById("saveBtn");
	const status = document.getElementById("status");
	btn.disabled = true;
	status.textContent = "Saving...";

	try {
		const resp = await fetch(VAULT_SERVER + "/api/save", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				token: TOKEN,
				title: title,
				content: content,
				source: platform,
				tags: tags,
			})
		});
		const data = await resp.json();
		if (resp.ok) {
			status.textContent = "✅ Saved to vault: " + (data.path || "");
		} else {
			status.textContent = "❌ Error: " + (data.error || resp.status);
		}
	} catch (e) {
		status.textContent = "❌ Server offline? Start vault-server first.";
	}
	setTimeout(() => { btn.disabled = false; }, 2000);
});
