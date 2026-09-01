from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PROXY DESATIVADA</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                background: #07070d;
                color: #fff;
                font-family: 'Segoe UI', system-ui, sans-serif;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
            }
            h1 {
                font-size: 1.8rem;
                font-weight: 600;
                letter-spacing: 1px;
            }
            p {
                margin-top: 12px;
                color: rgba(255,255,255,0.5);
                font-size: 0.95rem;
            }
        </style>
    </head>
    <body>
        <div>
            <h1>PROXY DESATIVADA</h1>
            <p>POR @LEO MODZ</p>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)