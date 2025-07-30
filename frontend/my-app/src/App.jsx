import { useState } from 'react'
import { useRef } from 'react'
import axios from 'axios'
import LandingPage from './components/LandingPage'
import ChatBox from './components/ChatBox'
import MessageBubble from './components/MessageBubble'

const App = () => {

  const [query, setQuery] = useState("");
  const [isChatView, setIsChatView] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);
  const nextMsgId = useRef(1);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const url = "http://127.0.0.1:8000/chat";

    const id = nextMsgId.current;
    nextMsgId.current += 1;
    //Append initial query to chat history
    setChatHistory(prev => [...prev, { id, sender: 'user', text: query }]);
    try {
      const res = await axios.post(
        url,
        { query });
      const response = res.data.response;

      const botMsgID = nextMsgId.current;
      nextMsgId.current += 1;
      setChatHistory(prev => [...prev, { id: botMsgID, sender: 'bot', text: response }]);

      if (!isChatView) {
        setIsChatView(true);
      }
      setQuery("");

    } catch (err) {
      console.error("API error", err)
      setChatHistory(prev => [...prev, { sender: bot, text: "Error: could not get a response" }]);
    }
  };

  const testMode = false;
  if (testMode) {
    return (
      <div style={{ padding: '1rem' }}>
        <h2>Testing MessageBubble</h2>
        <MessageBubble sender="user" text="This is a user message" />
        <MessageBubble sender="bot" text="This is a bot message" />
      </div>
    );
  }

  return (
    <>
    <div className="app-container">
      {isChatView ? (
        <ChatBox
          chatHistory={chatHistory}
          query={query}
          setQuery={setQuery}
          handleSubmit={handleSubmit}
        />
      ) : (
        <LandingPage
          query={query}
          setQuery={setQuery}
          handleSubmit={handleSubmit}
        />
      )}
      </div>
      </>
  );
}

export default App;