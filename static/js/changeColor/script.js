document.addEventListener('DOMContentLoaded', () => {
    const changeColorBtn = document.getElementById("changeColor");
    const navbar = document.getElementById("main-navbar");
    const demonCard = document.getElementsByClassName("demonCard");
    const news = document.getElementById("news");
    const nextUpdate = document.getElementById("nextUpdate");
    const searchbar = document.getElementById("search");
    const projectHelpers = document.getElementById("projectHelpers");
    const listDevs = document.getElementById("listDevs");
    const TekoLight = document.getElementsByClassName("Teko-Light");
    const menuBtn = document.getElementById("menuBtn");
    const menuIcon = document.getElementById("menuIcon");
    const unrated = document.getElementById("unrated");
    // Get searchbar
    const inputBar = document.getElementById("search");
    // Get their elements 
    const inputElements = document.getElementsByClassName("inputElements");
    let isOriginalColor = true;

    function change_color() {
        if (isOriginalColor) {
            navbar.style.backgroundColor = "#3e3e3e";
            // Demon card styles
            Array.from(demonCard).forEach(card => card.style.backgroundColor = "black");
            Array.from(demonCard).forEach(card => card.style.background = 'linear-gradient(to bottom, #111, #333)');
            // Next update
            nextUpdate.style.backgroundColor = "black";
            nextUpdate.style.background = 'linear-gradient(to bottom, #111, #333)';
            news.style.backgroundColor = "black";
            // News
            news.style.background = 'linear-gradient(to bottom, #111, #333)';
            // Searchbar
            searchbar.style.backgroundColor = "gray";
            // Project Helpers
            projectHelpers.style.backgroundColor = "black";
            // ListDevs
            listDevs.style.backgroundColor = "black";
            listDevs.style.background = 'linear-gradient(to bottom, #111, #333)';
            inputBar.style.backgroundColor = "#17181a";
            Array.from(inputElements).forEach(element => element.style.color = "white");
            Array.from(TekoLight).forEach(element => element.style.color = "white");
            menuBtn.style.backgroundColor = "#17181a";
            menuIcon.style.backgroundColor = "white";
            // Unrated
            unrated.style.background = 'linear-gradient(to bottom, #111, #333)';



        } else {
            navbar.style.backgroundColor = ""; // Resets to original color
            Array.from(demonCard).forEach(card => card.style.backgroundColor = ""); // Resets to original color
            nextUpdate.style.backgroundColor = "";
            searchbar.style.backgroundColor = "";
            projectHelpers.style.backgroundColor = "";
            listDevs.style.backgroundColor = "";
            inputBar.style.backgroundColor = "";
            Array.from(inputElements).forEach(element => element.style.color = "");
            Array.from(TekoLight).forEach(element => element.style.color = "");
            menuBtn.style.backgroundColor = "";
            menuIcon.style.backgroundColor = "";

        }
        isOriginalColor = !isOriginalColor;
    }

    // Assuming you want to trigger the function on button click
    if (changeColorBtn) {
        changeColorBtn.addEventListener('click', change_color);
    }
});

