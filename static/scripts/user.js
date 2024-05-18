function validateForm() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    if (username.trim() === "") {
      alert("Username cannot be empty");
      return false;
    }
    if (password.trim() === "") {
      alert("Password cannot be empty");
      return false;
    }
    if (password.length < 8) {
      alert("Password must be at least 8 characters long");
      return false;
    }
    return true;
  }