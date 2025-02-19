import React from 'react';

const Evaluation = ({evaluation}) => {
    if (!evaluation) return null;

    return (
        <div className="evaluation-card">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">
            Evaluation Results
            </h2>
            <p className="text-gray-700 mb-6">
                <strong>Band Score:</strong> {evaluation.bandScore}
            </p>
            <div className="space-y-4">
                <div>
                    <h3 className="text-xl font-semibold text-gray-800">Task Achievement/Response</h3>
                    <p className="text-gray-600">{evaluation.feedback.taskAchievement}</p>
                </div>
                <div>
                    <h3 className="text-xl font-semibold text-gray-800">Coherence and Cohesion</h3>
                    <p className="text-gray-600">{evaluation.feedback.coherenceAndCohesion}</p>
                </div>
                <div>
                    <h3 className="text-xl font-semibold text-gray-800">Lexical Resource</h3>
                    <p className="text-gray-600">{evaluation.feedback.lexicalResource}</p>
                </div>
                <div>
                    <h3 className="text-xl font-semibold text-gray-800">Grammatical Range and Accuracy</h3>
                    <p className="text-gray-600">{evaluation.feedback.grammaticalRangeAndAccuracy}</p>
                </div>
                <div>
                    <h3 className="text-xl font-semibold text-gray-800">Conclusion</h3>
                    <p className="text-gray-600">{evaluation.feedback.conclusion}</p>
                </div>
            </div>
        </div>
    );
};

export default Evaluation