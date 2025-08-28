const messageInput = document.querySelector('.message-input');
const chatBody = document.querySelector('.chat-body');
const creatMessageElement = (content, classes) => {
    const div = document.createElement('div');
    div.classList.add('message', classes);
    div.innerHTML = content;
    return div;
}
const handleOutgoingMessage = (userMessage) => {
    const messageContent = '<div class="outgoing-message">${userMessage}</div>';
    const outgoingMessageDiv = creatMessageElement(messageContent, "user-message");
    chatBody.appendChild(outgoingMessageDiv);
    messageInput.addEventListener('keydown', (e) => {
        const userMessage = e.target.value.trim();
        if (e.key === 'Enter' && userMessage) {
            handleOutgoingMessage(userMessage);

        }
    })
};