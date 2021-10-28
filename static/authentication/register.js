const usernameField = document.querySelector("#username");
const usernameFeedback = document.querySelector(".username-feedback");

const emailField = document.querySelector("#email");
const emailFeedback = document.querySelector(".email-feedback");

const passwordField = document.querySelector("#password");
const showPassBtn = document.querySelector(".show");

const submitBtn = document.querySelector(".submit-btn");

let email_valid = false, password_valid = false, username_valid = false;

submitBtn.disabled = true;

document.addEventListener('keyup',(e)=>{
    console.log(email_valid,password_valid,username_valid);
    if(email_valid&&password_valid&&username_valid)
    {
        submitBtn.removeAttribute('disabled');
    }
    else{
        submitBtn.disabled = true;
    }
});

usernameField.addEventListener("keyup", (e) => {
    const username = e.target.value;
    usernameFeedback.innerHTML = `checking ${username}`;
    usernameFeedback.classList.remove('invalid-feedback');
    usernameFeedback.classList.add('valid-feedback');
    usernameFeedback.style.display = 'block';
    if (username.length > 0) {
        fetch("/auth/username_validation/", {
            body: JSON.stringify({
                "username": username,
            }),
            method: "POST",
        })
            .then((res) => res.json()
                .then((data) => {
                    if (data.username_error) {
                        username_valid = false;
                        usernameFeedback.classList.remove('valid-feedback');
                        usernameFeedback.classList.add('invalid-feedback');

                        usernameField.classList.add('is-invalid');
                        usernameFeedback.innerHTML = `<p>${data.username_error}</p>`;
                    }
                    else {
                        username_valid = true;
                        usernameField.classList.remove('is-invalid');
                        usernameFeedback.innerHTML = "username valid";
                        // usernameFeedback.style.display = "none";
                    }
                }));
    }
    else {
        username_valid = false;
        usernameField.classList.remove('is-invalid');
        usernameFeedback.style.display = "none";
    }
});

emailField.addEventListener("keyup", (e) => {
    const email = e.target.value;
    emailFeedback.innerHTML = `checking ${email}`;
    emailFeedback.classList.remove('invalid-feedback');
    emailFeedback.classList.add('valid-feedback');
    emailFeedback.style.display = 'block';
    if (email.length > 0) {
        fetch("/auth/email_validation/", {
            body: JSON.stringify({
                "email": email,
            }),
            method: "POST",
        })
            .then((res) => res.json()
                .then((data) => {
                    if (data.email_error) {
                        email_valid = false;
                        emailFeedback.classList.remove('valid-feedback');
                        emailFeedback.classList.add('invalid-feedback');
                        emailField.classList.add('is-invalid');
                        emailFeedback.innerHTML = `<p>${data.email_error}</p>`;
                    }
                    else {
                        email_valid = true;
                        emailFeedback.innerHTML = "email valid";
                        emailField.classList.remove('is-invalid');

                    }
                }));
    }
    else {
        emailField.classList.remove('is-invalid');
        emailFeedback.style.display = "none";
        email_valid = false;
    }
});
passwordField.addEventListener('keyup',(e)=>{
    if(e.target.value.length>0)
    {
        password_valid = true;
    }
    else{
        password_valid = false;
    }
});
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
