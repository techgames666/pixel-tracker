from flask import Flask, request, redirect
from scraper.scraper import raspar_dados
import requests
import time

app = Flask(__name__)

# 🔗 Link de destino (sua página de vendas)
DESTINO = 'https://techgamesbr.site/products/mini-game-portatil-switch-ps2-psp-nitendo-e-varios-consoles-integrado-ultimas-unidades'

# 🎯 Dados do Pixel
PIXEL_ID = '670749832539557'
ACCESS_TOKEN = 'EAAYzzRkeKZAoBO9OghX47kcCTzBEfu1SQZCIoU3BBxUwZC0MYTeJGVvYlmwXF7bByJX30ZBRgRPSXzSINa7OnNW5EuC25Ko33hQZAC835crG2CMg0xEyuIkpudKGOyl1Bi6npZAzrbW9A0O3aC39arnPLP3BznzIEUebqZCKx05fkBh5ZCp4IPJ8rovX9WmCNSUPdwZDZD'

# 🚀 Rota raspagem - Raspagem bruta
@app.route('/raspar', methods=['POST'])
def raspar_pagina():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return {'error': 'URL é obrigatória'}, 400

    resultado = raspar_dados(url)

    if resultado.get('error'):
        return resultado, 500
    else:
        return resultado, 200


# 🚀 Rota principal - Redirecionamento simples
@app.route('/')
def home():
    return redirect(DESTINO)

# 🚀 Rota com rastreamento
@app.route('/link/<codigo>')
def rastrear(codigo):
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
        print('✅ Evento enviado com sucesso.')
    else:
        print('❌ Erro ao enviar evento:', response.text)

    return redirect(DESTINO)

# 🔥 Execução local (Render ignora essa linha)
if __name__ == '__main__':
    app.run(debug=True)

#CÓDIGO DE RASPAGEM E COLETA DE DADOS ABAIXO

from flask import Flask, request, jsonify, redirect
import requests
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

# Seus dados do pixel Facebook
PIXEL_ID = '670749832539557'
ACCESS_TOKEN = 'EAAYzzRkeKZAoBO9OghX47kcCTzBEfu1SQZCIoU3BBxUwZC0MYTeJGVvYlmwXF7bByJX30ZBRgRPSXzSINa7OnNW5EuC25Ko33hQZAC835crG2CMg0xEyuIkpudKGOyl1Bi6npZAzrbW9A0O3aC39arnPLP3BznzIEUebqZCKx05fkBh5ZCp4IPJ8rovX9WmCNSUPdwZDZD'

# Link padrão para redirecionar (pode mudar depois)
DESTINO = 'https://techgamesbr.site/products/mini-game-portatil-switch-ps2-psp-nitendo-e-varios-consoles-integrado-ultimas-unidades'

def enviar_evento_facebook(codigo, dados_custom):
    url = f'https://graph.facebook.com/v19.0/{PIXEL_ID}/events'
    payload = {
        'data': [
            {
                'event_name': 'ViewContent',
                'event_time': int(time.time()),
                'user_data': {
                    'client_ip_address': request.remote_addr,
                    'client_user_agent': request.headers.get('User-Agent'),
                },
                'custom_data': dados_custom,
                'action_source': 'website'
            }
        ],
        'access_token': ACCESS_TOKEN
    }
    response = requests.post(url, json=payload)
    return response

@app.route('/')
def redirect_page():
    # Redireciona para o link principal
    return redirect(DESTINO)

@app.route('/link/<codigo>')
def rastreador(codigo):
    # Exemplo já feito - envia evento para pixel com 'codigo'
    dados_custom = {
        'content_name': codigo,
        'content_category': 'pagina_de_vendas'
    }
    response_fb = enviar_evento_facebook(codigo, dados_custom)

    if response_fb.status_code == 200:
        print('Evento enviado com sucesso para o Facebook.')
    else:
        print('Erro ao enviar evento:', response_fb.text)

    return redirect(DESTINO)

@app.route('/raspar', methods=['POST'])
def raspar_pagina():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL é obrigatória'}), 400

    try:
        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            return jsonify({'error': f'Erro ao acessar URL: {res.status_code}'}), 400
        
        soup = BeautifulSoup(res.text, 'html.parser')
        
        titulo = soup.title.string if soup.title else 'Sem título'

        preco_tag = soup.find(class_='price')
        preco = preco_tag.get_text(strip=True) if preco_tag else 'Preço não encontrado'

        dados_custom = {
            'content_name': titulo,
            'value': preco,
            'content_category': 'pagina_de_vendas'
        }

        response_fb = enviar_evento_facebook(titulo, dados_custom)

        if response_fb.status_code == 200:
            return jsonify({'message': 'Evento enviado com sucesso', 'titulo': titulo, 'preco': preco})
        else:
            return jsonify({'error': 'Erro ao enviar evento para o Facebook', 'details': response_fb.text}), 500

    except Exception as e:
        return jsonify({'error': f'Erro ao processar URL: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
