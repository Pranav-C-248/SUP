async function login() {
    var username = document.getElementById('loginUsername').value;
    var password = document.getElementById('loginPassword').value;

    try {
        var status = await eel.loginHandle(username, password)();
        console.log("Status:",status)
        if (status==true){
            console.log("Success")
            redirectToFriends()
        }
        else{
            const name=document.getElementById("loginUsername")
            name.textContent="Wrong Creds"
            const password=document.getElementById("loginPassword")
            password.textContent="Wrong Creds"
        }
    } catch (error) {
        console.error(error);
    }

};

function redirectToFriends() {
    window.location.replace('/frontpage.html');
}

