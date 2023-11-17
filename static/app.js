const guessForm = document.querySelector('#guess-form')

let guessedWords = [];

guessForm.addEventListener('submit', function (e) {
    e.preventDefault()
    let guessInput = document.querySelector('#guess')
    let guess = guessInput.value
    axios.post('/guess', { 'guess': guess })
        .then(function (response) {
            returnGuessMessage(response);
            checkIfWordGuessed(guess, response);
        })
    guessInput.value = '';
})

function returnGuessMessage(response) {
    const message = response.data.message;
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = message;
}

function checkIfWordGuessed(guess, response) {
    if (!guessedWords.includes(guess)) {
        if (response.data.result === 'ok') {
            let points = guess.length
            let score = updateScore(points);
            document.querySelector('#score').textContent = score;
            guessedWords.push(guess);
        }
    }
    else {
        const messageDiv = document.getElementById('message');
        messageDiv.textContent = 'You guessed this word already';
    }
}

function updateScore(points) {
    let score = parseInt(document.querySelector('#score').textContent);
    score += points;
    return score;
}

