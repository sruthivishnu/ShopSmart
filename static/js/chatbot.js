const chatbotButton =
document.getElementById("chatbot-button");

const chatbotWindow =
document.getElementById("chatbot-window");

const chatClose =
document.getElementById("chat-close");

const sendBtn =
document.getElementById("send-btn");

const chatInput =
document.getElementById("chat-input");

const chatMessages =
document.getElementById("chatbot-messages");

chatbotButton.addEventListener(
    "click",
    () => {

        chatbotWindow.style.display = "flex";

    }
);

chatClose.addEventListener(
    "click",
    () => {

        chatbotWindow.style.display = "none";

    }
);
sendBtn.addEventListener(
    "click",
    sendMessage
);

// -----------------------------------------
// SEND MESSAGE ON ENTER KEY
// -----------------------------------------

chatInput.addEventListener(
    "keydown",
    function(event){

        if(event.key === "Enter"){

            event.preventDefault();

            sendMessage();

        }

    }
);

function sendMessage(){

    if(sendBtn.disabled){

        return;

    }

    const message =
    chatInput.value.trim();

    if(message === ""){

        return;

    }

    chatMessages.innerHTML +=
    `<div>
        <b>You:</b>
        ${message}
    </div>`;

    chatInput.value = "";

    chatMessages.innerHTML +=
    `<div id="typing-indicator">
        <b>Bot:</b>
        Thinking...
    </div>`;

    sendBtn.disabled = true;

    fetch(
        "/chat",
        {

            method:"POST",

            headers:{

                "Content-Type":
                "application/json"

            },

            body:JSON.stringify({

                message:message

            })

        }
    )

    .then(
        response => response.json()
    )

    .then(
    data => {

        document
            .getElementById("typing-indicator")
            ?.remove();

        chatMessages.innerHTML +=
        `<div>
            <b>Bot:</b>
            ${data.reply}
        </div>`;

        sendBtn.disabled = false;

        chatMessages.scrollTop =
        chatMessages.scrollHeight;

    }
);

}