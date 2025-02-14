import React, {useEffect, useState} from 'react';
import axios from 'axios';


const Prompt = ({onEssaySubmit}) => {
    const [prompt, setPrompt] = useState('');
    const [essay, setEssay] = useState('');

    useEffect(() => {
        //Fetch a random prompt from the backend
        axios.get('http://127.0.0.1:5000/get-prompt')
        .then(response => setPrompt(response.data.prompt))
        .catch(error => console.error(error));
    }, []);

    const handleSubmit = () => {
        onEssaySubmit(essay);
    };

    return (
        <div className="prompt-card">
            <h2>IELTS Writing Task 2</h2>
            <p>{prompt}</p>
            <textarea
                value={essay}
                onChange={(e) => setEssay(e.target.value)}
                placeholder="Write your essay here..."
            />
        <button onClick={handleSubmit}>Submit Essay</button>
    </div>
    );
};

export default Prompt;