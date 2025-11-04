# Download de Chats do Telegram

Este script em Python permite baixar todas as mensagens e arquivos de chats públicos do Telegram, utilizando a biblioteca Telethon.

---

## Requisitos

Antes de executar o script, instale as dependências necessárias:

```bash
pip install telethon
```

---

## Credenciais da API

Para usar o script, é necessário obter as credenciais de API do Telegram:

1. Acesse [https://my.telegram.org](https://my.telegram.org)
2. Clique em "API Development Tools"
3. Copie o `api_id` e o `api_hash` gerados
4. Substitua esses valores no código do script nas variáveis:

   ```python
   api_id = 12345678
   api_hash = "000000000000000000000000000000"
   ```

---

## Como usar

1. Clone ou copie o script Python.
2. Verifique se a variável `output_dir` está configurada corretamente para o local onde os arquivos e mensagens serão salvos:

   ```python
   output_dir = "/run/media/nox/backup"
   ```
3. Adicione os links dos chats que deseja baixar na lista `chat_urls`:

   ```python
   chat_urls = [
       "https://t.me/chat1",
       "https://t.me/chat2"
   ]
   ```
4. Execute o script:

   ```bash
   python telegram_backup.py
   ```

Durante a primeira execução, o script solicitará o número de telefone associado à sua conta do Telegram e o código de autenticação recebido por mensagem.

---

## Saída

O script cria uma pasta para cada chat dentro do diretório especificado, contendo:

* Um arquivo `messages.jsonl` com todas as mensagens.
* Todos os arquivos de mídia (imagens, vídeos, documentos, etc.) baixados.

Estrutura de saída:

```
/run/media/user/storage/
├── chat1/
│   ├── messages.jsonl
│   ├── arquivo1.jpg
│   ├── arquivo2.pdf
├── chat2/
│   ├── messages.jsonl
│   ├── video1.mp4
```

---

## Limites e Considerações

* O Telegram impõe limites de requisições por minuto, então o script pode pausar automaticamente para respeitar essas restrições.
* Todos os arquivos e mensagens disponíveis serão baixados, sem limite de tamanho ou quantidade.
* Caso o chat seja privado, é necessário que a conta esteja adicionada ao grupo ou canal.

---

## Licença

Este script é livre para uso e modificação em qualquer finalidade legítima e educacional.
