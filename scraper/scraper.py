import requests
from bs4 import BeautifulSoup

def raspar_dados(url):
    try:
        res = requests.get(url, timeout=10)

        if res.status_code != 200:
            return {'error': f'Erro ao acessar URL: {res.status_code}'}

        soup = BeautifulSoup(res.text, 'html.parser')

        titulo = soup.title.string if soup.title else 'Sem título'

        preco_tag = soup.find(class_='price')
        preco = preco_tag.get_text(strip=True) if preco_tag else 'Preço não encontrado'

        return {
            'titulo': titulo,
            'preco': preco
        }

    except Exception as e:
        return {'error': f'Erro ao processar URL: {str(e)}'}
