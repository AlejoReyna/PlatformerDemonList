// Script to change color of the elemnts of the updateProfile screen
document.addEventListener('DOMContentLoaded', () => {
    const changeColorBtn = document.getElementById("changeColor");
    const box_title = document.getElementsByClassName("title");
    const title_container = document.getElementsByClassName("title-container");

    let isOriginalColor = true;


    function change_color() {
        if (isOriginalColor) {
            Array.from(box_title).forEach(element => element.style.color ="red");
            Array.from(title_container).forEach(element => element.style.backgroundColor ="#3e3e3e");
        
        } else {
            Array.from(box_title).forEach(element => element.style.color ="");
            Array.from(title_container).forEach(element => element.style.backgroundColor ="");
        
        }
        isOriginalColor = !isOriginalColor;
        }

    if (changeColorBtn) {
        changeColorBtn.addEventListener('click', change_color);
        }
});