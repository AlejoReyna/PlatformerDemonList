// code for darkmode
document.addEventListener('DOMContentLoaded', () => {
    const changeColorBtn = document.getElementById("changeColor");
    const table_headers = document.getElementsByClassName("table-header");
    const table_row = document.getElementsByClassName("table-row");
    let isOriginalColor = true;
        function change_color() {
            // Iterar sobre cada elemento .table-header y aplicar los estilos
            for (const header of table_headers) {
                if (isOriginalColor) {
                    header.style.background = 'linear-gradient(to bottom, #111, #333)';
                } else {
                    header.style.background = ''; // Cambiar a un color o gradiente diferente si se desea
                }
            }
            isOriginalColor = !isOriginalColor;
        }
    
        if (changeColorBtn) {
            changeColorBtn.addEventListener('click', change_color);
        }
    });
    

