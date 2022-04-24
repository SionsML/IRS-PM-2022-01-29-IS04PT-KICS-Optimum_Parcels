document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".userInputs").forEach(input => {
        input.addEventListener('input', () => {
            if ((document.querySelector('.user_name').value.length === 0) || (document.querySelector('.password').value.length === 0)) {
                document.querySelector('input[type="submit"]').disabled = true;
            }
            else {
                document.querySelector('input[type="submit"]').disabled = false;
            }
        });
    });
});