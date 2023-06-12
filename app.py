from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests
from models import Item, Loja, NotaFiscal
import json
from datetime import datetime
import re
from lxml import html

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
    header = soup.find('div', {'class': 'txtCenter'})
    info = soup.find('div', {'id': 'infos'})
    tree = html.fromstring(response.content)

    #LOJA
    #nome_da_loja 
    nome_da_loja_element = header.find('div', {'class': 'txtTopo'}) 
    nome_da_loja_content = nome_da_loja_element.text
    nome_da_loja = nome_da_loja_content
    #cnpj
    cnpj_element = header.find_all('div', {'class': 'text'})[0]
    cnpj_content = cnpj_element.text.replace("\r", "").replace("\n", "").replace("\t", "").replace("CNPJ:", "").replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
    cnpj = cnpj_content
    # #endereco
    endereco_element = header.find_all('div', {'class': 'text'})[1]
    endereco_content = endereco_element.text.replace('\r', '').replace('\n', '').replace('\t', '').strip()
    endereco_content = endereco_content.replace(',,', ', ').replace(',', ', ')
    endereco = endereco_content

    loja = Loja(nome_da_loja, cnpj, endereco, nota_fiscal=[123])

    #NOTA FISCAL
    #chave de acesso
    chave_de_acesso_element = info.find('span', {'class': 'chave'})
    chave_de_acesso_content = chave_de_acesso_element.text.replace(" ", "")
    numero = chave_de_acesso_content

    #data de emissão
    # emissao_element = soup.find("strong", text=re.compile(" Emissão: "))
    # data_emissao = re.search(r"\d{2}/\d{2}/\d{4}", emissao_element.next_sibling.strip()).group()
    # data_emissao = data_emissao.replace("/", "-")
    # data_emissao = datetime.strptime(data_emissao, "%d-%m-%Y").strftime("%m-%d-%Y")

    #data de emissão 2
    padrao = r"(\d{2}/\d{2}/\d{4})"
    match = re.search(padrao, info.text)
    if match:
        data_emissao = match.group(1)
        data_emissao = datetime.strptime(data_emissao, "%d/%m/%Y").strftime("%m-%d-%Y")
        print(data_emissao)
    else:
        print("Data de emissão não encontrada.")


    #valor total
    valor_total_element = tree.xpath('//*[@id="linhaTotal"][2]/span')
    valor_total_content = valor_total_element[0].text.replace(",", ".")
    valor_total = valor_total_content

    nf = NotaFiscal(numero, data_emissao, valor_total, loja)
    
    #ITENS
    # nome_do_produto
    txtTit_elements = table.find_all('span', {'class': 'txtTit'}) 
    txtTit_content = [element.get_text() for element in txtTit_elements]
    # codigo_do_item_na_loja
    RCod_elements = table.find_all('span', {'class': 'RCod'}) 
    RCod_content = [element.get_text().split(":")[-1].strip()[:-1] for element in RCod_elements]
    # quantidade
    Rqtd_elements = table.find_all('span', {'class': 'Rqtd'}) 
    Rqtd_content = [element.get_text().split(".:")[-1].replace(",", ".") for element in Rqtd_elements]
    # unidade_de_medida
    RUN_elements = table.find_all('span', {'class': 'RUN'}) 
    RUN_content = [element.get_text().split(":")[-1] for element in RUN_elements]
    # valor_unitario
    RvlUnit_elements = table.find_all('span', {'class': 'RvlUnit'}) 
    RvlUnit_content = [element.get_text().split(".:")[-1].replace(",", ".") for element in RvlUnit_elements]
    # valor_total
    valor_elements = table.find_all('span', {'class': 'valor'}) 
    valor_content = [element.get_text().replace(",", ".") for element in valor_elements]
    
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

    # Transforma a nota fiscal em um dicionário para serializar para JSON
    nota_fiscal_dict = {}
    itens_list = []

    for i, item in enumerate(itens_da_nota):
        item_dict = {
            "nome_do_produto": item.nome_do_produto,
            "codigo_do_item_na_loja": item.codigo_do_item_na_loja,
            "quantidade": item.quantidade,
            "unidade_de_medida": item.unidade_de_medida,
            "valor_unitario": item.valor_unitario,
            "valor_total": item.valor_total,
            "nota_fiscal_chave_de_acesso": nf.numero,
        }
        itens_list.append(item_dict)

    nota_fiscal_dict = {
        "nota_fiscal":{
            "chave_de_acesso": nf.numero,
            "data_emissao": nf.data_emissao,
            "valor_total": nf.valor_total
        },
        "loja": {
            "nome_da_loja": loja.nome_da_loja,
            "cnpj": loja.cnpj,
            "endereco": loja.endereco
        },
        "itens": itens_list
    }

    return jsonify(nota_fiscal_dict)

if __name__ == '__main__':
    app.run()