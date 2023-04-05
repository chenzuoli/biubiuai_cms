// import { OpenAI } from "./openai.js";
// const openai = new OpenAI(process.env.OPENAI_API_KEY);

// import { Configuration, OpenAIApi } from "../node_modules/openai";
// const configuration = new Configuration({
//   apiKey: process.env.OPENAI_API_KEY,
// });
// const openai = new OpenAIApi(configuration);


const chatbotForm = document.querySelector("#chatbot-form");
const chatbotInput = document.querySelector("#chatbot-input");
const chatbotHistory = document.querySelector("#chatbot-history");
let chatTextHistory = "";


function getChatbotResponse(userMessage, chatTextHistory) {
  // generate chatbot response based on user input
  let response = "";
  // request to openai api to get response, use OPENAI_API_KEY environment variable to store the key
  const prompt = "You: " + userMessage
  // const gptResponse = openai.complete({
  //   engine: "davinci",
  //   prompt: prompt,
  //   maxTokens: 100,
  //   temperature: 0.7,
  //   topP: 1,
  //   presencePenalty: 0,
  //   frequencyPenalty: 0,
  //   bestOf: 1,
  //   n: 1,
  //   stream: false,
  //   stop: ["\n", "AI:"],
  // });
  // response = gptResponse.data.choices[0].text;
  // request to 43.153.35.39:3080 to get response, add parameter "userMessage" to the request, don't use axios
  // const xhr = new XMLHttpRequest();
  // xhr.open("POST", "http://43.153.35.39:3080/");
  // xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  // xhr.onload = function () {
  //   if (xhr.status === 200) {
  //     response = xhr.responseText;
  //     displayResponse(response);
  //   } else {
  //     console.log("Request failed.  Returned status of " + xhr.status);
  //   }
  // };
  // xhr.send(JSON.stringify({ message: userMessage }));

  // use "fetch" to request 43.153.35.39:3080 to get response add parameter "userMessage"
  fetch("http://43.153.35.39/chatgpt/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message: userMessage, basePromptPrefix: chatTextHistory }),
  })
    .then((response) => response.json())
    .then((data) => {
      response = data.message;
      displayResponse(response);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
  return response;
}

// 当聊天记录占满chatbot时，进行滚动，利用DIV的scrollIntoView方法，将最底端滚动到可视位置
function scrollChatbot() {
  const chatbotHistory = document.querySelector("#chatbot-history");
  chatbotHistory.scrollIntoView(false);
}


// display the response from the ChatGPT API
function displayResponse(response) {
  // display the user input
  const userInput = document.getElementById("chatbot-input").value.trim();
  const userMessage = document.createElement("div");
  userMessage.classList.add("message", "user-message");
  userMessage.innerHTML = `<div class="message-text">${userInput}</div>`;
  document.getElementById("chatbot-history").appendChild(userMessage);

  // display the ChatGPT response
  const chatbotResponse = document.createElement("div");
  chatbotResponse.classList.add("message", "chatbot-message");
  chatbotResponse.innerHTML = `<div class="message-text">${response}</div>`;
  document.getElementById("chatbot-history").appendChild(chatbotResponse);

  // clear the user input field
  document.getElementById("chatbot-input").value = '';

  // scroll to the bottom of the chatbot history
  scrollChatbot();
}

// scroll to the bottom of the chatbot history
// function scrollChatbot() {
//   const chatbotHistory = document.getElementById("chatbot-history");
//   chatbotHistory.scrollTop = chatbotHistory.scrollHeight;
// }

// select the role for the ChatGPT API
function selectRole() {
  const chatgptRole = document.querySelector("input[name='chatgpt-role']:checked").value;
  const chatbotHistory = document.getElementById("chatbot-history");

  // clear the chatbot history
  while (chatbotHistory.firstChild) {
    chatbotHistory.removeChild(chatbotHistory.firstChild);
  }
}

chatbotForm.addEventListener("submit", function (e) {
  e.preventDefault();
  const userMessage = "You: " + chatbotInput.value;

  // generate chatbot response based on user input
  const chatbotResponse = "AI: " + getChatbotResponse(userMessage, chatTextHistory);

  // add user message and chatbot response to chat history
  chatTextHistory += userMessage + "\n" + chatbotResponse + "\n";

  // append user message and chatbot response to chat history
  const messageContainer = document.createElement("div");
  messageContainer.classList.add("message-container");
  const userMessageElement = document.createElement("p");
  userMessageElement.classList.add("user-message");
  userMessageElement.textContent = userMessage;
  messageContainer.appendChild(userMessageElement);
  const chatbotResponseElement = document.createElement("p");
  chatbotResponseElement.classList.add("chatbot-message");
  chatbotResponseElement.textContent = chatbotResponse;
  messageContainer.appendChild(chatbotResponseElement);
  chatbotHistory.appendChild(messageContainer);

  // clear the input field for the next message
  chatbotInput.value = "";

  // scroll to the bottom of the chatbot history
  scrollChatbot();
});


