import React from 'react';

function MessageBubble({ message }) {
  const isUser = message.sender === 'User';
  
  return (
    <div className={`message-wrapper ${isUser ? 'User' : 'Cortana'}`}>
      <div className="message-bubble">
        {message.text}
      </div>
    </div>
  );
}

export default MessageBubble;