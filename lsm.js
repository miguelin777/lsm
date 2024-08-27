const letters = [
    { letter: 'C', image: 'img/C.png' },
    { letter: 'J', image: 'img/J.png' },
    { letter: 'D', image: 'img/D.png' },
    { letter: 'W', image: 'img/W.png' },
    { letter: 'E', image: 'img/E.png' },
    { letter: 'F', image: 'img/F.png' },
    { letter: 'A', image: 'img/A.png' },
    { letter: 'X', image: 'img/X.png' },
    { letter: 'I', image: 'img/I.png' },
    { letter: 'Z', image: 'img/Z.png' },
    { letter: 'N', image: 'img/N.png' },
    { letter: 'G', image: 'img/G.png' },
    { letter: 'P', image: 'img/P.png' },
    { letter: 'V', image: 'img/V.png' },
    { letter: 'H', image: 'img/H.png' },
    { letter: 'B', image: 'img/B.png' },
    { letter: 'K', image: 'img/K.png' },
    { letter: 'L', image: 'img/L.png' },
    { letter: 'M', image: 'img/M.png' },
    { letter: 'O', image: 'img/O.png' },
    { letter: 'Y', image: 'img/Y.png' },
    { letter: 'Q', image: 'img/Q.png' },
    { letter: 'R', image: 'img/R.png' },
    { letter: 'S', image: 'img/S.png' },
    { letter: 'Ñ', image: 'img/Ñ.png' },
    { letter: 'T', image: 'img/T.png' },
    { letter: 'U', image: 'img/U.png' }
    
    // Añade más letras e imágenes aquí...
];

let currentLetter = 0;

function showNextSign() {
    if (currentLetter >= letters.length) {
        currentLetter = 0; // Reiniciar a la primera letra si se llegan a mostrar todas
    }
    document.getElementById('signImage').src = letters[currentLetter].image;
    document.getElementById('userInput').value = '';
    document.getElementById('resultMessage').textContent = '';
}

function checkAnswer() {
    const userInput = document.getElementById('userInput').value.toUpperCase();
    const correctLetter = letters[currentLetter].letter;
    const resultMessage = document.getElementById('resultMessage');

    if (userInput === correctLetter) {
        resultMessage.textContent = '¡Correcto!';
        resultMessage.style.color = 'green';
    } else {
        resultMessage.textContent = `Incorrecto. La respuesta correcta es ${correctLetter}.`;
        resultMessage.style.color = 'red';
    }

    currentLetter++;
    setTimeout(showNextSign, 2000); // Mostrar la siguiente seña después de 2 segundos
}

// Mostrar la primera seña al cargar la página
window.onload = showNextSign;