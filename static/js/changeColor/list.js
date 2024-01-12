// Script for list template
document.addEventListener('DOMContentLoaded', () => {
    const changeColorBtn = document.getElementById("changeColor");
    const demonCard = document.getElementsByClassName("demonCard");
    const news = document.getElementById("news");
    const nextUpdate = document.getElementById("nextUpdate");
    const projectHelpers = document.getElementById("projectHelpers");
    const listDevs = document.getElementById("listDevs");
    const TekoLight = document.getElementsByClassName("Teko-Light");
    const menuBtn = document.getElementById("menuBtn");
    const menuIcon = document.getElementById("menuIcon");
    const unrated = document.getElementById("unrated");
    const cardText = document.getElementsByClassName("cardText")
    // Get searchbar
    const inputBar = document.getElementById("search");
    // Get their elements 
    const inputElements = document.getElementsByClassName("inputElements");
    let isOriginalColor = true;

    function change_color() {
        if (isOriginalColor) {
            
            // Demon card styles
            Array.from(demonCard).forEach(card => card.style.backgroundColor = "black");
            Array.from(demonCard).forEach(card => card.style.background = 'linear-gradient(to right, #0a0f0d, #000000);');
            // Next update
            nextUpdate.style.backgroundColor = "black";
            nextUpdate.style.background = 'linear-gradient(to bottom, #111, #333)';
            news.style.backgroundColor = "black";
            // News
            news.style.background = 'linear-gradient(to bottom, #2c2c2c, #000000);';
            Array.from(cardText).forEach(element => element.style.color = "white");
            // Project Helpers
            projectHelpers.style.backgroundColor = "black";
            // ListDevs
            listDevs.style.backgroundColor = "black";
            listDevs.style.background = 'linear-gradient(to bottom, #2e2e2e 0%, #1c1c1c 50%, #000000 100%);';
            inputBar.style.backgroundColor = "#17181a";
            inputBar.style.color = "white";
            Array.from(inputElements).forEach(element => element.style.color = "white");
            Array.from(TekoLight).forEach(element => element.style.color = "white");
            menuBtn.style.backgroundColor = "#17181a";
            menuIcon.style.backgroundColor = "white";
            // Unrated
            unrated.style.background = 'linear-gradient(to bottom, #111, #333)';
            


        } else {
            /*
            navbar.style.backgroundColor = "";*/ // Resets to original color
            Array.from(demonCard).forEach(card => card.style.backgroundColor = ""); // Resets to original color
            nextUpdate.style.backgroundColor = "";
            nextUpdate.style.background = "";
            news.style.backgroundColor = "";
            // News
            news.style.background = "";
            Array.from(cardText).forEach(element => element.style.color = "");

            projectHelpers.style.backgroundColor = "";
            listDevs.style.backgroundColor = "";
            listDevs.style.background = "";
            inputBar.style.backgroundColor = "";
            Array.from(inputElements).forEach(element => element.style.color = "");
            Array.from(TekoLight).forEach(element => element.style.color = "");
            menuBtn.style.backgroundColor = "white";
            menuIcon.style.backgroundColor = "";
            // Unrated 
            unrated.style.background = "";


        }
        isOriginalColor = !isOriginalColor;
    }

    // Assuming you want to trigger the function on button click
    if (changeColorBtn) {
        changeColorBtn.addEventListener('click', change_color);
    }
});

