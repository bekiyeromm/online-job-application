function validateForm() {
   
    var username = document.getElementById("username").value;
    var age = document.getElementById("age").value;
    var address = document.getElementById("address").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;

    if (username.length < 3) {
        alert("Username must be at least 3 characters long.");
        return false;
    }

  
    if (age <= 0 || isNaN(age)) {
        alert("Please enter a valid age.");
        return false;
    }

    if (address.trim() === "") {
        alert("Address cannot be empty.");
        return false;
    }

    var emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    if (!emailPattern.test(email)) {
        alert("Please enter a valid email address.");
        return false;
    }

   
    if (password.length < 6) {
        alert("Password must be at least 6 characters long.");
        return false;
    }

    return true;
}
