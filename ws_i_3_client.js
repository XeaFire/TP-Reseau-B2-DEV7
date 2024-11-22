function hello() {
    const uri = "ws://5.5.5.11:8765";
    const websks = new WebSocket(uri);

    websks.onopen = () => chat(websks);

    websks.onmessage = (event) => {
        console.log(event.data);
    };
}

function chat(websks) {
    let userInput;

    do {
        userInput = prompt("Chatbox :");
        if (userInput) websks.send(userInput);
    } while (userInput);
}

hello();
