import MessageBubble from './MessageBubble';

const ChatBox = ({ chatHistory, query, setQuery, handleSubmit }) => {
  return (
    <div className="chat-container">
      <div className="chat-history">
        {chatHistory.map((msg, idx) => (
          <MessageBubble key={idx} sender={msg.sender} text={msg.text} />
        ))}
      </div>

      <form onSubmit={handleSubmit} className="chat-input">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Type your message..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
};

export default ChatBox;