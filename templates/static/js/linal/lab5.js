import { getMatrixById } from '../matrix.js';
import { show_verdict, send_response } from '../common.js';


DOMAIN = "";
const URL = DOMAIN + "/linal/lab5/check";


function check_request() {
    let response_dict = {};
    response_dict[`matrix_a_res`] = document.getElementById("step1_determinant").value;
    response_dict[`matrix_b_res`] = document.getElementById("step2_determinant").value;
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
