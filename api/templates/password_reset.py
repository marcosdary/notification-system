class PasswordReset:
    def __init__(self, link: str, expiresAt: str):
        self._link = link
        self._expiresAt = expiresAt

    def template(self):
        return """
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
        <meta charset="UTF-8">
        <title>Redefinição de Senha</title>

        <style>
        body{
            font-family: Arial, sans-serif;
            background:#f4f6f9;
            margin:0;
            padding:0;
        }

        .container{
            max-width:500px;
            margin:50px auto;
            background:white;
            padding:30px;
            border-radius:10px;
            text-align:center;
            box-shadow:0 4px 10px rgba(0,0,0,0.1);
        }

        h1{
            color:#333;
        }

        p{
            color:#555;
        }

        .button{
            display:inline-block;
            margin-top:20px;
            padding:14px 25px;
            background:#4CAF50;
            color:white;
            text-decoration:none;
            border-radius:6px;
            font-weight:bold;
        }

        .footer{
            margin-top:25px;
            font-size:12px;
            color:#888;
        }
        </style>
        </head>

        <body>

        <div class="container">

        <h1>Redefinir Senha</h1>

        <p>Recebemos uma solicitação para redefinir sua senha.</p>

        <p>Clique no botão abaixo para criar uma nova senha:</p>

        <a class="button" href="{%s}">Redefinir Senha</a>

        <div class="footer">
        Se você não solicitou essa alteração, ignore este email.
        </div>

        <p>Este código expira em {%s}.</p>

        </div>

        </body>
        </html>
        """.format(self._link, self._expiresAt)