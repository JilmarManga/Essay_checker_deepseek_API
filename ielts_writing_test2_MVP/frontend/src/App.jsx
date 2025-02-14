import React, { useState } from 'react';
import axios from 'axios';
import Prompt from './components/Prompt.jsx';
import Evaluation from './components/Evaluation.jsx';

const App = () => {
    const [evaluation, setEvaluation] = useState(null);

    const handleEssaySubmit = (essay) => {
        console.log('Submit button clicked') //Debugging line
        axios.post('http://127.0.0.1:5000//evaluate-essay', { essay })
        .then(response => setEvaluation(response.data))
        .catch(error => console.error(error));
    };

    return (
        <div className="container">
            <h1>IELTS Writing Practice</h1>
            <Prompt onEssaySubmit={handleEssaySubmit} />
            {evaluation && <Evaluation evaluation={evaluation} />}
        </div>
    );
};

export default App;
