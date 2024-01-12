// Script to change color of the elemnts of the updateProfile screen
document.addEventListener('DOMContentLoaded', () => {
    const changeColorBtn = document.getElementById("changeColor");
    const profileBox = document.getElementById("profile-box");
    const labelContainer = document.getElementsByClassName("label-container");
    const labelText = document.getElementsByClassName("labelText");
    const input = document.getElementsByClassName("form-control");
    const updateBtn = document.getElementById("updateBtn");
    const inputValue = document.getElementsByClassName("value-color");
    const msg = document.getElementsByClassName("msg");
    let isOriginalColor = true;


    function change_color() {
        if (isOriginalColor) {
        profileBox.style.backgroundColor = "black";
        Array.from(labelContainer).forEach(element => element.style.backgroundColor = "gray"); 
        Array.from(labelText).forEach(element => element.style.color = "red"); // Resets to original color
        Array.from(input).forEach(element => element.style.background = 'linear-gradient(to bottom, #111, #333)');
        updateBtn.style.backgroundColor = "gray";
        updateBtn.style.color = "red";
        Array.from(inputValue).forEach(element => element.style.color = "white");
        Array.from(msg).forEach(element => element.style.color = "white");
        } else {
        profileBox.style.backgroundColor = "";
        Array.from(labelContainer).forEach(element => element.style.backgroundColor = "");
        Array.from(labelText).forEach(element => element.style.color = ""); // Resets to original color
        Array.from(input).forEach(element => element.style.background = '');
        updateBtn.style.backgroundColor = "";
        updateBtn.style.color = "";
        Array.from(inputValue).forEach(element => element.style.color = "");
        Array.from(msg).forEach(element => element.style.color = "");
        }
        isOriginalColor = !isOriginalColor;
        }

    if (changeColorBtn) {
        changeColorBtn.addEventListener('click', change_color);
        }
});