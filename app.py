from flask import Flask, render_template, request, redirect, url_for
from database import conectar
from datetime import date
import psycopg2.extras
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', hoje=date.today().isoformat())

@app.route('/enviar', methods=['POST'])
def enviar():
    conn = conectar()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # --- Fornecedor: busca ou cria ---
    fornecedor_nome = request.form['fornecedor_nome'].strip()
    fornecedor_cnpj = request.form.get('fornecedor_cnpj', '').strip()

    cursor.execute('SELECT id FROM fornecedor WHERE nome ILIKE %s', (fornecedor_nome,))
    fornecedor = cursor.fetchone()

    if fornecedor:
        fornecedor_id = fornecedor['id']
    else:
        cursor.execute('''
            INSERT INTO fornecedor (nome, cnpj) VALUES (%s, %s) RETURNING id
        ''', (fornecedor_nome, fornecedor_cnpj))
        fornecedor_id = cursor.fetchone()['id']

    # --- Produto: busca ou cria ---
    produto_codigo = request.form['produto_codigo'].strip()
    produto_nome = request.form['produto_nome'].strip()

    cursor.execute('SELECT id FROM produto WHERE codigo = %s', (produto_codigo,))
    produto = cursor.fetchone()

    quantidade = float(request.form['quantidade'])
    preco_unitario = float(request.form['preco_unitario'])

    if produto:
        produto_id = produto['id']
    else:
        cursor.execute('''
            INSERT INTO produto 
            (nome, codigo, categoria, unidade, estoque_atual, estoque_minimo, preco_medio, nacional)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
        ''', (produto_nome, produto_codigo, 'Não classificado', 'un', 0, 0, preco_unitario, 'S'))
        produto_id = cursor.fetchone()['id']

    # --- Registra a movimentação ---
    cursor.execute('''
        INSERT INTO movimentacao 
        (tipo, produto_id, fornecedor_id, quantidade, preco_unitario, numero_nf, data, motivo, responsavel)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (
        'E',
        produto_id,
        fornecedor_id,
        quantidade,
        preco_unitario,
        request.form['numero_nf'],
        request.form['data'],
        request.form['motivo'],
        'Portal do Fornecedor'
    ))

    # --- Atualiza o estoque ---
    cursor.execute('''
        UPDATE produto 
        SET estoque_atual = estoque_atual + %s,
            preco_medio = %s
        WHERE id = %s
    ''', (quantidade, preco_unitario, produto_id))

    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('sucesso'))

@app.route('/sucesso')
def sucesso():
    return render_template('sucesso.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8081))
    app.run(debug=True, host='0.0.0.0', port=port)
    