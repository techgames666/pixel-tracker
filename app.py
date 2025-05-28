from flask import Flask, request, redirect
import requests
import time

app = Flask(__name__)

PIXEL_ID = '670749832539557'  # Substitua pelo seu Pixel ID
ACCESS_TOKEN = 'EAAYzzRkeKZAoBO9OghX47kcCTzBEfu1SQZCIoU3BBxUwZC0MYTeJGVvYlmwXF7bByJX30ZBRgRPSXzSINa7OnNW5EuC25Ko33hQZAC835crG2CMg0xEyuIkpudKGOyl1Bi6npZAzrbW9A0O3aC39arnPLP3BznzIEUebqZCKx05fkBh5ZCp4IPJ8rovX9WmCNSUPdwZDZD'  # Seu access token
DESTINO = 'https://techgamesbr.site/products/mini-game-portatil-switch-ps2-psp-nitendo-e-varios-consoles-integrado-ultimas-unidades🔥'  # Página de vendas

@app.route('/')
def redirect_page():
    return redirect(DESTINO)

@app.route('/link/<codigo>')
def rastreador(codigo):
    user_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    event_time = int(time.time())

    print(f'🟢 Clique detectado! IP: {user_ip}, User-Agent: {user_agent}, Código: {codigo}')

    url = f'https://graph.facebook.com/v19.0/{PIXEL_ID}/events'
    payload = {
        'data': [
            {
                'event_name': 'ViewContent',
                'event_time': event_time,
                'user_data': {
                    'client_ip_address': user_ip,
                    'client_user_agent': user_agent,
                },
                'custom_data': {
                    'content_name': codigo,
                    'content_category': 'pagina_de_vendas'
                },
                'action_source': 'website'
            }
        ],
        'access_token': ACCESS_TOKEN
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print('✅ Evento enviado com sucesso para o Facebook.')
    else:
        print('❌ Erro ao enviar evento:', response.text)

    return redirect(DESTINO)

if __name__ == '__main__':
    app.run(debug=True)
