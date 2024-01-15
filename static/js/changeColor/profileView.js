document.addEventListener('DOMContentLoaded', () => {
    const changeColorBtn = document.getElementById("changeColor");
    const box_title = document.getElementsByClassName("title");
    const title_container = document.getElementsByClassName("title-container");
    const black_background = document.getElementsByClassName("black-background");
    const value_color = document.getElementsByClassName("value-color");
    const profile_box = document.getElementyById("profile-box");
    const btn = document.getElementsByClassName("btn");
    let isOriginalColor = true;

    function change_color() {
        if (isOriginalColor) {
            profile_box.style.backgroundColor = "gray";             
             Array.from(box_title).forEach(element => element.style.color ="red");
             Array.from(title_container).forEach(element => element.style.backgroundColor ="#3e3e3e");
             Array.from(black_background).forEach(element => { element.style.backgroundColor ="black"; element.style.color="white"; });
             Array.from(btn).forEach(element => { element.style.backgroundColor ="black"; element.style.color="white"; });
             Array.from(value_color).forEach(element => { element.style.backgroundColor ="gray"; element.style.color="white"; });
        } else {
            Array.from(box_title).forEach(element => element.style.color ="");
            Array.from(title_container).forEach(element => element.style.backgroundColor ="");
            Array.from(black_background).forEach(element => { element.style.backgroundColor ="";  element.style.color=""; });
            Array.from(btn).forEach(element => { element.style.backgroundColor ="black"; element.style.color=""; });
            Array.from(value_color).forEach(element => { element.style.backgroundColor ="gray"; element.style.color="white"; });
            profile_box.style.backgroundColor = "";             
        }
        isOriginalColor = !isOriginalColor;
    }

    if (changeColorBtn) {
        changeColorBtn.addEventListener('click', change_color);
    }
});