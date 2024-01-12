// Script to change color of the footer
document.addEventListener('DOMContentLoaded', () => {
    const changeColorBtn = document.getElementById("changeColor");
    const footer = document.getElementsByClassName("footer");
    const footerIcon = document.getElementsByClassName("footerIcon");
    function change_color() {
        if (isOriginalColor) {
            Array.from(footer).forEach(element => element.style.color = "black");
            Array.from(footerIcon).forEach(element => element.style.color = "white");
        } else {
            Array.from(footer).forEach(element => element.style.color = "black");
            Array.from(footerIcon).forEach(element => element.style.color = "white");
        }
        isOriginalColor = !isOriginalColor;
    }
    if (changeColorBtn) {
        changeColorBtn.addEventListener('click', change_color);
    }

});