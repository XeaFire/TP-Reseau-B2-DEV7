function hello() {
    const uri = "ws://5.5.5.11:8765";
    const websks = new WebSocket(uri);

    websks.onopen = () => {
        websks.send(userInput);
    };

    websks.onmessage = (event) => {
        console.log(event.data);
        alert(event.data)
    };

    let userInput = prompt("What's your name?")

    while (true) {
        userInput = prompt("Chatbox : ")
        console.log("benn")
        websks.send(userInput);

    }


}


hello()

