import { getMatrixById } from '../matrix.js';
import { show_verdict, send_response } from '../common.js';


DOMAIN = "";
const URL = DOMAIN + "/linal/lab1/check";


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

    send_response(response_dict, URL);
}


document.addEventListener('DOMContentLoaded', function () {
    let verdict = document.getElementById("is_solved").textContent;
    if (typeof show_verdict === 'function' && verdict === 'true') {
        show_verdict();
    } else if (typeof show_verdict === 'function') {
        console.info("show_verdict is defined but verdict is not 'true'");
    } else {
        console.error("Function show_verdict is not defined");
    }

    const button = document.getElementById('check_button');
    if (button) {
        button.addEventListener('click', check_request);
    }
});
