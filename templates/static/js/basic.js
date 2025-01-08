DOMAIN = "";

const LOGOUT_URL = DOMAIN + "/logout";


function logout() {

    const xhr = new XMLHttpRequest();
    xhr.open("POST", LOGOUT_URL);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send();

    xhr.onreadystatechange = function() {
        if (this.readyState === 4) {
            console.log("Status:", this.status);
            if (this.status === 200) {
                console.log("Response:", this.responseText);
                location.reload();
            } else {
                console.error("Request failed with status", this.status);
            }
        }
    };
}