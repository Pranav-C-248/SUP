function login() {
    var username = document.getElementById('loginUsername').value;
    var password = document.getElementById('loginPassword').value;

    var status=eel.loginHandle(username, password)
    console.log("login status: ",status)

};
