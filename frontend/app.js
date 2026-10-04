
const chatForm = document.getElementById("chat-form");
const messageInput = document.getElementById("message-input");
const chatBox = document.getElementById("chat-box");
const sendButton = document.getElementById("send-button");

let sessionId = null;


/* =========================
   Add message to chat
========================= */

function addMessage(content, role) {

    const message = document.createElement("div");

    message.className = `message ${role}`;

    message.textContent = content;

    chatBox.appendChild(message);

    chatBox.scrollTop = chatBox.scrollHeight;
}


/* =========================
   Loading indicator
========================= */

function showLoading() {

    const loading = document.createElement("div");

    loading.id = "loading-message";

    loading.className = "message assistant";

    loading.innerHTML = `
        <span class="typing">Assistant is thinking...</span>
    `;

    chatBox.appendChild(loading);

    chatBox.scrollTop = chatBox.scrollHeight;
}


function removeLoading() {

    const loading = document.getElementById("loading-message");

    if (loading) {
        loading.remove();
    }
}


/* =========================
   Send message
========================= */

async function sendMessage(message) {

    if (!message.trim()) {
        return;
    }


    addMessage(message, "user");

    messageInput.value = "";

    sendButton.disabled = true;

    messageInput.disabled = true;

    showLoading();


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

            throw new Error(
                `Request failed with status ${response.status}`
            );

        }


        const data = await response.json();


        sessionId = data.session_id;


        removeLoading();

        addMessage(
            data.message,
            "assistant"
        );


    } catch (error) {

        removeLoading();

        console.error(error);

        addMessage(
            "Sorry, something went wrong while contacting the assistant. Please try again.",
            "assistant"
        );

    } finally {

        sendButton.disabled = false;

        messageInput.disabled = false;

        messageInput.focus();

    }
}


/* =========================
   Chat form submit
========================= */

chatForm.addEventListener("submit", function(event) {

    event.preventDefault();

    const message = messageInput.value.trim();

    sendMessage(message);

});


/* =========================
   Evaluation test buttons
========================= */

const testCards = document.querySelectorAll(".test-card");


testCards.forEach(function(card) {

    card.addEventListener("click", function() {

        const prompt = card.dataset.prompt;

        messageInput.value = prompt;

        messageInput.focus();

        messageInput.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });

    });

});
