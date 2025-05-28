import requests
from bs4 import BeautifulSoup

def raspar_dados(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Garante que deu certo (200 OK)

        soup = BeautifulSoup(response.text, 'html.parser')

        # Exemplo de coleta de dados
        titulo = soup.title.string if soup.title else 'Sem título'

        # Captura a meta description (se tiver)
        description = soup.find("meta", attrs={"name": "description"})
        descricao = description['content'] if description else 'Sem descrição'

        # Captura o preço (ajuste conforme o site)
        preco = soup.find('span', class_='price')  # Trocar classe se necessário
        preco = preco.text.strip() if preco else 'Sem preço encontrado'

        dados = {
            'titulo': titulo,
            'descricao': descricao,
            'preco': preco,
        }

        print("🟢 Dados capturados:", dados)
        return dados

    except Exception as e:
        print("❌ Erro ao raspar dados:", e)
        return None
