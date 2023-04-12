from fastapi import FastAPI, HTTPException
from bs4 import BeautifulSoup
import requests
from models import Item

app = FastAPI()

@app.get('/')
async def index():
    return '1 - Essa API recebe como parâmetro uma URL de uma nota fiscal 2 - Realiza o scrapping do seus itens 3 - E retorna em formato JSON todos os dados da nota'

@app.get('/itens-da-nota/{chave_acesso}')
async def itens_da_nota(chave_acesso: str):
    url = "http://nfe.sefaz.ba.gov.br/servicos/nfce/qrcode.aspx?p=" + chave_acesso
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'id': 'tabResult'})
    txtTit_elements = table.find_all('span', {'class': 'txtTit'})
    RvlUnit_elements = table.find_all('span', {'class': 'RvlUnit'})
    txtTit_content = [element.get_text() for element in txtTit_elements]
    RvlUnit_content = [element.get_text().split(".:")[-1] for element in RvlUnit_elements]
    itens_da_nota = []
    for i in range(len(txtTit_content)):
        nome_produto = txtTit_content[i]
        valor = RvlUnit_content[i]
        item = Item(nome_produto=nome_produto, valor=valor)
        itens_da_nota.append(item)
    response = {'itens': []}
    for idn in itens_da_nota:
        response['itens'].append({'nome_produto': idn.nome_produto, 'valor': idn.valor.split()[0]})
    return response
