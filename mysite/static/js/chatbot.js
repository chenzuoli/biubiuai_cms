const chatbotForm = document.querySelector("#chatbot-form");
const chatbotInput = document.querySelector("#chatbot-input");
const chatbotHistory = document.querySelector("#chatbot-history");

chatbotForm.addEventListener("submit", function(e) {
  e.preventDefault();
  const userMessage = chatbotInput.value;
  
  // generate chatbot response based on user input
  const chatbotResponse = getChatbotResponse(userMessage);
  
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
});

function getChatbotResponse(userMessage) {
  // generate chatbot response based on user input
  let response = "";
  if (userMessage.toLowerCase().includes("hello")) {
    response = "Hi there!";
  } else {
    response = "I'm sorry, I don't understand.";
  }
  return response;
}