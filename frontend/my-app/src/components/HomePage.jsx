import { useState } from 'react';
import axios from 'axios';

const HomePage = () => {

    url = "/chat"

    const [query, setQuery] = useState("")
    const [response, setResponse] = useState("")

    const handleSubmit = async (e) => {
        e.preventDefault();
        try{
            const res = await axios.post(
                url, 
                {query});
            setResponse(res.data.response);
        } catch {
            console.error("API error", err)
            setResponse("There was an error with your request");
        }
    };

    return (
        <>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={query}
                    onChange={e => setQuery(e.target.value)}
                />
                <button type="submit">Submit</button>
            </form>
        </>
    );
};