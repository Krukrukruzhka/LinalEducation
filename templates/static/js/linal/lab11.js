import { getMatrixById } from '../matrix.js';
import { show_verdict, send_response } from '../common.js';


DOMAIN = "";
const URL = DOMAIN + "/linal/lab11/check";


function check_request() {
    let response_dict = {};

    response_dict[`step_1_det`] = document.getElementById("step_1_det").value;

    response_dict[`step_2_det_1`] = document.getElementById("step_2_det_1").value;
    response_dict[`step_2_det_2`] = document.getElementById("step_2_det_2").value;
    response_dict[`step_2_det_3`] = document.getElementById("step_2_det_3").value;

    response_dict[`step_3_x_1`] = document.getElementById("step_3_x_1").value;
    response_dict[`step_3_x_2`] = document.getElementById("step_3_x_2").value;
    response_dict[`step_3_x_3`] = document.getElementById("step_3_x_3").value;

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
