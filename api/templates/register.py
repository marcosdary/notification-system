class Register:
    def __init__(self, link: str) -> None:
        self._link = link

    def template(self):
        return """
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
        <meta charset="UTF-8">

        <style>
        body{
            font-family:Arial;
            background:#f4f6f9;
        }

        .container{
            max-width:500px;
            margin:50px auto;
            background:white;
            padding:30px;
            border-radius:10px;
            text-align:center;
        }

        .button{
            display:inline-block;
            padding:14px 25px;
            background:#2196F3;
            color:white;
            text-decoration:none;
            border-radius:6px;
            margin-top:20px;
        }

        </style>
        </head>

        <body>

        <div class="container">

        <h1>Bem-vindo!</h1>

        <p>Obrigado por criar sua conta.</p>

        <p>Para ativar seu cadastro clique no botão abaixo:</p>

        <a class="button" href="{%s}">
        Confirmar Cadastro
        </a>

        <p style="margin-top:25px;font-size:12px;color:#888;">
        Se você não criou esta conta, ignore este email.
        </p>

        </div>

        </body>
        </html>
        """.format(self._link)