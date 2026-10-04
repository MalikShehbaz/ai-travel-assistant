
const chatForm = document.getElementById("chat-form");

const messageInput = document.getElementById("message-input");

const chatBox = document.getElementById("chat-box");

const sendButton = document.getElementById("send-button");

const testCards = document.querySelectorAll(".test-card");


/*
    The session ID is kept in the browser.

    This means multiple messages from the same browser
    session are sent to the same backend conversation.
*/

let sessionId = null;


/* =========================
   Add message
========================= */

function addMessage(content, role) {

    const message = document.createElement("div");

    message.className = `message ${role}`;

    message.textContent = content;

    chatBox.appendChild(message);

    chatBox.scrollTop = chatBox.scrollHeight;
}


/* =========================
   Loading message
========================= */

function showLoading() {

    removeLoading();

    const loading = document.createElement("div");

    loading.id = "loading-message";

    loading.className = "message assistant";

    loading.innerHTML = `
        <span class="typing">
            Assistant is thinking...
        </span>
    `;

    chatBox.appendChild(loading);

    chatBox.scrollTop = chatBox.scrollHeight;
}


function removeLoading() {

    const loading =
        document.getElementById("loading-message");

    if (loading) {
        loading.remove();
    }
}


/* =========================
   Set UI loading state
========================= */

function setLoadingState(isLoading) {

    sendButton.disabled = isLoading;

    messageInput.disabled = isLoading;

    testCards.forEach(function(card) {
        card.disabled = isLoading;
    });

}


/* =========================
   Send message to FastAPI
========================= */

async function sendMessage(message) {

    const cleanMessage = message.trim();

    if (!cleanMessage) {
        return;
    }


    /*
        Show the customer's message immediately.
    */

    addMessage(
        cleanMessage,
        "user"
    );


    /*
        Clear the input.
    */

    messageInput.value = "";


    /*
        Disable controls while waiting
        for the backend.
    */

    setLoadingState(true);

    showLoading();


    try {

        const response = await fetch(
            "/api/v1/chat",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    message: cleanMessage,

                    session_id: sessionId
                })
            }
        );


        /*
            Handle HTTP errors.
        */

        if (!response.ok) {

            let errorMessage =
                `Request failed with status ${response.status}.`;

            try {

                const errorData =
                    await response.json();

                if (errorData.detail) {
                    errorMessage =
                        `Request failed: ${errorData.detail}`;
                }

            } catch (error) {
                /*
                    Ignore JSON parsing errors.
                */
            }

            throw new Error(errorMessage);
        }


        /*
            Convert response to JSON.
        */

        const data =
            await response.json();


        /*
            Save the session ID returned by FastAPI.

            Future messages from this browser session
            will use the same ID.
        */

        sessionId = data.session_id;


        /*
            Remove loading indicator.
        */

        removeLoading();


        /*
            Display assistant response.
        */

        addMessage(
            data.message,
            "assistant"
        );


    } catch (error) {

        console.error(
            "Chat request failed:",
            error
        );


        removeLoading();


        addMessage(
            "Sorry, the assistant could not process this request. Please try again.",
            "assistant"
        );


    } finally {

        setLoadingState(false);

        messageInput.focus();

    }

}


/* =========================
   Normal chat submission
========================= */

chatForm.addEventListener(
    "submit",
    function(event) {

        event.preventDefault();

        const message =
            messageInput.value.trim();

        sendMessage(message);

    }
);


/* =========================
   Evaluation buttons
========================= */

testCards.forEach(
    function(card) {

        card.addEventListener(
            "click",
            function() {

                const prompt =
                    card.dataset.prompt;

                /*
                    Automatically execute the
                    selected evaluation test.
                */

                sendMessage(prompt);

            }
        );

    }
);


/* =========================
   Enter key
========================= */

messageInput.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            chatForm.requestSubmit();

        }

    }
);
