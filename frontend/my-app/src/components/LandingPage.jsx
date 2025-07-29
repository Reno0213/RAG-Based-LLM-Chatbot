const LandingPage = ({query, setQuery, handleSubmit}) => {
    return (
        <>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={query}
                    onChange={e => setQuery(e.target.value)}
                    placeholder="Ask LoLBot..."
                />
                <button type="submit">Submit</button>
            </form>
        </>
    );
};

export default LandingPage;