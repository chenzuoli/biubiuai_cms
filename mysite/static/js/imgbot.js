// 请求https://api.stability.ai，获取response（image结果），参数为prompt提示词

const imgbotForm = document.querySelector("#imgbot-form");
const imgbotInput = document.querySelector("#imgbot-input");
const imgbotHistory = document.querySelector("#imgbot-history");
// const base_url = "http://localhost:8000"
const base_url = "http://43.153.96.195"

imgbotForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const userMessage = "You: " + imgbotInput.value;

    // generate imgbot response based on user input
    getImgbotResponse(userMessage);

    // display the user message in the imgbot history
    const messageContainer = document.createElement("div");
    const userMessageElement = document.createElement("p");
    userMessageElement.classList.add("user-message");
    userMessageElement.textContent = userMessage;
    messageContainer.appendChild(userMessageElement);
    imgbotHistory.appendChild(messageContainer);

    // display AI img in the imgbot history
    const imgbotResponse = "AI: ";
    const imgbotResponseElement = document.createElement("p");
    imgbotResponseElement.classList.add("imgbot-message");
    imgbotResponseElement.textContent = imgbotResponse;
    messageContainer.appendChild(imgbotResponseElement);
    imgbotHistory.appendChild(messageContainer);

    // clear the input field for the next message
    imgbotInput.value = "";

});



function getImgbotResponse(userMessage) {
    let response = "";
    // request stability.ai, parameter: prompt
    let request_api = '/text_to_image/'
    fetch(base_url + request_api, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ "image_prompt": userMessage }),
    }).then((response) => {
        console.log(response);
        return response.json();
    }).then((data) => {
        response = data.img_path;
        displayImgResponse(response);
    }).catch((error) => {
        console.error(error);
        console.log("error");
    });
    console.log(response)
    return response;

}


// 当聊天记录占满chatbot时，进行滚动，利用DIV的scrollIntoView方法，将最底端滚动到可视位置
function scrollImgbot() {
    imgbotHistory.scrollIntoView(false);
  }
  

// Define a function named displayImgResponse that takes a parameter named `path`
// This function will display the image response in the imgbot history by creating a message container, user message element, imgbot response element, and appending them to the imgbot history
// The imgbot response element will have its src attribute set to the image response URL obtained by using the `path` parameter
// The function will be called by passing the `path` parameter obtained from the response of the fetch request in the getImgbotResponse function

function displayImgResponse(img_path) {
    // display img
    const messageContainer = document.createElement("div");
    const imgbotResponseElement = document.createElement("img");
    imgbotResponseElement.classList.add("imgbot-message");
    imgbotResponseElement.src = base_url + img_path;
    messageContainer.appendChild(imgbotResponseElement);
    imgbotHistory.appendChild(messageContainer);

    // add a line break to separate messages
    const lineBreak = document.createElement("br");
    imgbotHistory.appendChild(lineBreak);

    // clear the user input field
    imgbotInput.value = '';

    // scroll to the bottom of the chatbot history
    scrollChatbot();
}
