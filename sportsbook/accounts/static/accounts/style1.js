document.addEventListener("DOMContentLoaded", function() {
    const amountForm = document.getElementById("amountForm");
    const fullForm = document.getElementById("fullForm");
    const amountInput = document.getElementById("amount");
    const finalAmount = document.getElementById("finalAmount");

    fullForm.style.display = "none";

    amountForm.addEventListener("submit", function(e) {
        e.preventDefault();
        const amount = parseInt(amountInput.value);

        if (amount < 300 || amount > 100000) {
            alert("Deposit must be between 300 and 100000");
        } else {
            finalAmount.value = amount;
            fullForm.style.display = "flex";
        }
    });
})


