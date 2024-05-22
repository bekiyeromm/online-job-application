document.addEventListener("DOMContentLoaded", function() {
    const tableCells = document.querySelectorAll("#admin-table td");

    tableCells.forEach(cell => {
        cell.addEventListener("click", function() {
            const fullValue = cell.getAttribute("data-full-value");
            if (fullValue) {
                alert(fullValue); 
            }
        });
    });
});
