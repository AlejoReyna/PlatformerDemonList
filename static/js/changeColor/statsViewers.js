document.addEventListener('DOMContentLoaded', () => {
    const changeColorBtn = document.getElementById("changeColor");
    const box_title = document.getElementsByClassName("title");
    const title_container = document.getElementsByClassName("title-container");
    const black_background = document.getElementsByClassName("black-background");
    const table_container = document.getElementById("table-container");
    let isOriginalColor = true;


    function change_color() {
        if (isOriginalColor) {
            table_container.style.backgroundColor = "black";
            Array.from(box_title).forEach(element => element.style.color ="red");
            Array.from(title_container).forEach(element => element.style.backgroundColor ="#3e3e3e");
            Array.from(black_background).forEach(element =>  { element.style.backgroundColor ="black"; element.style.color="red";}); 
        } else {
            table_container.style.backgroundColor = "white";
            Array.from(box_title).forEach(element => element.style.color ="");
            Array.from(title_container).forEach(element => element.style.backgroundColor ="");
            Array.from(black_background).forEach(element => { element.style.backgroundColor ="";  element.style.color=""; });
        }
        isOriginalColor = !isOriginalColor;
    }
    if (changeColorBtn) {
        changeColorBtn.addEventListener('click', change_color);
    }
});