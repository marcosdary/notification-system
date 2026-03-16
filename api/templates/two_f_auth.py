from jinja2 import Template

class TwoFAuth:
    def __init__(self, coding: int, expiresAt: str):
        self._coding = coding
        self._expiresAt = expiresAt

    def get_template(self):
        html = """
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
        <meta charset="UTF-8">
        <title>Verificação de Segurança</title>

        <style>
        body{
            font-family:Arial;
            background:#f4f6f9;
        }

        .container{
            max-width:450px;
            margin:50px auto;
            background:white;
            padding:30px;
            border-radius:10px;
            text-align:center;
        }

        .code{
            font-size:32px;
            letter-spacing:6px;
            margin:20px 0;
            font-weight:bold;
            color:#333;
        }

        .footer{
            font-size:12px;
            color:#888;
        }
        </style>
        </head>

        <body>

        <div class="container">

        <h2>Verificação em Duas Etapas</h2>

        <p>Use o código abaixo para continuar o login:</p>

        <div class="code">
        {{ code }}
        </div>

        <p>Este código expira em {{ expires }}</p>

        <div class="footer">
        Nunca compartilhe este código com ninguém.
        </div>

        </div>

        </body>
        </html>
        """

        template = Template(html)

        return template.render(
            code=self._coding,
            expires=self._expiresAt
        )
    