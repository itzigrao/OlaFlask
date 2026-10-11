const loginForm = document.getElementById('loginForm');


if (loginForm) {
    loginForm.addEventListener("submit", async function(event) {
        event.preventDefault(); //* impede o envio tradicional do formulário ou a navegacao href

        const email = document.getElementById("loginEmail").value;
        const senha = document.getElementById("loginSenha").value;


        const dados = {
            email: email,
            senha: senha

        };

        const resposta = await fetch("/login", {
            method: "POST",
            headers: {
                "content-type": "application/json"
            },
            body: JSON.stringify(dados)
        });

        const resultado = await resposta.json();

        if (resposta.ok) {
            const loginMessage = document.getElementById('loginMessage');
            loginMessage.textContent = resultado.mensagem;
            redirecionarDepois(resultado.redirect);
        } else {
            console.log(resultado.Erro)
            const loginMessage = document.getElementById("loginMessage");
            loginMessage.textContent = resultado.Erro;
        }

    });
}

const registerForm = document.getElementById('registerForm');

if (registerForm) {
    registerForm.addEventListener("submit", async function(event){
        event.preventDefault();

        const nome = document.getElementById('registerNome').value;
        const email = document.getElementById('registerEmail').value;
        const senha = document.getElementById('registerSenha').value;

        const dados = {
            nome: nome,
            email: email,
            senha: senha
        }

        //* await aguarda a resposta da requisição
        const resposta = await fetch("/register", {
            method: "POST",
            headers: {
                "Content-type": "application/json"
            },
            body: JSON.stringify(dados)
        });

        const resultado = await resposta.json();
        if (resposta.ok) {
            const registerMessage = document.getElementById('registerMessage')
            registerMessage.textContent = resultado.mensagem;
            redirecionarDepois(resultado.redirect);
        } else {
            console.log(resultado.Erro);
            const registerMessage = document.getElementById("registerMessage");
            registerMessage.textContent = resultado.Erro;
        }
    });
}

const logoutButton = document.getElementById('logoutButton');

if (logoutButton) {
    logoutButton.addEventListener("click", async function(event) {
        event.preventDefault();

        const resposta =  await fetch("/logout", {
            method: "POST"
        });

        const resultado = await resposta.json();

        if (resposta.ok) {
            window.location.href = resultado.redirect;
        } else {
            console.log(resultado.Erro)
            const logoutError = document.getElementById('logoutError')
            logoutError.textContent = resultado.Erro
        }
    })
}

function redirecionarDepois(destino, tempo = 650) { 
    setTimeout(function(){
        window.location.href = destino;
    }, tempo);

}


// function exibirMensagemRedirecionar(elemento, mensagem, destino) {
//     elemento.textContent = mensagem;

//     setTimeout(function(){
//         window.location.href = destino;
//     }, 1500);
// }

// const loginMessage = documento.getElementById('loginMessage');

// if (resposta.ok) {
//     exibirMensagemRedirecionar(
//         loginMessage,
//         resultado.mensagem,
//         resultado.redirect
//     ); 
// } else { 
//     loginMessage.textContent = resultado.Erro;
// }

// const registerMessage = document.getElementById('registerMessage');

// if (resposta.ok) {
//     exibirMensagemRedirecionar(
//         registerMessage,
//         resposta.mensagem,
//         resposta.redirect
//     );
// } else {
//     registerMessage.textContent = resultado.Erro;
// }

 