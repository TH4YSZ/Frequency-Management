function mostrar() {
    const senhaInput = document.querySelector('input[name="senha"]');
    const btnSenha = document.getElementById('btnSenha');

    if (senhaInput.type === 'password') {

        senhaInput.type = 'text';
        btnSenha.classList.remove('bi-eye-slash');
        btnSenha.classList.add('bi-eye');

    } else {

        senhaInput.type = 'password';
        btnSenha.classList.remove('bi-eye');
        btnSenha.classList.add('bi-eye-slash');
    }
}