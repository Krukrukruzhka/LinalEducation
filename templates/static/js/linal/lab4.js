import { getMatrixById } from '../matrix.js';
import { show_verdict, send_response } from '../common.js';


DOMAIN = "";
const URL = DOMAIN + "/linal/lab4/check";


function check_request() {
    let response_dict = {};
    let matrices = document.getElementsByClassName("editable_matrix");
    response_dict[`answer_matrix_det`] = matrices[0].getElementsByClassName("matrix_element")[0].value;
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
