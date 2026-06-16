const cardTileContent = document.querySelector("[data-card-tile-content]");
const correctAnswer = document.querySelector("[data-card-correct-answer]");
const checkButton = document.querySelector("[data-card-guess-check]");

if (cardTileContent && correctAnswer && checkButton) {
    checkButton.addEventListener("click", () => {
        cardTileContent.textContent = correctAnswer.textContent;
        checkButton.disabled = true;
    });
}