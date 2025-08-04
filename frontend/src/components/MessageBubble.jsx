const MessageBubble = ({ sender, text }) => {
  const isUser = sender === 'user';

  return (
    <div className={`message-bubble ${isUser ? 'user' : 'bot'}`}>
      <p>{text}</p>
    </div>
  );
};

export default MessageBubble;