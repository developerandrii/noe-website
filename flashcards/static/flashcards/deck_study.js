const cardTileContent = document.querySelector("[data-card-tile-content]");
const correctAnswer = document.querySelector("[data-card-correct-answer]");
const guessInput = document.querySelector("[data-card-guess-input]");
const checkButton = document.querySelector("[data-card-guess-check]");
const comparison = document.querySelector("[data-card-comparison]");

function normalizeText(text) {
    // Ignore spaces around the answer and make comparison case-insensitive.
    return text.trim().toLowerCase();
}

function buildSimpleComparison(userAnswer, correctAnswer) {
    const result = document.createElement("p");
    result.classList.add("card-comparison__text");

    const normalizedUserAnswer = normalizeText(userAnswer);
    const normalizedCorrectAnswer = normalizeText(correctAnswer);

    // We compare by character for now.
    // This is simple and imperfect, but good enough for the first version.
    const maxLength = Math.max(
        normalizedUserAnswer.length,
        normalizedCorrectAnswer.length,
    );

    for (let index = 0; index < maxLength; index += 1) {
        const userCharacter = normalizedUserAnswer[index];
        const correctCharacter = normalizedCorrectAnswer[index];

        const character = document.createElement("span");

        if (userCharacter === correctCharacter) {
            character.textContent = correctCharacter;
        } else if (userCharacter && !correctCharacter) {
            // User typed an extra character that does not exist in the correct answer.
            character.textContent = userCharacter;
            character.classList.add("card-comparison__extra");
        } else if (!userCharacter && correctCharacter) {
            // User missed a character that exists in the correct answer.
            character.textContent = correctCharacter;
            character.classList.add("card-comparison__missing");
        } else {
            // User typed a different character than expected.
            character.textContent = userCharacter;
            character.classList.add("card-comparison__extra");
        }

        result.appendChild(character);
    }

    return result;
}

if (cardTileContent && correctAnswer && guessInput && checkButton && comparison) {
    checkButton.addEventListener("click", () => {
        const userAnswer = guessInput.value;
        const realAnswer = correctAnswer.textContent;

        // After pressing check button, the visible card changes from front to back.
        cardTileContent.textContent = realAnswer;

        // Display comparison container when check button is clicked.
        comparison.hidden = false;
        comparison.replaceChildren();

        const title = document.createElement("h2");
        title.classList.add("card-comparison__title");
        title.textContent = "Comparison";

        comparison.appendChild(title);
        comparison.appendChild(buildSimpleComparison(userAnswer, realAnswer));

        // Turn off check button.
        // Prevent checking the same card multiple times for now.
        checkButton.disabled = true;
    });
}