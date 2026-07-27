

function ChatBar({sendMessage}){
  

  return (
    <>
      <div className="input-container">
          <input placeholder="Enter message"className='chat-bar' type="text"></input>
          <button className="send-button" onClick={sendMessage}>Enter</button>
      </div>
    </>
  );
}

export default ChatBar