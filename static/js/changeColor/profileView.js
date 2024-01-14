document.addEventListener('DOMContentLoaded', () => {
    const changeColorBtn = document.getElementById("changeColor");
    const box_title = document.getElementsByClassName("title");
    const title_container = document.getElementsByClassName("title-container");
    const black_background = document.getElementsByClassName("black-background");
    const btn = document.getElementsByClassName("btn");

    let isOriginalColor = true;

    function change_color() {
        if (isOriginalColor) {
             Array.from(box_title).forEach(element => element.style.color ="red");
             Array.from(title_container).forEach(element => element.style.backgroundColor ="#3e3e3e");
             Array.from(black_background).forEach(element => { element.style.backgroundColor ="black"; element.style.color="white"; });
             Array.from(btn).forEach(element => { element.style.backgroundColor ="black"; element.style.color="white"; });

             
        } else {
            Array.from(box_title).forEach(element => element.style.color ="");
            Array.from(title_container).forEach(element => element.style.backgroundColor ="");
            Array.from(black_background).forEach(element => { element.style.backgroundColor ="";  element.style.color=""; });
            Array.from(btn).forEach(element => { element.style.backgroundColor ="black"; element.style.color=""; });

        }
        isOriginalColor = !isOriginalColor;
    }

    if (changeColorBtn) {
        changeColorBtn.addEventListener('click', change_color);
    }
});