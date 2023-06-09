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

  // use "fetch" to request 43.153.96.195 to get response add parameter "userMessage"
  console.log("user message: " + userMessage)
  // 通过前端页面选择的角色，来设置fetch的接口名称
  // 获取id=chatgpt-role的select标签，然后获取其选中的option的value值
  let chatgptRole = document.getElementById("chatgpt-role").value;
  console.log("chatgptRole: " + chatgptRole)

  let openapi;
  switch (chatgptRole) {
    case "chatgpt":
      openapi = "/chatgpt/";
      break;
    case "qa_gpt":
      openapi = "/qa_gpt/";
      break;
    case "grammar_correction_gpt":
      openapi = "/grammar_correction_gpt/";
      break;
    case "summarizer_gpt":
      openapi = "/summarizer_gpt/";
      break;
    case "text_to_command":
      openapi = "/text_to_command/";
      break;
    case "text_to_code":
      openapi = "/text_to_code/";
      break;
    case "text_to_sql":
      openapi = "/text_to_sql/";
      break;
    case "customer_gpt":
      openapi = "/customer_gpt/";
      break;
    case "storyteller":
      openapi = "/storyteller/";
      break;
    case "translator":
      openapi = "/translator/";
      break;
    case "teacher_gpt":
      openapi = "/teacher_gpt/";
      break;
    case "lawyer":
      openapi = "/lawyer/";
      break;
    case "doctor":
      openapi = "/doctor/";
      break;
    case "engineer":
      openapi = "/engineer/";
      break;
    case "salesman":
      openapi = "/salesman/";
      break;
    case "police":
      openapi = "/police/";
      break;
    case "journalist":
      openapi = "/journalist/";
      break;
    case "nurse":
      openapi = "/nurse/";
      break;
    case "artist":
      openapi = "/artist/";
      break;
    case "musician":
      openapi = "/musician/";
      break;
    case "chef":
      openapi = "/chef/";
      break;
    default:
      "/chatgpt/";
  }
  fetch("http://43.153.96.195" + openapi, {
    // fetch("http://127.0.0.1:8000" + openapi, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ "message": userMessage, "basePrefixPrompt": chatTextHistory }),
  })
    .then((response) => response.json())
    .then((data) => {
      response = data.message;
      displayResponse(response);
    })
    .catch((error) => {
      console.error(error);
      console.log("error");
      //console.error("Error:", error);
    });
  return response;
}

// 当聊天记录占满chatbot时，进行滚动，利用DIV的scrollIntoView方法，将最底端滚动到可视位置
function scrollChatbot() {
  const chatbotHistory = document.querySelector("#chatbot-history");
  chatbotHistory.scrollIntoView(false);
}


// display the response from the ChatGPT API， 缓慢显示响应结果，利用setInterval方法，每隔一段时间显示一部分
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
  const messageText = document.createElement("div");
  messageText.classList.add("message-text");
  chatbotResponse.appendChild(messageText);
  document.getElementById("chatbot-history").appendChild(chatbotResponse);

  // add a line break to separate messages
  const lineBreak = document.createElement("br");
  document.getElementById("chatbot-history").appendChild(lineBreak);

  // add background color to the chatbot response
  chatbotResponse.style.backgroundColor = "#F5F5F5";

  // clear the user input field
  document.getElementById("chatbot-input").value = '';

  // scroll to the bottom of the chatbot history
  scrollChatbot();

  // use setInterval to display the response slowly
  let i = 0;
  const intervalId = setInterval(() => {
    if (i >= response.length) {
      clearInterval(intervalId);
      return;
    }
    messageText.innerHTML += response.charAt(i);
    i++;
  }, 50);
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