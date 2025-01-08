const DOMAIN = "http://127.0.0.1"

REGISTRATE_URL = DOMAIN + "/register-user";
LOGIN_URL = DOMAIN + "/login-user";
PROFILE_URL = DOMAIN + "/profile";


function register_user() {
    let response_dict = {};

    response_dict[`role_id`] = document.getElementById("input_role").value;
    response_dict[`name`] = document.getElementById("input_name").value;
    response_dict[`username`] = document.getElementById("input_login").value;
    response_dict[`password`] = document.getElementById("input_password").value;
    response_dict[`repeated_password`] = document.getElementById("input_repeated_password").value;

    console.log(response_dict);

    const xhr = new XMLHttpRequest();
    xhr.open("POST", REGISTRATE_URL);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify(response_dict));

    xhr.onreadystatechange = function() {
        if (this.readyState === 4) {
            console.log("Status:", this.status);
            if (this.status === 200) {
                console.log("Response:", this.responseText);
                const responseObject = JSON.parse(this.responseText);
                window.location.href = PROFILE_URL;
            } else {
                console.error("Request failed with status", this.status);
            }
        }
    };
}


function login_user() {
    let response_dict = {};

    response_dict[`username`] = document.getElementById("input_login").value;
    response_dict[`password`] = document.getElementById("input_password").value;
    response_dict[`grant_type`] = "password";
    response_dict[`scopes`] = null;
    response_dict[`client_id`] = null;
    response_dict[`client_secret`] = null;

    console.log(response_dict);

    const xhr = new XMLHttpRequest();
    xhr.open("POST", LOGIN_URL);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify(response_dict));

    xhr.onreadystatechange = function() {
        if (this.readyState === 4) {
            console.log("Status:", this.status);
            if (this.status === 200) {
                console.log("Response:", this.responseText);
                const responseObject = JSON.parse(this.responseText);
                window.location.href = PROFILE_URL;
            } else {
                console.error("Request failed with status", this.status);
            }
        }
    };
}


function to_login() {
    window.location.href = DOMAIN + "/login";
}


function to_register() {
    window.location.href = DOMAIN + "/register";
}
