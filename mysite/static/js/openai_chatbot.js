const chatbot = {
    API_URL: 'https://api.openai.com/v1/engine/davinci-codex/completions',
    API_KEY: process.env.OPENAI_API_KEY,
  
    // initialize the chatbot
    init: function() {
      // add event listeners for user input and role selection
      document.getElementById("send-btn").addEventListener("click", chatbot.send);
      document.querySelector("input[name='chatgpt-role']").addEventListener("change", chatbot.selectRole);
  
      // make an initial request to the ChatGPT API to start the conversation
      axios.post(chatbot.API_URL, {
        prompt: 'Hello, can you help me?',
        max_tokens: 1024,
        temperature: 0.7,
        n: 1,
        stop: '\n'
      }, {
        headers: {
          'Authorization': `Bearer ${chatbot.API_KEY}`,
          'Content-Type': 'application/json'
        }
      })
      .then(function(response) {
        chatbot.displayResponse(response.data.choices[0].text);
      })
      .catch(function(error) {
        console.error(error);
      });
    },
  
    // send user input to the ChatGPT API and display the response
    send: function() {
      const userInput = document.getElementById("user-input").value.trim();
      if (userInput === '') return;
  
      const chatgptRole = document.querySelector("input[name='chatgpt-role']:checked").value;
      const prompt = `As a ${chatgptRole}, ${userInput}`;
      if (chatgptRole === 'customer') {
        prompt += '\nAI: ';
      }
  
      axios.post(chatbot.API_URL, {
        prompt: prompt,
        max_tokens: 1024,
        temperature: 0.7,
        n: 1,
        stop: '\n'
      }, {
        headers: {
          'Authorization': `Bearer ${chatbot.API_KEY}`,
          'Content-Type': 'application/json'
        }
      })
      .then(function(response) {
        chatbot.displayResponse(response.data.choices[0].text);
      })
      .catch(function(error) {
        console.error(error);
      });
  
      // reset the input field
      document.getElementById("user-input").value = '';
    },
  
    // display the response from the ChatGPT API
    displayResponse: function(responseText) {
      const messagesContainer = document.getElementById("messages");
      const message = '<div class="message"><span class="bot">AI:</span> ' + responseText + '</div>';
      messagesContainer.innerHTML += message;
  
      // scroll the chat to the latest message
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    },
  
    // update the prompt based on the selected chatgpt role
    selectRole: function() {
      const selectedRole = document.querySelector("input[name='chatgpt-role']:checked").value;
      const inputField = document.getElementById("user-input");
  
      if (selectedRole === 'storyteller') {
        // add a prompt for the storyteller role
        inputField.placeholder = 'Enter the beginning of a story...';
      } else {
        // remove the prompt for the customer role
        inputField.placeholder = '';
      }
    }
  };
  
  // initialize the chatbot
  chatbot.init();