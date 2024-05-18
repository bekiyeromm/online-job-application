function validateForm() {
    var title = document.getElementById("title").value;
    var location = document.getElementById("location").value;
    var salary = document.getElementById("salary").value;
    var responsibilities = document.getElementById("responsibilities").value;
    var requirements = document.getElementById("requirements").value;

    if (title.trim() === "") {
        alert("Title cannot be empty");
        return false;
    }
    if (location.trim() === "") {
        alert("Location cannot be empty");
        return false;
    }
    if (isNaN(salary) || salary.trim() === "") {
        alert("Salary must be a valid number");
        return false;
    }
    if (responsibilities.trim() === "") {
        alert("Responsibilities cannot be empty");
        return false;
    }
    if (requirements.trim() === "") {
        alert("Requirements cannot be empty");
        return false;
    }

    return true;
}