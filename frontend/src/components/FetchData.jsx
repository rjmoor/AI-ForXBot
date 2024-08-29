import React, { useEffect, useState } from 'react';
import axios from 'axios';

function FetchData() {
    const [data, setData] = useState(null);

    useEffect(() => {
        axios.get('http://localhost:5000/api/some-endpoint')
            .then(response => setData(response.data))
            .catch(error => console.error('Error fetching data:', error));
    }, []);

    return (
        <div>
            <h1>Data from API:</h1>
            <pre>{JSON.stringify(data, null, 2)}</pre>
        </div>
    );
}

export default FetchData;
