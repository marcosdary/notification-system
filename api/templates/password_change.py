class PasswordChange:

    def template():
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

        .alert{
            color:#4CAF50;
            font-weight:bold;
            margin-top:15px;
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

        <h2>Senha Alterada</h2>

        <p class="alert">
        Sua senha foi alterada com sucesso.
        </p>

        <p>Se você realizou esta alteração, nenhuma ação é necessária.</p>

        <p>Se você não reconhece esta alteração, redefina sua senha imediatamente.</p>

        <div class="footer">
        © 2026 Seu Sistema
        </div>

        </div>

        </body>
        </html>
        """