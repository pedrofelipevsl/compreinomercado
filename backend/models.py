from datetime import datetime
from typing import List, Optional

class Loja:
    def __init__(self, nome: str, cnpj: str, endereco: str, nota_fiscal: List['NotaFiscal'] = None):
        self.nome = nome
        self.cnpj = cnpj
        self.endereco = endereco
        self.nota_fiscal = nota_fiscal or []

    def to_dict(self):
        return {
            "nome": self.nome,
            "cnpj": self.cnpj,
            "endereco": self.endereco,
            "nota_fiscal": [nf.to_dict() for nf in self.nota_fiscal],
        }

class Item:    
    def __init__(self, nome_do_produto, codigo_do_item_na_loja, quantidade, unidade_de_medida, valor_unitario, valor_total, nota_fiscal_id):
        self.nome_do_produto = nome_do_produto
        self.codigo_do_item_na_loja = codigo_do_item_na_loja
        self.quantidade = quantidade
        self.unidade_de_medida = unidade_de_medida
        self.valor_unitario = valor_unitario
        self.valor_total = valor_total
        self.nota_fiscal_id = nota_fiscal_id

    def to_dict(self):
        return {
            "id": self.id,
            "nome_do_produto": self.nome_do_produto,
            "codigo_do_item_na_loja": self.codigo_do_item_na_loja,
            "quantidade": self.quantidade,
            "unidade_de_medida": self.unidade_de_medida,
            "valor_unitario": self.valor_unitario,
            "valor_total": self.valor_total,
            "nota_fiscal_id": self.nota_fiscal_id
        }

class NotaFiscal:
    def __init__(self, numero: str, data_emissao: datetime, valor_total: float, loja: Optional[Loja] = None, itens: Optional[List[Item]] = None):
        self.numero = numero
        self.data_emissao = data_emissao
        self.valor_total = valor_total
        self.loja = loja
        self.itens = itens or []

    def adicionar_item(self, item: Item):
        self.itens.append(item)

    def to_dict(self):
        return {
            "numero": self.numero,
            "data_emissao": self.data_emissao.isoformat(),
            "valor_total": self.valor_total,
            "loja": self.loja.to_dict() if self.loja else None,
            "itens": [item.to_dict() for item in self.itens],
        }
