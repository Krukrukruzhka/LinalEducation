export function show_verdict() {
    const red = "#FFBCAD";
    const green = "#ACE1AF";

    let verdict = document.getElementById("is_solved").textContent;
    console.log(verdict);

    let verdict_block = document.getElementById("user_verdict_block");
    if (!verdict_block) {
        console.error("Element with id 'user_verdict_block' not found.");
        return;
    }

    verdict_block.removeAttribute("hidden");
    let verdict_image = verdict_block.getElementsByClassName("verdict_image")[0];
    let verdict_text = verdict_block.getElementsByClassName("verdict_text")[0];

    if (verdict == "true") {
        verdict_block.style.background = green;
        verdict_text.textContent = "Решено";
    } else {
        verdict_block.style.background = red;
        verdict_text.textContent = "Есть ошибки";
    }

}


export function send_response(response_dict, url) {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", url);
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