import { getMatrixById } from '../matrix.js';
import { show_verdict, send_response } from '../common.js';


DOMAIN = "";
const URL = DOMAIN + "/angem/lab8/check";


function check_request() {
    let response_dict = {};

    response_dict[`step_1_matrix_1`] = getMatrixById("step_1_matrix_1");
    response_dict[`step_1_matrix_2`] = getMatrixById("step_1_matrix_2");
    response_dict[`step_1_matrix_3`] = getMatrixById("step_1_matrix_3");

    response_dict[`step_2_rank`] = document.getElementById("step_2_rank").value;

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
