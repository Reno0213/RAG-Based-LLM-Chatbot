import './searchbar.css'
import logo from "./assets/logo.png"
function App() {
  return (
    <div className="app-container">
      <img src={logo} alt="Logo" id="logo"></img>
      <form className="search-form">
        <input
          type="text"
          placeholder="Ask a question..."
        />
        <button type="submit">Search</button>
      </form>
    </div>
  );
}

export default App;