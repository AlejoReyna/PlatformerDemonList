document.addEventListener('DOMContentLoaded', () => {
    const changeColorBtn = document.getElementById("changeColor");
    const navbar = document.getElementById("main-navbar");
    const demonCard = document.getElementsByClassName("demonCard");
    const nextUpdate = document.getElementById("nextUpdate");
    const body = document.getElementById("bg");
    const searchbar = document.getElementById("search");

    let isOriginalColor = true;

    function change_color() {
        if (isOriginalColor) {
            navbar.style.backgroundColor = "black";
            Array.from(demonCard).forEach(card => card.style.backgroundColor = "black");
            if (nextUpdate) { // Check if element exists
                nextUpdate.style.backgroundColor = "black";
            }
            body.style.backgroundColor = "black";
            searchbar.style.backgroundColor = "gray";
        } else {
            navbar.style.backgroundColor = ""; // Resets to original color
            Array.from(demonCard).forEach(card => card.style.backgroundColor = ""); // Resets to original color
            if (nextUpdate) { // Check if element exists
                nextUpdate.style.backgroundColor = "";
            }
            body.style.backgroundColor = "";
            searchbar.style.backgroundColor = "";
        }
        isOriginalColor = !isOriginalColor;
    }

    // Assuming you want to trigger the function on button click
    if (changeColorBtn) {
        changeColorBtn.addEventListener('click', change_color);
    }
});