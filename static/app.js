let guessedWords = [];
let game = 'on'

const startButton = document.querySelector('#start-btn');
if (startButton) {
    startButton.addEventListener('click', function () {
        const redirectTo = 'http://127.0.0.1:5000/game';
        window.location.href = redirectTo;
    })
}

const guessForm = document.querySelector('#guess-form')
if (guessForm) {
    if (game === 'on') {
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
    }
    else {
        guessForm.removeEventListener();
    }
}

let timer = document.querySelector('#timer')

function updateTimer() {
    let time = parseInt(timer.textContent);
    if (game === 'on') {
        if (time === 0) {
            game = 'off'
            endGame();
        }
        else {
            time--;
            timer.textContent = time;
        }
    }
}


if (timer) {
    setInterval(updateTimer, 1000);
}


function returnGuessMessage(response) {
    const message = response.data.message;
    const messageDiv = document.getElementById('message');
    if (game === 'on') {
        messageDiv.textContent = message;
    }
    else {
        endGame();
    }
}

function checkIfWordGuessed(guess, response) {
    if (!guessedWords.includes(guess)) {
        if (response.data.result === 'ok') {
            let points = guess.length
            updateScore(points);
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
    document.querySelector('#score').textContent = score;
    let highScore = parseInt(document.querySelector('#hi-score').textContent);
    if (score > highScore) {
        document.querySelector('#hi-score').textContent = score;
    }
    return score;
}

const endGameForm = document.createElement('form');
endGameForm.method = 'POST';
endGameForm.action = '/endgame';

function endGame() {
    axios.post('/endgame')
        .then(function (response) {
            endGameForm.submit();
            window.location.href = '/';
        })
}



