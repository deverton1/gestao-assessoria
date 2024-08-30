from flask import Flask, render_template, request, redirect, send_file, url_for
from io import BytesIO
from datetime import datetime
import pdfkit
from flask_sqlalchemy import SQLAlchemy

# Configuração do aplicativo Flask
app = Flask(__name__)

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clientes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo do Cliente atualizado
class Cliente(db.Model):
    id = db.Column(db.String(50), primary_key=True)  # Código da empresa como chave primária
    cnpj = db.Column(db.String(20), unique=True, nullable=False)
    codigo_acesso = db.Column(db.String(50))  # Código de acesso
    razao_social = db.Column(db.String(200), nullable=False)
    nome_fantasia = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    telefone = db.Column(db.String(20), nullable=True)
    logradouro = db.Column(db.String(200), nullable=True)
    numero = db.Column(db.String(10), nullable=True)
    complemento = db.Column(db.String(100), nullable=True)
    bairro = db.Column(db.String(100), nullable=True)
    municipio = db.Column(db.String(100), nullable=True)
    uf = db.Column(db.String(2), nullable=True)
    cep = db.Column(db.String(10), nullable=True)

    def __repr__(self):
        return f'<Cliente {self.razao_social}>'

# Rota para exibir a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para exibir clientes
@app.route('/clientes')
def clientes():
    todos_clientes = Cliente.query.all()
    return render_template('clientes.html', clientes=todos_clientes)

# rota para adicionar clientes
@app.route('/add_cliente', methods=['POST'])
def add_cliente():
    cnpj = request.form['cnpj']
    razao_social = request.form['razao_social']
    nome_fantasia = request.form['nome_fantasia']
    email = request.form['email']
    telefone = request.form['telefone']
    logradouro = request.form['logradouro']
    numero = request.form['numero']
    complemento = request.form['complemento']
    bairro = request.form['bairro']
    municipio = request.form['municipio']
    uf = request.form['uf']
    cep = request.form['cep']

    novo_cliente = Cliente(
        cnpj=cnpj,
        razao_social=razao_social,
        nome_fantasia=nome_fantasia,
        email=email,
        telefone=telefone,
        logradouro=logradouro,
        numero=numero,
        complemento=complemento,
        bairro=bairro,
        municipio=municipio,
        uf=uf,
        cep=cep
    )
    db.session.add(novo_cliente)
    db.session.commit()

    return redirect(url_for('clientes'))

# Rota para editar um cliente
@app.route('/edit_cliente/<int:id>', methods=['GET', 'POST'])
def edit_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    if request.method == 'POST':
        cliente.cnpj = request.form['cnpj']
        cliente.razao_social = request.form['razao_social']
        cliente.nome_fantasia = request.form['nome_fantasia']
        cliente.email = request.form['email']
        cliente.telefone = request.form['telefone']
        cliente.logradouro = request.form['logradouro']
        cliente.numero = request.form['numero']
        cliente.complemento = request.form['complemento']
        cliente.bairro = request.form['bairro']
        cliente.municipio = request.form['municipio']
        cliente.uf = request.form['uf']
        cliente.cep = request.form['cep']
        
        db.session.commit()
        return redirect(url_for('clientes'))
    
    return render_template('edit_cliente.html', cliente=cliente)

# Rota para excluir um cliente
@app.route('/delete_cliente/<int:id>', methods=['POST'])
def delete_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return redirect(url_for('clientes'))


# Rota para geração de recibos
@app.route('/recibos', methods=['GET', 'POST'])
def recibos():
    if request.method == 'POST':
        nome = request.form['nome']
        valor = request.form['valor']
        return gerar_recibo(nome, valor)
    return render_template('recibos.html')

# Rota para a página de contato
@app.route('/contato')
def contato():
    return render_template('contato.html')

# Função para gerar recibos em PDF
def gerar_recibo(nome, valor):
    data_emissao = datetime.now().strftime('%d/%m/%Y')
    html = render_template('recibo_template.html', nome=nome, valor=valor, data_emissao=data_emissao)
    pdf = pdfkit.from_string(html, False)
    return send_file(BytesIO(pdf), attachment_filename=f'recibo_{nome}.pdf', as_attachment=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados
    app.run(debug=True)