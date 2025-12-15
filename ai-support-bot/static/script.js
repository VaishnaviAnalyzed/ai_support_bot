document.addEventListener('DOMContentLoaded', () => {
    const chatContainer = document.getElementById('chat-container');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const newChatBtn = document.getElementById('new-chat-btn');

    // Default welcome message
    const welcomeMessage = `
        <div class="message bot-message">
            <div class="avatar">🤖</div>
            <div class="message-content">
                <p>Hello! I'm your AI Support Assistant. I can help with refunds, shipping, product details, and more. How can I help you today?</p>
                <span class="timestamp">Just now</span>
            </div>
        </div>
    `;

    // New Chat Functionality
    if (newChatBtn) {
        newChatBtn.addEventListener('click', () => {
            chatContainer.innerHTML = welcomeMessage;
            userInput.value = '';
            userInput.focus();
            sendBtn.disabled = true;
        });
    }

    // Auto-scroll to bottom of chat
    const scrollToBottom = () => {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    };

    // Helper to format time
    const getTime = () => {
        return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    };

    // Add a message to the UI
    const addMessage = (text, sender, intent = null) => {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');

        const avatarDiv = document.createElement('div');
        avatarDiv.classList.add('avatar');
        avatarDiv.textContent = sender === 'user' ? '👤' : '🤖';

        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');

        // Optional Intent Badge for Bot
        let intentHtml = '';
        if (intent && sender === 'bot') {
            intentHtml = `<span class="intent-badge">${intent}</span>`;
        }
        
        // Remove [IntentName] prefix if existing in text to redundant display
        let displayText = text;
        if (sender === 'bot' && intent && text.startsWith(`[${intent}]`)) {
             displayText = text.substring(intent.length + 2).trim();
        }

        contentDiv.innerHTML = `
            ${intentHtml}
            <p>${displayText}</p>
            <span class="timestamp">${getTime()}</span>
        `;

        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(contentDiv);
        chatContainer.appendChild(messageDiv);
        
        scrollToBottom();
    };

    // Enable/Disable button based on input
    userInput.addEventListener('input', () => {
        sendBtn.disabled = userInput.value.trim() === '';
    });

    // Handle Sending Message
    const sendMessage = async () => {
        const text = userInput.value.trim();
        if (!text) return;

        // UI Update
        addMessage(text, 'user');
        userInput.value = '';
        sendBtn.disabled = true;

        // Show typing indicator? (Simplified: just wait)
        
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: text })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            
            // Artificial delay for realism
            // setTimeout(() => {
                addMessage(data.response, 'bot', data.intent);
            // }, 500);
            
        } catch (error) {
            console.error('Error:', error);
            addMessage("I'm sorry, I'm having trouble connecting to the server. Please try again later.", 'bot');
        }
    };

    sendBtn.addEventListener('click', sendMessage);

    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});
