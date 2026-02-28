// Theme Toggle
function toggleTheme() {
    document.body.classList.toggle("light-mode");
    const isLight = document.body.classList.contains("light-mode");
    const icon = document.querySelector(".theme-btn:last-child i");
    
    // Save preference
    localStorage.setItem('theme', isLight ? 'light' : 'dark');
    
    if (isLight) {
        icon.classList.replace("ph-moon", "ph-sun");
    } else {
        icon.classList.replace("ph-sun", "ph-moon");
    }
}

// Drag & Drop Logic
const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");

dropZone.addEventListener("click", () => fileInput.click());

dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("dragover");
});

dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("dragover");
});

dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("dragover");
    const files = e.dataTransfer.files;
    if (files.length) {
        fileInput.files = files;
        uploadDoc();
    }
});

fileInput.addEventListener("change", uploadDoc);

// Upload Function
async function uploadDoc() {
    const file = fileInput.files[0];
    
    if (!file) return;
    
    // Basic validation
    if (!file.name.endsWith(".txt")) {
        alert("Only .txt files are allowed!");
        return;
    }
    
    const formData = new FormData();
    formData.append("file", file);

    // Show loading state (optional visual cue)
    dropZone.querySelector("p").innerText = "Uploading...";

    try {
        const response = await fetch("/api/upload", {
            method: "POST",
            body: formData
        });
        
        if (response.ok) {
            loadDocuments();
        } else {
            alert("Upload failed!");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Upload error");
    } finally {
        dropZone.querySelector("p").innerHTML = "<strong>Click to upload</strong> or drag & drop";
        fileInput.value = ""; // Reset input
    }
}

// Load Documents
async function loadDocuments() {
    try {
        const response = await fetch("/api/documents");
        const data = await response.json();
        const docs = data.documents || data;
        const list = document.getElementById("docList");
        
        list.innerHTML = "";

        if (!docs || docs.length === 0) {
            list.innerHTML = `<div style="text-align:center; padding: 20px; color: var(--text-muted); font-size: 13px;">No documents found</div>`;
            return;
        }

        docs.forEach(doc => {
            const div = document.createElement("div");
            div.className = "file-item";
            div.innerHTML = `
                <div class="file-name">
                    <i class="ph ph-file-text" style="color: var(--primary);"></i>
                    ${doc.name}
                </div>
                <button class="delete-btn" onclick="deleteDoc('${doc.id}')" title="Delete">
                    <i class="ph ph-trash"></i>
                </button>
            `;
            list.appendChild(div);
        });
    } catch (error) {
        console.error("Error loading docs:", error);
    }
}

// Delete Document
async function deleteDoc(docId) {
    // Create custom modal
    const modal = document.createElement('div');
    modal.style.cssText = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); display: flex; align-items: center; justify-content: center; z-index: 9999; backdrop-filter: blur(4px);';
    
    // Get computed styles to use actual color values
    const computedStyle = getComputedStyle(document.body);
    const bgColor = computedStyle.getPropertyValue('--bg-sidebar').trim() || '#18181b';
    const borderColor = computedStyle.getPropertyValue('--border').trim() || '#27272a';
    const textColor = computedStyle.getPropertyValue('--text-main').trim() || '#e4e4e7';
    const mutedColor = computedStyle.getPropertyValue('--text-muted').trim() || '#a1a1aa';
    
    modal.innerHTML = `
        <div style="background: ${bgColor}; padding: 24px; border-radius: 12px; max-width: 400px; box-shadow: 0 10px 40px rgba(0,0,0,0.5); border: 1px solid ${borderColor};">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
                <i class="ph-fill ph-warning-circle" style="font-size: 24px; color: #ef4444;"></i>
                <h3 style="margin: 0; font-size: 18px; color: ${textColor};">Delete Document?</h3>
            </div>
            <p style="color: ${mutedColor}; margin-bottom: 20px; font-size: 14px;">This action cannot be undone. The document and all its data will be permanently removed.</p>
            <div style="display: flex; gap: 10px; justify-content: flex-end;">
                <button id="cancelBtn" style="padding: 8px 16px; border-radius: 8px; border: 1px solid ${borderColor}; background: transparent; color: ${textColor}; cursor: pointer;">Cancel</button>
                <button id="confirmBtn" style="padding: 8px 16px; border-radius: 8px; border: none; background: #ef4444; color: white; cursor: pointer; font-weight: 500;">Delete</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Handle cancel
    modal.querySelector('#cancelBtn').onclick = () => modal.remove();
    modal.onclick = (e) => { if (e.target === modal) modal.remove(); };
    
    // Handle confirm
    modal.querySelector('#confirmBtn').onclick = async () => {
        modal.remove();
        await fetch(`/api/documents/${docId}`, { method: "DELETE" });
        loadDocuments();
    };
}

// Ask Question
async function askQuestion() {
    const inputField = document.getElementById("questionInput");
    const question = inputField.value.trim();
    if (!question) return;

    // Check if documents exist
    const response = await fetch("/api/documents");
    const data = await response.json();
    if (!data.documents || data.documents.length === 0) {
        showWarning("Please upload a document first before asking questions.");
        return;
    }

    const chatBox = document.getElementById("chatBox");
    
    // Hide intro message on first question
    const introMsg = chatBox.querySelector('.intro');
    if (introMsg) introMsg.remove();

    // Add User Message
    chatBox.innerHTML += `
        <div class="message user">
            <div class="message-content">${question}</div>
        </div>
    `;

    inputField.value = "";
    scrollToBottom();

    // Show a temporary loading bubble (optional, triggers later replacement)
    const loadingId = "loading-" + Date.now();
    chatBox.innerHTML += `
        <div class="message bot" id="${loadingId}">
            <div class="message-content" style="color: var(--text-muted); display: flex; align-items: center; gap: 8px;">
                <i class="ph ph-circle-notch" style="animation: spin 1s linear infinite;"></i>
                Thinking...
            </div>
        </div>
    `;
    scrollToBottom();

    try {
        const response = await fetch("/api/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question })
        });

        const data = await response.json();
        
        // Remove loading message
        document.getElementById(loadingId).remove();

        // Format Sources
        let sourcesHtml = "";
        if (data.sources && data.sources.length > 0) {
            // Filter sources - only show if content is highly relevant
            const relevantSources = data.sources.filter(src => {
                const content = src.content.toLowerCase();
                const answer = data.answer.toLowerCase();
                // Extract meaningful words (longer than 5 chars) from answer
                const meaningfulWords = answer.split(' ').filter(w => w.length > 5 && !['acme', 'tech'].includes(w.toLowerCase()));
                // Require at least 2 meaningful words to match
                const matches = meaningfulWords.filter(word => content.includes(word)).length;
                return matches >= 2;
            });

            if (relevantSources.length === 0 && data.sources.length > 0) {
                // If filter is too strict, show only the first source
                relevantSources.push(data.sources[0]);
            }

            // Extract keywords from question and answer for finding relevant snippets
            const questionWords = question.toLowerCase().split(' ').filter(w => w.length > 3);
            const answerWords = data.answer.toLowerCase().split(' ').filter(w => w.length > 4);
            const keywords = [...new Set([...questionWords, ...answerWords])];

            // Group sources by document name and show each chunk separately
            const sourcesByDoc = {};
            relevantSources.forEach((src, index) => {
                const key = `${src.document_name}_${index}`; // Unique key per chunk
                if (!sourcesByDoc[key]) {
                    sourcesByDoc[key] = {
                        name: src.document_name,
                        chunks: []
                    };
                }
                
                // Find best matching portion
                let displayContent = src.content;
                let bestMatchIndex = -1;
                let maxMatches = 0;
                
                // Find the position with most keyword matches
                for (let i = 0; i < displayContent.length - 100; i += 50) {
                    const snippet = displayContent.substring(i, i + 200).toLowerCase();
                    const matches = keywords.filter(kw => snippet.includes(kw)).length;
                    if (matches > maxMatches) {
                        maxMatches = matches;
                        bestMatchIndex = i;
                    }
                }
                
                // Extract relevant snippet
                if (bestMatchIndex !== -1 && displayContent.length > 250) {
                    const start = bestMatchIndex;
                    const end = Math.min(displayContent.length, start + 250);
                    displayContent = (start > 0 ? '...' : '') + displayContent.substring(start, end) + (end < src.content.length ? '...' : '');
                } else if (displayContent.length > 250) {
                    displayContent = displayContent.substring(0, 250) + '...';
                }
                
                sourcesByDoc[key].chunks.push(displayContent);
            });

            sourcesHtml = `<div class="sources-container" style="margin-top: 12px;">`;
            sourcesHtml += `<div style="font-size: 12px; color: var(--text-muted); margin-bottom: 8px;"><strong>Sources:</strong></div>`;
            
            Object.keys(sourcesByDoc).forEach(key => {
                const source = sourcesByDoc[key];
                sourcesHtml += `
                    <div class="source-chip" style="display: block; margin-bottom: 8px; padding: 10px; background: var(--surface); border-radius: 8px; border-left: 3px solid var(--primary);">
                        <div style="color: var(--primary); font-weight: 600; margin-bottom: 4px;">
                            <i class="ph-fill ph-file-text"></i>
                            ${source.name}
                        </div>
                        <div style="font-size: 12px; color: var(--text-muted); line-height: 1.4;">${source.chunks.join('<br><br>')}</div>
                    </div>
                `;
            });
            sourcesHtml += `</div>`;
        }

        // Add Bot Message
        chatBox.innerHTML += `
            <div class="message bot">
                <div class="message-content">
                    ${data.answer}
                    ${sourcesHtml}
                </div>
            </div>
        `;
        scrollToBottom();

    } catch (error) {
        document.getElementById(loadingId).innerHTML = `<div class="message-content" style="color: red;">Error fetching response.</div>`;
    }
}

// Scroll to bottom helper
function scrollToBottom() {
    const chatBox = document.getElementById("chatBox");
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Enable Enter key to send
document.getElementById("questionInput").addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        askQuestion();
    }
});

// Logout function
function logout() {
    window.location.replace("/logout");
}

// Show warning notification
function showWarning(message) {
    const existing = document.querySelector('.warning-toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = 'warning-toast';
    toast.style.cssText = 'position: fixed; top: 20px; right: 20px; background: #f59e0b; color: white; padding: 12px 20px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); z-index: 10000; animation: slideIn 0.3s ease;';
    toast.innerHTML = `<i class="ph-fill ph-warning"></i> ${message}`;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Load saved theme on page load
if (localStorage.getItem('theme') === 'light') {
    document.body.classList.add('light-mode');
    const icon = document.querySelector('.theme-btn:last-child i');
    if (icon) icon.classList.replace('ph-moon', 'ph-sun');
}

// Load chat history from database
async function loadChatHistory() {
    try {
        const response = await fetch('/api/chat-history');
        const data = await response.json();
        const chatBox = document.getElementById('chatBox');
        
        if (data.history && data.history.length > 0) {
            const introMsg = chatBox.querySelector('.intro');
            if (introMsg) introMsg.remove();
            
            data.history.forEach(msg => {
                chatBox.innerHTML += `
                    <div class="message user">
                        <div class="message-content">${msg.question}</div>
                    </div>
                `;
                
                let sourcesHtml = '';
                if (msg.sources && msg.sources.length > 0) {
                    sourcesHtml = '<div class="sources-container" style="margin-top: 12px;">';
                    sourcesHtml += '<div style="font-size: 12px; color: var(--text-muted); margin-bottom: 8px;"><strong>Sources:</strong></div>';
                    msg.sources.forEach(src => {
                        const content = src.content.length > 250 ? src.content.substring(0, 250) + '...' : src.content;
                        sourcesHtml += `
                            <div class="source-chip" style="display: block; margin-bottom: 8px; padding: 10px; background: var(--surface); border-radius: 8px; border-left: 3px solid var(--primary);">
                                <div style="color: var(--primary); font-weight: 600; margin-bottom: 4px;">
                                    <i class="ph-fill ph-file-text"></i>
                                    ${src.document_name}
                                </div>
                                <div style="font-size: 12px; color: var(--text-muted); line-height: 1.4;">${content}</div>
                            </div>
                        `;
                    });
                    sourcesHtml += '</div>';
                }
                
                chatBox.innerHTML += `
                    <div class="message bot">
                        <div class="message-content">
                            ${msg.answer}
                            ${sourcesHtml}
                        </div>
                    </div>
                `;
            });
            
            scrollToBottom();
        }
    } catch (error) {
        console.error('Error loading chat history:', error);
    }
}

// Initial Load
loadDocuments();
loadChatHistory();