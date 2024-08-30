import csv
import requests
from app import db, Cliente  # Importe o banco de dados e o modelo Cliente
from flask import Flask

# Inicialize o app Flask
app = Flask(__name__)

# Função para consultar a API por CNPJ
def consultar_cnpj(cnpj):
    url = f"https://api.invertexto.com/v1/cnpj/{cnpj}?token=15158|CReshPRmmuMYkSDArod6UX83JifNCVmQ"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao consultar o CNPJ {cnpj}: {response.status_code}")
        return None

# Função para importar os clientes do CSV e inserir no banco de dados
def importar_clientes_csv(filepath):
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cnpj = row['CNPJ']
            codigo = row['Código']
            codigo_acesso = row['Código de Acesso']
            
            # Consultar os dados na API
            dados_cliente = consultar_cnpj(cnpj)
            if dados_cliente:
                cliente = Cliente(
                    id=codigo,  # Preservando o código como ID ou chave única
                    cnpj=cnpj,
                    codigo_acesso=codigo_acesso,
                    razao_social=dados_cliente.get('razao_social', ''),
                    nome_fantasia=dados_cliente.get('nome_fantasia', ''),
                    email=dados_cliente.get('email', ''),
                    telefone=dados_cliente.get('telefone1', ''),
                    logradouro=dados_cliente['endereco'].get('logradouro', ''),
                    numero=dados_cliente['endereco'].get('numero', ''),
                    complemento=dados_cliente['endereco'].get('complemento', ''),
                    bairro=dados_cliente['endereco'].get('bairro', ''),
                    municipio=dados_cliente['endereco'].get('municipio', ''),
                    uf=dados_cliente['endereco'].get('uf', ''),
                    cep=dados_cliente['endereco'].get('cep', '')
                )
                db.session.add(cliente)  # Adicionar o cliente à sessão

        db.session.commit()  # Confirmar a transação para salvar no banco de dados

if __name__ == "__main__":
    with app.app_context():
        importar_clientes_csv('clientes.csv')  # Caminho para o seu arquivo CSV
        print("Clientes importados com sucesso!")