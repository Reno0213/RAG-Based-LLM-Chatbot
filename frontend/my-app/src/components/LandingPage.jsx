import logo from '../assets/logo.png';

const LandingPage = ({query, setQuery, handleSubmit}) => {
    return (
        <>
        <div className="logo central">
            <img src={logo} alt="LoLBot logo" />
        </div>
            <form onSubmit={handleSubmit}>
                <input className="search-form"
                    type="text"
                    value={query}
                    onChange={e => setQuery(e.target.value)}
                    placeholder="Ask LoLBot..."
                />
                <button className="search-form button" type="submit">Submit</button>
            </form>
        </>
    );
};

export default LandingPage;