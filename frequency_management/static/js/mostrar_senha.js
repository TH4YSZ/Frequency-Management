function mostrar() {
    var inputPass = document.getElementById('id_password');
    var btnShowPass = document.getElementById('btnSenha');

    if (inputPass.type === 'password') {
        inputPass.setAttribute('type', 'text');
        btnShowPass.classList.replace('bi-eye', 'bi-eye-slash');
    } else {
        inputPass.setAttribute('type', 'password');
        btnShowPass.classList.replace('bi-eye-slash', 'bi-eye');
    }
}
