// code for darkmode
document.addEventListener('DOMContentLoaded', () => {
    const changeColorBtn = document.getElementById("changeColor");
    const TekoRed = document.getElementsByClassName("TekoRed");
    const BlackBlackground = document.getElementsByClassName("BlackBackground");
    let isOriginalColor = true;


    function change_color() {
        if (isOriginalColor) {
        Array.from(TekoRed).forEach(element => element.style.color = "red");
        Array.from(BlackBlackground).forEach(element => element.style.backgroundColor = "black");
        navbar.style.backgroundColor = "#3e3e3e";
        } else {
        Array.from(TekoRed).forEach(element => element.style.color = "");
        navbar.style.backgroundColor = "";
        Array.from(BlackBlackground).forEach(element => element.style.backgroundColor = "");
        }
        isOriginalColor = !isOriginalColor;
    }
    if (changeColorBtn) {
        changeColorBtn.addEventListener('click', change_color);
    }
});