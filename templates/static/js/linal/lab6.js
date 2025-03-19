import { getMatrixById } from '../matrix.js';
import { show_verdict, send_response } from '../common.js';


DOMAIN = "";
const URL = DOMAIN + "/linal/lab6/check";


function check_request() {
    let response_dict = {};

    let step1_inputs = document.getElementsByClassName("linal_lab6_step1_input");
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

    send_response(response_dict, URL);
}


document.addEventListener('DOMContentLoaded', function () {
   if (typeof show_verdict === 'function') {
        show_verdict();
    } else {
        console.error("Function show_verdict is not defined");
    }

   const button = document.getElementById('check_button');
   if (button) {
       button.addEventListener('click', check_request);
   }
});
