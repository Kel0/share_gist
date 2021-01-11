import React, { useState } from 'react';

import { apiWrapper }  from "./api/apiWrapper";


const App = () => {
    const [query, setQuery] = useState('');

    const doRequest = async () => {
        const data = await apiWrapper("lexers");
        console.log(data);
    }

    return (
        <div className="main-container">
            <button
                type="text"
                className="doRequest"
                value={query}
                onClick={doRequest}
            >
                Click me
            </button>
        </div>
    );
}

export default App;