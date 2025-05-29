from flask import Flask, request, redirect, jsonify, render_template, flash, url_for
import requests
from bs4 import BeautifulSoup
import time
import os

app = Flask(__name__)
app.secret_key = 'uma_chave_super_secreta_aqui'  # necessário para flash funcionar

# Configurações via variáveis de ambiente
config = {
    'PIXEL_ID': os.getenv('PIXEL_ID', '670749832539557'),
    'ACCESS_TOKEN': os.getenv('ACCESS_TOKEN', 'EAAYzzRkeKZAoBO9OghX47kcCTzBEfu1SQZCIoU3BBxUwZC0MYTeJGVvYlmwXF7bByJX30ZBRgRPSXzSINa7OnNW5EuC25Ko33hQZAC835crG2CMg0xEyuIkpudKGOyl1Bi6npZAzrbW9A0O3aC39arnPLP3BznzIEUebqZCKx05fkBh5ZCp4IPJ8rovX9WmCNSUPdwZDZD'),
    'DESTINO': os.getenv('DESTINO', 'https://techgamesbr.site/products/mini-game-portatil-switch-ps2-psp-nitendo-e-varios-consoles-integrado-ultimas-unidades')
}

def enviar_evento_facebook(codigo, dados_custom):
    url = f'https://graph.facebook.com/v19.0/{config["PIXEL_ID"]}/events'
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
        'access_token': config['ACCESS_TOKEN']
    }
    response = requests.post(url, json=payload)
    return response

@app.route('/')
def home():
    if not config['DESTINO']:
        return "URL de destino não configurada", 500
    return redirect(config['DESTINO'])

@app.route('/link/<codigo>')
def rastrear(codigo):
    dados_custom = {
        'content_name': codigo,
        'content_category': 'pagina_de_vendas'
    }
    response_fb = enviar_evento_facebook(codigo, dados_custom)

    if response_fb.status_code == 200:
        print('Evento enviado com sucesso para o Facebook.')
    else:
        print('Erro ao enviar evento:', response_fb.text)

    if not config['DESTINO']:
        return "URL de destino não configurada", 500
    return redirect(config['DESTINO'])

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

@app.route('/painel', methods=['GET'])
def painel():
    # Apenas mostra as configs atuais (não salva mais)
    mensagens = []
    if not config['PIXEL_ID']:
        mensagens.append("PIXEL_ID não configurado.")
    if not config['ACCESS_TOKEN']:
        mensagens.append("ACCESS_TOKEN não configurado.")
    if not config['DESTINO']:
        mensagens.append("DESTINO não configurado.")
    return render_template('painel.html', config=config, mensagens=mensagens)

if __name__ == '__main__':
    app.run(debug=False)
