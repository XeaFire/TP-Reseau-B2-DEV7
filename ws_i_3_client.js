function hello() {
    const uri = "ws://5.5.5.11:8765";
    const websks = new WebSocket(uri);
    let userInput = prompt("Choose your username")


    websks.onopen = () => {
        websks.send(userInput);
    };

    websks.onmessage = (event) => {
        console.log(event.data);
    };

    userInput.onchange

    while (true) {
        userInput = prompt("Chatbox : ")
    }

}


hello()

