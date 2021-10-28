const passwordField = document.querySelector("#password");
const showPassBtn = document.querySelector(".show");


showPassBtn.addEventListener('click', (e) => {
    if (passwordField.visible == "true") {
        passwordField.visible = "false";
        passwordField.type = "password";
        showPassBtn.textContent = "show";
    }
    else {
        passwordField.visible = "true";
        passwordField.type = "text";
        showPassBtn.textContent = "hide";
    }
});
