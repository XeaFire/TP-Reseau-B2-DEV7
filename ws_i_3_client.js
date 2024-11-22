function hello() {
    const uri = "ws://5.5.5.11:8765";
    const websks = new WebSocket(uri);
    const userInput = prompt("What's your name?")

    websks.onopen = () => {
        websks.send(userInput);
    };

    websks.onmessage = (event) => {
        console.log(event.data);
        alert(event.data)
    };

    window.onbeforeunload = function () {
        websocket.onclose = function () { }; // disable onclose handler first
        websocket.close();
    };


}


hello()

