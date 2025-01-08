DOMAIN = "";

const URL = DOMAIN + "/lab1/check";


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

    let matrices = document.getElementsByClassName("editable_matrix");
    let matrix = [];
    let rows = matrices[0].getElementsByClassName("matrix_row");
    for (let matrix_row of rows) {
        matrix.push([]);
        let n = matrix.length;
        let matrix_values = matrix_row.getElementsByClassName("matrix_element");
        for (let matrix_element of matrix_values) {
            matrix[n - 1].push(matrix_element.value);
        }
    }
    response_dict[`answer_matrix`] = matrix;
    
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