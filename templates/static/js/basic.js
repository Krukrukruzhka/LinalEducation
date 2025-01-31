DOMAIN = "";

const LOGOUT_URL = DOMAIN + "/logout";
const EDIT_ADD_INFO_URL = DOMAIN + "/update-additional-info";
const ADD_NEW_GROUPS_URL = DOMAIN + "/add-new-groups";


function to_profile() {
    window.location.href = DOMAIN + "/profile";
}


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
};

function show_edit_block(block_id) {
    let modal = document.getElementById(block_id);
    let body = document.body;

    modal.style.display = 'block';
    body.classList.add("blurred_content");
};


function hide_edit_block(block_id) {
    let modal = document.getElementById(block_id);
    let body = document.body;

    modal.style.display = 'none';
    body.classList.remove("blurred_content");
};


function save_userdata() {
    let edit_modal = document.getElementById("edit_modal")
    let response_dict = {};

    const labels = edit_modal.querySelectorAll('label.user_info');

    labels.forEach(label => {
        const inputElement = label.querySelector('input, select');
        if (inputElement) {
            response_dict[inputElement.id] = inputElement.value === "None" ? null : inputElement.value;
        }
    });

    console.log(response_dict);

    const xhr = new XMLHttpRequest();
    xhr.open("POST", EDIT_ADD_INFO_URL);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify(response_dict));

    xhr.onreadystatechange = function() {
        if (this.readyState === 4) {
            console.log("Status:", this.status);
            if (this.status === 200) {
                console.log("Response:", this.responseText);
                const responseObject = JSON.parse(this.responseText);
                hide_edit_block('edit_modal');
                location.reload();
            } else {
                console.error("Request failed with status", this.status);
            }
        }
    };
}


function add_new_groups() {
    let edit_modal = document.getElementById("add_groups")
    let response_dict = {"text_with_groups": document.getElementById('group_description').value};

    console.log(response_dict);

    const xhr = new XMLHttpRequest();
    xhr.open("POST", ADD_NEW_GROUPS_URL);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify(response_dict));

    xhr.onreadystatechange = function() {
        if (this.readyState === 4) {
            console.log("Status:", this.status);
            if (this.status === 200) {
                console.log("Response:", this.responseText);
                const responseObject = JSON.parse(this.responseText);
                hide_edit_block('add_groups');
                location.reload();
            } else {
                console.error("Request failed with status", this.status);
            }
        }
    };
}