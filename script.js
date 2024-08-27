const canvas = document.getElementById('puzzleCanvas');
const ctx = canvas.getContext('2d');

// Definir el tamaño del canvas y el número de filas y columnas de cuadros
const canvasSize = 500;
const numRows = 2;
const numCols = 2;

// Calcular el tamaño de cada cuadro
const squareSize = canvasSize / numRows;

// Crear un array de cuadros
const squares = [];
for (let row = 0; row < numRows; row++) {
    for (let col = 0; col < numCols; col++) {
        squares.push({
            x: col * squareSize,
            y: row * squareSize,
            width: squareSize,
            height: squareSize
        });
    }
}

// Definir las figuras con diferentes tamaños
const shapes = [
    { x: 10, y: 10, width: 200, height: 200, color: 'red' },
    { x: 120, y: 10, width: 120, height: 90, color: 'green' },
    { x: 220, y: 10, width: 110, height: 110, color: 'blue' },
    { x: 10, y: 120, width: 240, height: 130, color: 'yellow' },
    { x: 150, y: 120, width: 150, height: 120, color: 'purple' },
    { x: 260, y: 120, width: 120, height: 200, color: 'orange' },
    { x: 10, y: 260, width: 150, height: 100, color: 'cyan' },
    { x: 130, y: 260, width: 120, height: 420, color: 'pink' },
    { x: 270, y: 260, width: 200, height: 460, color: 'brown' }
];

let selectedShape = null;
let offsetX, offsetY;

function drawShapes() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (const shape of shapes) {
        ctx.fillStyle = shape.color;
        ctx.fillRect(shape.x, shape.y, shape.width, shape.height);
    }
    for (const square of squares) {
        ctx.strokeStyle = 'black';
        ctx.strokeRect(square.x, square.y, square.width, square.height);
    }
}

canvas.addEventListener('mousedown', (e) => {
    const mouseX = e.offsetX;
    const mouseY = e.offsetY;

    for (const shape of shapes) {
        if (
            mouseX > shape.x &&
            mouseX < shape.x + shape.width &&
            mouseY > shape.y &&
            mouseY < shape.y + shape.height
        ) {
            selectedShape = shape;
            offsetX = mouseX - shape.x;
            offsetY = mouseY - shape.y;
            break;
        }
    }
});

canvas.addEventListener('mousemove', (e) => {
    if (selectedShape) {
        selectedShape.x = e.offsetX - offsetX;
        selectedShape.y = e.offsetY - offsetY;
        drawShapes();
    }
});

canvas.addEventListener('mouseup', () => {
    selectedShape = null;
});

drawShapes();
