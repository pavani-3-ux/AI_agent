import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from level7_multi_agent import run_agent


# ============================================================
# CONFIGURATION
# ============================================================

HOST = "127.0.0.1"
PORT = 8000

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "agent.log")


# ============================================================
# LOGGING
# ============================================================

os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("production_ai_agent")
logger.setLevel(logging.INFO)

if not logger.handlers:

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=2_000_000,
        backupCount=3,
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="My AI Agent",
    description="Production AI Agent with Tools, Web Search, RAG and Multi-Agent capabilities",
    version="1.0.0"
)


# ============================================================
# REQUEST MODEL
# ============================================================

class ChatRequest(BaseModel):

    message: str


# ============================================================
# CHAT UI
# ============================================================

HTML_PAGE = r"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>My AI Agent</title>


<style>

* {
    box-sizing: border-box;
}


body {

    margin: 0;

    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        Roboto,
        Arial,
        sans-serif;

    background: #f7f7f8;

    height: 100vh;

    overflow: hidden;
}


.app {

    height: 100vh;

    display: flex;

    flex-direction: column;
}


/* =========================================================
   HEADER
   ========================================================= */

.header {

    height: 60px;

    background: #ffffff;

    border-bottom: 1px solid #e5e5e5;

    display: flex;

    align-items: center;

    padding: 0 24px;

    font-size: 18px;

    font-weight: 600;

    color: #202123;
}


.status {

    margin-left: 10px;

    font-size: 12px;

    font-weight: 400;

    color: #16a34a;
}


/* =========================================================
   CHAT AREA
   ========================================================= */

.chat-container {

    flex: 1;

    overflow-y: auto;

    padding: 30px 20px 120px;

}


.chat {

    max-width: 850px;

    margin: 0 auto;
}


.message {

    display: flex;

    margin-bottom: 28px;

    line-height: 1.6;

    font-size: 15px;
}


.message.user {

    justify-content: flex-end;
}


.message-content {

    max-width: 75%;

    padding: 14px 18px;

    border-radius: 16px;

    white-space: pre-wrap;

    word-wrap: break-word;
}


.user .message-content {

    background: #e9e9eb;

    color: #202123;

    border-bottom-right-radius: 5px;
}


.assistant .message-content {

    background: transparent;

    color: #202123;

    padding-left: 0;

    border-radius: 0;
}


/* =========================================================
   WELCOME
   ========================================================= */

.welcome {

    text-align: center;

    padding-top: 15vh;

    color: #202123;
}


.welcome h1 {

    font-size: 32px;

    margin-bottom: 10px;
}


.welcome p {

    color: #6b7280;

    font-size: 15px;
}


/* =========================================================
   INPUT AREA
   ========================================================= */

.input-area {

    position: fixed;

    bottom: 0;

    left: 0;

    right: 0;

    background: linear-gradient(
        transparent,
        #f7f7f8 25%
    );

    padding: 20px;
}


.input-wrapper {

    max-width: 850px;

    margin: 0 auto;

    display: flex;

    align-items: flex-end;

    gap: 10px;

    background: #ffffff;

    border: 1px solid #d9d9e3;

    border-radius: 16px;

    padding: 10px 12px;

    box-shadow:
        0 2px 8px rgba(0, 0, 0, 0.05);
}


textarea {

    flex: 1;

    border: none;

    outline: none;

    resize: none;

    font-family: inherit;

    font-size: 15px;

    line-height: 1.5;

    max-height: 150px;

    padding: 8px;

}


button {

    width: 38px;

    height: 38px;

    border: none;

    border-radius: 10px;

    background: #202123;

    color: white;

    cursor: pointer;

    font-size: 18px;
}


button:hover {

    background: #000000;
}


button:disabled {

    opacity: 0.5;

    cursor: not-allowed;
}


/* =========================================================
   PROCESSING
   ========================================================= */

.processing {

    display: flex;

    align-items: center;

    gap: 8px;

    color: #6b7280;

    font-size: 14px;
}


.dot {

    width: 6px;

    height: 6px;

    background: #6b7280;

    border-radius: 50%;

    animation: pulse 1.2s infinite;
}


.dot:nth-child(2) {

    animation-delay: 0.2s;
}


.dot:nth-child(3) {

    animation-delay: 0.4s;
}


@keyframes pulse {

    0%, 60%, 100% {

        opacity: 0.3;
    }

    30% {

        opacity: 1;
    }
}


.error {

    color: #dc2626;
}


/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 600px) {

    .header {

        padding: 0 16px;
    }

    .chat-container {

        padding-left: 12px;

        padding-right: 12px;
    }

    .message-content {

        max-width: 90%;
    }

    .welcome h1 {

        font-size: 26px;
    }
}

</style>

</head>


<body>

<div class="app">


    <div class="header">

        🤖 My AI Agent

        <span class="status">
            ● Online
        </span>

    </div>


    <div
        class="chat-container"
        id="chatContainer"
    >

        <div
            class="chat"
            id="chat"
        >

            <div
                class="welcome"
                id="welcome"
            >

                <h1>
                    How can I help you?
                </h1>

                <p>
                    Ask me anything.
                </p>

            </div>

        </div>

    </div>


    <div class="input-area">

        <div class="input-wrapper">

            <textarea
                id="messageInput"
                rows="1"
                placeholder="Message My AI Agent..."
                autocomplete="off"
            ></textarea>


            <button
                id="sendButton"
                onclick="sendMessage()"
                title="Send"
            >
                ↑
            </button>

        </div>

    </div>

</div>


<script>


const input =
    document.getElementById(
        "messageInput"
    );


const button =
    document.getElementById(
        "sendButton"
    );


const chat =
    document.getElementById(
        "chat"
    );


const welcome =
    document.getElementById(
        "welcome"
    );


const chatContainer =
    document.getElementById(
        "chatContainer"
    );


/* =========================================================
   AUTO RESIZE
   ========================================================= */

input.addEventListener(
    "input",
    function() {

        this.style.height = "auto";

        this.style.height =
            Math.min(
                this.scrollHeight,
                150
            ) + "px";
    }
);


/* =========================================================
   ENTER TO SEND
   ========================================================= */

input.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage();
        }
    }
);


/* =========================================================
   ADD MESSAGE
   ========================================================= */

function addMessage(
    role,
    text
) {

    const message =
        document.createElement(
            "div"
        );

    message.className =
        "message " + role;


    const content =
        document.createElement(
            "div"
        );

    content.className =
        "message-content";


    content.textContent =
        text;


    message.appendChild(
        content
    );


    chat.appendChild(
        message
    );


    chatContainer.scrollTop =
        chatContainer.scrollHeight;


    return message;
}


/* =========================================================
   PROCESSING MESSAGE
   ========================================================= */

function addProcessing() {

    const message =
        document.createElement(
            "div"
        );

    message.className =
        "message assistant";


    message.id =
        "processingMessage";


    message.innerHTML = `

        <div class="processing">

            <span>Processing</span>

            <span class="dot"></span>

            <span class="dot"></span>

            <span class="dot"></span>

        </div>

    `;


    chat.appendChild(
        message
    );


    chatContainer.scrollTop =
        chatContainer.scrollHeight;
}


/* =========================================================
   REMOVE PROCESSING
   ========================================================= */

function removeProcessing() {

    const processing =
        document.getElementById(
            "processingMessage"
        );


    if (processing) {

        processing.remove();
    }
}


/* =========================================================
   SEND MESSAGE
   ========================================================= */

async function sendMessage() {

    const message =
        input.value.trim();


    if (!message) {

        return;
    }


    welcome.style.display =
        "none";


    addMessage(
        "user",
        message
    );


    input.value = "";

    input.style.height = "auto";


    button.disabled =
        true;


    input.disabled =
        true;


    addProcessing();


    try {

        const response =
            await fetch(
                "/chat",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        message: message
                    })
                }
            );


        const data =
            await response.json();


        removeProcessing();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Request failed."
            );
        }


        addMessage(
            "assistant",
            data.answer
        );


    }

    catch (error) {

        removeProcessing();


        addMessage(
            "assistant",
            "Sorry, I couldn't process your request right now."
        );


        console.error(
            error
        );

    }

    finally {

        button.disabled =
            false;

        input.disabled =
            false;

        input.focus();
    }
}


/* =========================================================
   INITIAL FOCUS
   ========================================================= */

input.focus();


</script>

</body>

</html>
"""


# ============================================================
# HOME
# ============================================================

@app.get(
    "/",
    response_class=HTMLResponse
)
def home():

    return HTML_PAGE


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "My AI Agent",
        "timestamp": datetime.now().isoformat()
    }


# ============================================================
# CHAT ENDPOINT
# ============================================================

@app.post("/chat")
def chat(request: ChatRequest):

    message = request.message.strip()


    if not message:

        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )


    logger.info(
        "User request received"
    )


    try:

        answer = run_agent(
            message
        )


        logger.info(
            "Request completed successfully"
        )


        return {

            "success": True,

            "answer": str(answer),

            "timestamp":
                datetime.now().isoformat()

        }


    except Exception as error:

        logger.exception(
            "Agent processing failed"
        )


        raise HTTPException(

            status_code=500,

            detail=(
                "The AI agent could not "
                "process your request."
            )

        )


# ============================================================
# SERVER
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("                 MY AI AGENT")
    print("=" * 60)
    print()
    print("Open:")
    print(
        f"http://{HOST}:{PORT}"
    )
    print()
    print("Press CTRL+C to stop.")
    print("=" * 60)
    print()


    uvicorn.run(
        app,
        host=HOST,
        port=PORT
    )