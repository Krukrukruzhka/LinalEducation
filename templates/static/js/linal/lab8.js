DOMAIN = "";

const URL = DOMAIN + "/linal/lab8/check";


function show_verdict(verdict) {
    const red = "#FFBCAD";
    const green = "#ACE1AF";

    let verdict_block = document.getElementById("user_verdict_block");
    if (!verdict_block) {
        console.error("Element with id 'user_verdict_block' not found.");
        return;
    }

    verdict_block.removeAttribute("hidden");
    let verdict_image = verdict_block.getElementsByClassName("verdict_image")[0];
    let verdict_text = verdict_block.getElementsByClassName("verdict_text")[0];

    if (verdict) {
        verdict_block.style.background = green;
        verdict_text.textContent = "Решено";
    } else {
        verdict_block.style.background = red;
        verdict_text.textContent = "Есть ошибки";
    }

}


function check_request() {
    let response_dict = {};

    let step1_inputs = document.getElementsByClassName("linal_lab8_step1_input");
    let intValues = [];
    for (let i = 0; i < step1_inputs.length; i++) {
        let value = parseInt(step1_inputs[i].value, 10);
        if (!isNaN(value)) {
            intValues.push(value);
        } else {
            intValues.push(0);
        }
    }
    response_dict[`step_1`] = intValues

    let matrices = document.getElementsByClassName("editable_matrix");
    response_dict[`step_2`] = matrices[0].getElementsByClassName("matrix_element")[0].value;

    console.log(response_dict);

    const xhr = new XMLHttpRequest();
    xhr.open("POST", URL);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify(response_dict));

    xhr.onreadystatechange = function() {
        if (this.readyState === 4) {
            console.log("Status:", this.status);
            if (this.status === 200) {
                console.log("Response:", this.responseText);
                const responseObject = JSON.parse(this.responseText);
                const verdict = responseObject.verdict;
                show_verdict(verdict);
            } else {
                console.error("Request failed with status", this.status);
            }
        }
    };
}