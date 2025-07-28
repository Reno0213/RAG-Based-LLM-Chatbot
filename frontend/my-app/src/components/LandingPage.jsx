import React from "react";
import logo from "../assets/logo.png";

function LandingPage({ query, setQuery, handleSubmit }) {
  return (
    <div className="landing-container">
      <img src={logo} alt="Logo" className="logo" />
      <form onSubmit={handleSubmit} className="landing-form">
        <input
          type="text"
          placeholder="Ask something..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="search-input"
        />
        <button type="submit" className="search-button">Ask</button>
      </form>
    </div>
  );
}

export default LandingPage;