import React, { useState } from 'react';
import axios from 'axios';
import Prompt from './components/Prompt.jsx';
import Evaluation from './components/Evaluation.jsx';

const App = () => {
    const [evaluation, setEvaluation] = useState(null);

    /*const handleEssaySubmit = (essay) => {
        console.log('Submit button clicked') //Debugging line
        axios.post('http://127.0.0.1:5000//evaluate-essay', { essay })
        .then(response => setEvaluation(response.data))
        .catch(error => console.error(error));
    };*/

    const handleEssaySubmit = (essay) => {
    axios.post('http://127.0.0.1:5000/evaluate-essay', { essay })
        .then(response => {
            console.log("Evaluation:", response.data);
            setEvaluation(response.data);
        })
        .catch(error => {
            console.error("Error evaluating essay:", error);
        });
    };

    return (
        <div className="min-h-screen bg-gray-100 py-8">
            <div className='max-w-4xl mx-auto px-4'>
            <h1 className='text-4xl font-bold text-center text-blue-600 mb-8'>
                IELTS Writing Practice
            </h1>
            <Prompt onEssaySubmit={handleEssaySubmit} />
            {evaluation && <Evaluation evaluation={evaluation} />}
            </div>
        </div>
    );
};

export default App;
