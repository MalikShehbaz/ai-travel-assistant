const form = document.getElementById("chat-form");
const input = document.getElementById("message-input");
const chatBox = document.getElementById("chat-box");

let sessionId = null;


function addMessage(role, content) {
    const message = document.createElement("div");

    message.className = `message ${role}`;
    message.textContent = content;

    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight;
}


form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const message = input.value.trim();

    if (!message) {
        return;
    }

    addMessage("user", message);

    input.value = "";

    try {
        const response = await fetch("/api/v1/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message,
                session_id: sessionId
            })
        });

        if (!response.ok) {
            throw new Error("Request failed");
        }

        const data = await response.json();

        sessionId = data.session_id;

        addMessage("assistant", data.message);

    } catch (error) {
        addMessage(
            "assistant",
            "Sorry, something went wrong. Please try again."
        );
    }
});