// -----CONSTANTES GERAIS AUTH-------
const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');
const logoutButton = document.getElementById('logoutButton');
// ----- FIM CONSTS GERAIS AUTH -------

// ----- CONSTS GOALS -----
const formGoal = document.getElementById('formGoal');
const listGoals = document.getElementById('listGoals');
//Variavel de controle de edição
let goalEmEdicaoId = null;
const goalTitulo = document.getElementById('goalTitulo');
const goalDescricao = document.getElementById('goalDescricao');
const submitGoalButton = document.getElementById('submitGoalButton');
const cancelEditButton = document.getElementById('cancelEditButton');
const goalMessage = document.getElementById('goalMessage')
// ----- FIM CONST GOALS ------

// ---- FUNCOES AUTH ----
//Login
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
//Registro
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
//Logout
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
// ---- FIM FUNCOES AUTH ----


// --- INICIO FUNCOES CRUD GOALS ----
//Função de formulario objetivo, criar e editar;
if (formGoal) {
    formGoal.addEventListener("submit", async function(event){
        event.preventDefault()

        const dados = {
            titulo: goalTitulo.value.trim(),
            descricao: goalDescricao.value.trim()
        };

        const estaEditando = goalEmEdicaoId !== null;

        const url = estaEditando
            ?`/update_goal/${goalEmEdicaoId}`
            :'/create_goal';

        const metodo = estaEditando
            ?'PATCH'
            :'POST';

        
        try{

            const resposta = await fetch(url, {
                method: metodo,
                headers: {
                    "Content-type": "application/json"
                },
                body: JSON.stringify(dados)

            });

            const resultado = await resposta.json()
            if (!resposta.ok) {
                // throw interrompe o bloco try e envia o erro ao catch
                throw new Error(resultado.Erro ||
                     "Não foi possível salvar o objetivo" 
                );
            }

            goalMessage.textContent = resultado.mensagem;

            finalizarFormGoal();
            
            // faz uma consulta e recarrega a lista.
            await carregarGoals();

        } catch (erro) {
            goalMessage.textContent = erro.message;
            console.error(erro);
        }
    });
}
// ediçao
if (listGoals) {
    carregarGoals();

    listGoals.addEventListener("click", function(event) {
        const editarButton = event.target.closest(".editarGoal");

        if(!editarButton) {
            return;
        }
        // closest percorre a arvore dom ate encotrar o elemento selecionado
        // recebe o objetivo especifico atraves da classe e do click de edicao
        // basicamente recebe o elemnto objetivo selecionado
        const itemGoal = editarButton.closest('.verGoal')

        // buscando um elemento especifico com query selector dentro de itemgoal
        const tituloAtual = itemGoal.querySelector('.tituloGoal').textContent;

        const descricaoAtual = itemGoal.querySelector('.descricaoGoal').textContent;

        goalEmEdicaoId = editarButton.dataset.goalId;

        // goaltitulo se refere ao id de input do formulario
        goalTitulo.value = tituloAtual;
        goalDescricao.value = descricaoAtual;


        submitGoalButton.textContent = "Salvar alterações";

        cancelEditButton.hidden = false;

        goalMessage.textContent = "Editando Objetivo"

        // coloca um destaque no elemento
        goalTitulo.focus();

        // rolar a pagina até o formulario. Sendo smooth(suave), e start significa até o começo do elemento selcionado.
        formGoal.scrollIntoView({
            behavior: 'smooth',
            block: "start"
        });
    });
}
//deletar
if (listGoals) {
    listGoals.addEventListener("click", async function(event){
        const deletarButton = event.target.closest('.deletarGoal');

        if (!deletarButton) {
            return;
        }

        const listgoalMessage = document.getElementById('listgoalMessage');
        
        try {
            const goalId = deletarButton.dataset.goalId;

            const confirmou = window.confirm("Deseja realmente excluir este objetivo?");

            if (!confirmou) {
                return;
            }


            const resposta = await fetch(`/delete_goal/${goalId}`, {
                method: 'POST'
            });

            const resultado = await resposta.json();

            if (!resposta.ok) {
                throw new Error(resultado.Erro || "Não foi possível excluir");
            }

            if (listgoalMessage) {

            listgoalMessage.textContent = resultado.mensagem;
            }

            if (String(goalEmEdicaoId) === String(goalId)) {
                finalizarFormGoal();
            }

            await carregarGoals();

        } catch(erro){
            listgoalMessage.textContent = erro.message;
            }
        console.error(erro);
    });
}

if (cancelEditButton) {
    cancelEditButton.addEventListener("click", function()
        {
            finalizarFormGoal();
            goalMessage.textContent = "";
        }
    );
}
// ---- FIM FUNCOES GOALS ----

// --- INICIO FUNCOES SEM LISTENER ---
function redirecionarDepois(destino, tempo = 650) { 
    setTimeout(function(){
        window.location.href = destino;
    }, tempo);

}
//Funçao para listar os gols criando elemetnos html e tags css
async function carregarGoals() {
    const listGoals = document.getElementById('listGoals');

    if (!listGoals) {
        return;
    }

    try {
        const resposta = await fetch('/list_goal', {
            method: "GET"

        });

        const resultado = await resposta.json()

        if (!resposta.ok) {
            throw new Error(resultado.Erro);
        }

        listGoals.innerHTML = "";

        resultado.lista.forEach(function(goal){
            const item = document.createElement('li');
            item.classList.add('verGoal');
            item.dataset.goalId = goal.id;

            const titulo = document.createElement('span');
            titulo.classList.add('tituloGoal');
            titulo.textContent = goal.titulo;

            const descricao = document.createElement('span');
            descricao.classList.add('descricaoGoal')
            descricao.textContent = goal.descricao || "";

            const editarButton = document.createElement("button");
            editarButton.type = "button";
            editarButton.classList.add("editarGoal");
            editarButton.dataset.goalId = goal.id;
            editarButton.textContent = "Editar";

            const deletarButton = document.createElement("button");
            deletarButton.type = "button";
            deletarButton.classList.add("deletarGoal");
            deletarButton.dataset.goalId = goal.id;
            deletarButton.textContent = "Deletar";

            item.append(
                titulo,
                " | ",
                descricao,
                " | ",
                editarButton,
                " | " ,
                deletarButton
            );

            listGoals.appendChild(item);
        });
    } catch (erro) {
        const listgoalMessage = document.getElementById('listgoalMessage');

        if (listgoalMessage){
        listgoalMessage.textContent = erro.message;
        }
        console.error(erro);
    }

}

function finalizarFormGoal() {
    goalEmEdicaoId = null;
    formGoal.reset();

    submitGoalButton.textContent = "Criar"
    cancelEditButton.hidden = true;
}
// ---- FIM ----




// const btnDeletar = document.getElementsByClassName('deletarGoal')

// if (btnDeletar) {
//     formGoal.document.addEventListener("click", async function(event) {
//         event.preventDefault()

//     });
// }
 