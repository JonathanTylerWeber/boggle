const guessForm = document.querySelector('#guess-form')

guessForm.addEventListener('submit', function (e) {
    e.preventDefault()
    let guessInput = document.querySelector('#guess')
    let guess = guessInput.value
    axios.post('/guess', { 'guess': guess })
        .then(function (response) {
            const result = response.data.result;
            console.log(result)
            if (result === 'ok') {
                console.log('Word is valid and exists on the board.');
            } else if (result === 'not-on-board') {
                console.log('Word is not on the board.');
            } else if (result === 'not-word') {
                console.log('Word is not a valid word.');
            }
        })
})

