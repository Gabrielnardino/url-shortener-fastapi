// static/script.js
document.addEventListener('DOMContentLoaded', () => {
    // Garante que estamos pegando os elementos corretos
    const urlForm = document.getElementById('url-form');
    const longUrlInput = document.getElementById('long_url_input');
    const customCodeInput = document.getElementById('custom_code_input');
    const resultDiv = document.getElementById('result');

    urlForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Impede o recarregamento da página

        // Pega os valores no momento do submit
        const longUrl = longUrlInput.value;
        const customCode = customCodeInput.value;

        resultDiv.textContent = 'Encurtando...';
        resultDiv.classList.remove('error');

        // Cria o corpo da requisição (payload)
        const requestBody = {
            long_url: longUrl,
        };

        // Adiciona a chave 'custom_code' APENAS se o campo não estiver vazio
        if (customCode.trim() !== '') {
            requestBody.custom_code = customCode;
        }

        try {
            const response = await fetch('/encurtar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody), // Envia o corpo da requisição
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Ocorreu um erro.');
            }

            const fullShortUrl = `${window.location.origin}/${data.short_code}`;
            resultDiv.innerHTML = `Link curto: <a href="${fullShortUrl}" target="_blank">${fullShortUrl}</a>`;

        } catch (error) {
            resultDiv.textContent = `Erro: ${error.message}`;
            resultDiv.classList.add('error');
        }
    });
});