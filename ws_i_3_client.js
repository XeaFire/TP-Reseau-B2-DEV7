function hello() {
    const uri = "ws://5.5.5.11:8765";
    const websks = new WebSocket(uri);
    let userInput = prompt("What's your name?")

    websks.onopen = () => {
        websks.send(userInput);
    };

    websks.onmessage = (event) => {
        console.log(event.data);
        alert(event.data)
    };

    while (true) {
        userInput = prompt("Chatbox : ")
        websks.send(userInput);
        console.log("benn")
    }


}


hello()

