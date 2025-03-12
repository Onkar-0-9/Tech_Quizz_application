let currentQuestionIndex = 0;
let score = 0;
let totalQuestions = 0;

function startQuiz() {
    // Reset quiz state
    currentQuestionIndex = 0;
    score = 0;
    document.getElementById('quiz-screen').style.display = 'block';
    document.getElementById('start-screen').style.display = 'none';
    loadQuestion();
}

function loadQuestion() {
    fetch('/get_question')
        .then(response => response.json())
        .then(data => {
            console.log('Question data:', data); // Debug log
            
            if (data.error) {
                if (data.error === 'Quiz completed') {
                    endQuiz();
                    return;
                }
                document.getElementById('question').innerText = data.error;
                return;
            }

            // Display question and options
            document.getElementById('question').innerText = data.question;
            const optionsContainer = document.getElementById('options');
            optionsContainer.innerHTML = '';

            data.options.forEach((option, index) => {
                const button = document.createElement('button');
                button.className = 'option-btn';
                button.innerText = option;
                button.onclick = () => selectOption(button, option);
                optionsContainer.appendChild(button);
            });

            // Update progress
            document.getElementById('current-question').innerText = data.index + 1;
            document.getElementById('total-questions').innerText = data.total_questions;
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('question').innerText = 'Error loading question';
        });
}

function selectOption(button, answer) {
    // Remove previous selections
    document.querySelectorAll('.option-btn').forEach(btn => {
        btn.classList.remove('selected');
    });
    
    // Mark this option as selected
    button.classList.add('selected');
    
    // Enable submit button
    const submitBtn = document.getElementById('submit-btn');
    submitBtn.disabled = false;
    submitBtn.onclick = () => submitAnswer(answer);
}

function submitAnswer(answer) {
    const question = document.getElementById('question').innerText;
    
    fetch('/submit_answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            question: question,
            answer: answer
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            score++;
            document.getElementById('score').innerText = score;
        }
        // Load next question
        loadQuestion();
    })
    .catch(error => console.error('Error:', error));
}

function endQuiz() {
    document.getElementById('quiz-screen').style.display = 'none';
    const resultsDiv = document.getElementById('results');
    resultsDiv.style.display = 'block';
    resultsDiv.innerHTML = `
        <h2>Quiz Completed!</h2>
        <p>Your final score: ${score}</p>
        <button onclick="location.reload()">Try Again</button>
    `;
}

// Make sure submit button is visible and working
document.addEventListener('DOMContentLoaded', () => {
    const submitBtn = document.getElementById('submit-btn');
    if (submitBtn) {
        submitBtn.onclick = submitAnswer;
    }
});
