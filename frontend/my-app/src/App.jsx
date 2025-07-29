import { useState } from 'react'
import axios from 'axios'
import LandingPage from './components/LandingPage'
import ChatBox from './components/ChatBox'
import './index.css'

const App = () => {

  const [query, setQuery] = useState("");
  const [isChatView, setIsChatView] = useState(true);
  const [chatHistory, setChatHistory] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const url = "/chat"

    //Append initial query to chat history
    setChatHistory(prev => [...prev, { sender: 'user', text: query }]);
    try {
      const res = await axios.post(
        url,
        { query });
      const response = res.data.response;
      setChatHistory(prev => [...prev, { sender: 'bot', text: response }]);

      if (!isChatView) {
        setIsChatView(true);
      }
      setQuery("");

    } catch (err) {
      console.error("API error", err)
      setChatHistory(prev => [...prev, { sender: bot, text: "Error: could not get a response" }]);
    }
  };

  return (
    <>
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
    </>
  );
}

export default App;