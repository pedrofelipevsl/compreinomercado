from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests
from models import Item, Loja, NotaFiscal
import json

app = Flask(__name__)

@app.route('/')
def index():
    return '1 - Essa API recebe como parâmetro uma URL de uma nota fiscal 2 - Realiza o scrapping do seus itens 3 - E retorna em formato JSON todos os dados da nota'

@app.route('/itens-da-nota/<chave_acesso>')
def itens_da_nota(chave_acesso):
    url = "http://nfe.sefaz.ba.gov.br/servicos/nfce/qrcode.aspx?p=" + chave_acesso
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'id': 'tabResult'})
    
    #scraping dos itens
    # nome_do_produto
    txtTit_elements = table.find_all('span', {'class': 'txtTit'}) 
    txtTit_content = [element.get_text() for element in txtTit_elements]
    # codigo_do_item_na_loja
    RCod_elements = table.find_all('span', {'class': 'RCod'}) 
    RCod_content = [element.get_text().split(":")[-1] for element in RCod_elements]
    # quantidade
    Rqtd_elements = table.find_all('span', {'class': 'Rqtd'}) 
    Rqtd_content = [element.get_text().split(".:")[-1] for element in Rqtd_elements]
    # unidade_de_medida
    RUN_elements = table.find_all('span', {'class': 'RUN'}) 
    RUN_content = [element.get_text().split(":")[-1] for element in RUN_elements]
    # valor_unitario
    RvlUnit_elements = table.find_all('span', {'class': 'RvlUnit'}) 
    RvlUnit_content = [element.get_text().split(".:")[-1] for element in RvlUnit_elements]
    # valor_total
    valor_elements = table.find_all('span', {'class': 'valor'}) 
    valor_content = [element.get_text() for element in valor_elements]
    
    itens_da_nota = []
    for i in range(len(txtTit_content)):
        nome_do_produto = txtTit_content[i]
        codigo_do_item_na_loja = RCod_content[i]
        quantidade = Rqtd_content[i]
        unidade_de_medida = RUN_content[i]
        valor_unitario = RvlUnit_content[i]
        valor_total = valor_content[i]
        item = Item(nome_do_produto, codigo_do_item_na_loja, quantidade, unidade_de_medida, valor_unitario, valor_total, nota_fiscal_id=123)
        itens_da_nota.append(item)

    # Transforma a lista de itens em um dicionário para serializar para JSON
    items_dict = {}
    for i, item in enumerate(itens_da_nota):
        items_dict[i] = {
            "nome_do_produto": item.nome_do_produto,
            "codigo_do_item_na_loja": item.codigo_do_item_na_loja,
            "quantidade": item.quantidade,
            "unidade_de_medida": item.unidade_de_medida,
            "valor_unitario": item.valor_unitario,
            "valor_total": item.valor_total,
            "nota_fiscal_id": item.nota_fiscal_id
            }

    return jsonify(items_dict)

if __name__ == '__main__':
    app.run(debug=True)
