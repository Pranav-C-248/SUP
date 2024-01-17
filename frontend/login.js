async function login() {
    var username = document.getElementById('loginUsername').value;
    var password = document.getElementById('loginPassword').value;

    try {
        var status = await eel.loginHandle(username, password)();
        console.log("Status:",status)
        console.log("asdasdasdadsasdadsasd")
    } catch (error) {
        console.error(error);
    }

};
