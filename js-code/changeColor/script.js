const changeColorBtn = document.getElementById("changeColor");
    // La siguiente línea obtiene la navbar por completo
    const navbar = document.getElementById("main-navbar");

    // Básicamente la siguiente variable checa si el color está en blanco o nel
    let isOriginalColor = true; 
    
    function change_color(){
        /** Primer código 
        changeColorBtn.addEventListener("click", function() {
            navbar.style.backgroundColor = "black";
        }); **/
        if (isOriginalColor) {
            navbar.style.backgroundColor = "black";
        } else {
            navbar.style.backgroundColor = ""; // Establece esto al color original
        }
        isOriginalColor = !isOriginalColor; 
    }