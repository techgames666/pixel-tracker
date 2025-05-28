from flask import Flask, request, redirect
import requests
import time

app = Flask(__name__)

# 🔥 Dados do seu Pixel
PIXEL_ID = '670749832539557'
ACCESS_TOKEN = 'EAAYzzRkeKZAoBO9OghX47kcCTzBEfu1SQZCIoU3BBxUwZC0MYTeJGVvYlmwXF7bByJX30ZBRgRPSXzSINa7OnNW5EuC25Ko33hQZAC835crG2CMg0xEyuIkpudKGOyl1Bi6npZAzrbW9A0O3aC39arnPLP3BznzIEUebqZCKx05fkBh5ZCp4IPJ8rovX9WmCNSUPdwZDZD'

# 🔗 Página de destino
DESTINO = 'https://techgamesbr.site/products/mini-game-portatil-switch-ps2-psp-nitendo-e-varios-consoles-integrado-ultimas-unidades'


# ✅ Rota principal (simples, sem código)
@app.route('/')
def home():
    enviar_evento('ViewContent', 'pagina_principal')
    return redirect(DESTINO)


# 🎯 Rota com código identificador
@app.route('/link/<codigo>')
def rastreador(codigo):
    enviar_evento('ViewContent', codigo)
    return redirect(DESTINO)


# 🚀 Função para enviar evento para o Pixel do Facebook
def enviar_evento(evento_nome, conteudo):
    try:
        user_ip = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        event_time = int(time.time())

        url = f'https://graph.facebook.com/v19.0/{PIXEL_ID}/events'
        payload = {
            'data': [
                {
                    'event_name': evento_nome,
                    'event_time': event_time,
                    'user_data': {
                        'client_ip_address': user_ip,
                        'client_user_agent': user_agent,
                    },
                    'custom_data': {
                        'content_name': conteudo,
                        'content_category': 'pagina_de_vendas'
                    },
                    'action_source': 'website'
                }
            ],
            'access_token': ACCESS_TOKEN
        }

        response = requests.post(url, json=payload)

        if response.status_code == 200:
            print(f'✅ Evento enviado com sucesso: {conteudo}')
        else:
            print(f'❌ Erro ao enviar evento: {response.text}')

    except Exception as e:
        print(f'❌ Erro geral ao enviar evento: {e}')


# 🚦 Rodar localmente (opcional)
if __name__ == '__main__':
    app.run(debug=True)
