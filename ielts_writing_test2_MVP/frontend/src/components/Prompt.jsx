import React, {useEffect, useState, useCallback} from 'react';
import axios from 'axios';


const Prompt = ({ onEssaySubmit }) => {
    const [prompt, setPrompt] = useState('');
    const [essay, setEssay] = useState('');
    const [isSubmiting, setIsSubmiting] = useState(false); // New state

    useEffect(() => {
        //Fetch a random prompt from the backend
        console.log('Fetching prompt') //Debugging line;
        axios.get('http://127.0.0.1:5000/get-prompt')
        .then(response => setPrompt(response.data.prompt))
        .catch(error => console.error(error));
    }, []);

    const handleSubmit = useCallback(() => {
        if (isSubmiting) return; //Prevent multiple submissions
        console.log('Submit button clicked') //Debugging line;
        setIsSubmiting(true); //Disable the submit button
        onEssaySubmit(essay);
    }, [isSubmiting, onEssaySubmit, essay]);

    return (
        <div className="prompt-card">
            <h2>IELTS Writing Task 2</h2>
            <p>{prompt}</p>
            <textarea
                value={essay}
                onChange={(e) => setEssay(e.target.value)}
                placeholder="Write your essay here..."
            />
        <button onClick={handleSubmit} disabled={isSubmiting}>
            {isSubmiting ? 'Submitted' : 'Submit Essay'}
        </button>
    </div>
    );
};

export default Prompt;

