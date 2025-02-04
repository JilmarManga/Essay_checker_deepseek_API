import React from 'react';

const Evaluation = ({evaluation}) => {
    if (!evaluation) return null;

    return (
        <div>
            <h2>Evaluation Results</h2>
            <p><strong>Band Score:</strong> {evaluation.bandScore}</p>
            <p><strong>Feedback:</strong> {evaluation.feedback}</p>
        </div>
    );
};

export default Evaluation