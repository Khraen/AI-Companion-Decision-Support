import React, { useEffect, useRef } from 'react';
import MessageBubble from './MessageBubble';

function MessageBoxContainer({ messages, isLoading }) {
  const containerRef = useRef(null);

  // Auto-scroll to the bottom whenever a new message arrives
  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="message-box-container" ref={containerRef}>
      {messages.map((msg) => (
        <MessageBubble key={msg.id} message={msg} />
      ))}
      {/* Conditionally show typing indicator when waiting on API */}
      {isLoading && (
        <div className="message-bubble bot loading">
          <span className="dot">.</span>
          <span className="dot">.</span>
          <span className="dot">.</span>
        </div>
      )}
    </div>
  );
}

export default MessageBoxContainer;