// Script to change the color of the navbar 
document.addEventListener('DOMContentLoaded', () => {
    const menuBtn = document.getElementById("menuBtn");
    const navbar = document.getElementById("main-navbar");
    const changeColorBtn = document.getElementById("changeColor");
    const menuIcon = document.getElementById("menuIcon");
    const MenuText = document.getElementsByClassName("MenuText");
    const dropdownContainer = document.getElementById("menuContent");
    const menuElement = document.getElementsByClassName("menuElement");
    let isOriginalColor = true;

    function change_color() {
        if (isOriginalColor) {
            navbar.style.backgroundColor = "#3e3e3e";
            changeColorBtn.classList.remove("fa-moon");
            changeColorBtn.classList.add("fa-sun");
            changeColorBtn.style.color = "white"; 
            menuBtn.style.backgroundColor = "#17181a";
            dropdownContainer.style.backgroundColor = "#17181a";
            Array.from(MenuText).forEach(element => element.style.color = "white");
            Array.from(menuElement).forEach(element => element.style.color = "white");
            menuIcon.style.backgroundColor = "white";
        } else {
            navbar.style.backgroundColor = "";
            changeColorBtn.classList.remove("fa-sun");
            changeColorBtn.classList.add("fa-moon");
            changeColorBtn.style.color = ""; 
            menuBtn.style.backgroundColor = "white";
            dropdownContainer.style.backgroundColor = "";
            Array.from(MenuText).forEach(element => element.style.color = "");
            Array.from(menuElement).forEach(element => element.style.color = "");
            menuIcon.style.backgroundColor = "";
        }
        isOriginalColor = !isOriginalColor;
        localStorage.setItem('isOriginalColor', isOriginalColor);
    }

    function applyNightMode() {
        // Verifica si el modo nocturno está activo y aplica los estilos
        if (localStorage.getItem('isOriginalColor') === 'false') {
            change_color();
        }
    }

    if (changeColorBtn) {
        changeColorBtn.addEventListener('click', change_color);
    }

    applyNightMode();
});