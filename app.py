from flask import Flask, render_template, request, redirect, url_for
from database import conectar
from datetime import date
import psycopg2.extras

app = Flask(__name__)

@app.route('/')
def index():
    conn = conectar()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute('SELECT * FROM produto ORDER BY nome')
    produtos = cursor.fetchall()
    cursor.execute('SELECT * FROM fornecedor ORDER BY nome')
    fornecedores = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html',
        produtos=produtos,
        fornecedores=fornecedores,
        hoje=date.today().isoformat()
    )

@app.route('/enviar', methods=['POST'])
def enviar():
    conn = conectar()
    cursor = conn.cursor()

    produto_id = request.form['produto_id']
    quantidade = float(request.form['quantidade'])
    preco_unitario = float(request.form['preco_unitario'])

    # Registra a movimentação
    cursor.execute('''
        INSERT INTO movimentacao 
        (tipo, produto_id, fornecedor_id, quantidade, preco_unitario, numero_nf, data, motivo, responsavel)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (
        'E',
        produto_id,
        request.form['fornecedor_id'],
        quantidade,
        preco_unitario,
        request.form['numero_nf'],
        request.form['data'],
        request.form['motivo'],
        'Portal do Fornecedor'
    ))

    # Atualiza o estoque
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
    app.run(debug=True, host='0.0.0.0', port=8081)