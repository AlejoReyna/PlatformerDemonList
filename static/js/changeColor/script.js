document.addEventListener('DOMContentLoaded', () => {
    const changeColorBtn = document.getElementById("changeColor");
    const navbar = document.getElementById("main-navbar");
    const demonCard = document.getElementsByClassName("demonCard");
    const nextUpdate = document.getElementById("nextUpdate");
    const searchbar = document.getElementById("search");
    const projectHelpers = document.getElementById("projectHelpers");
    const listDevs = document.getElementById("listDevs");
    let isOriginalColor = true;

    function change_color() {
        if (isOriginalColor) {
            navbar.style.backgroundColor = gray;
            Array.from(demonCard).forEach(card => card.style.backgroundColor = "black");
            if (nextUpdate) { // Check if element exists
                nextUpdate.style.backgroundColor = "black";
            }
            searchbar.style.backgroundColor = "gray";
            projectHelpers.style.backgroundColor = "black";
            listDevs.style.backgroundColor = "black";
        } else {
            navbar.style.backgroundColor = ""; // Resets to original color
            Array.from(demonCard).forEach(card => card.style.backgroundColor = ""); // Resets to original color
            if (nextUpdate) { // Check if element exists
                nextUpdate.style.backgroundColor = "";
            }
            
            searchbar.style.backgroundColor = "";
            projectHelpers.style.backgroundColor = "";
            listDevs.style.backgroundColor = "";
        }
        isOriginalColor = !isOriginalColor;
    }

    // Assuming you want to trigger the function on button click
    if (changeColorBtn) {
        changeColorBtn.addEventListener('click', change_color);
    }
});
