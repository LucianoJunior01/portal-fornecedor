# Portal do Fornecedor

Sistema que simula o ambiente de um fornecedor, permitindo o envio de 
dados de Notas Fiscais diretamente para o sistema de almoxarifado AlmoxIF.

## Acesso direto
https://portal-fornecedor-production.up.railway.app

## Sistema integrado
Os dados enviados aqui são recebidos e processados pelo AlmoxIF:
https://github.com/LucianoJunior01/almoxif

## Como funciona
O fornecedor seleciona o produto e preenche os dados da NF (número, 
quantidade, preço, data). Ao enviar, os dados são gravados no banco 
PostgreSQL compartilhado, e o AlmoxIF atualiza o estoque automaticamente.

## Tecnologias utilizadas
- Python 3.12
- Flask
- PostgreSQL (Railway)
- Bootstrap 5

## Como executar localmente

### 1. Clone o repositório
```bash
git clone https://github.com/LucianoJunior01/portal-fornecedor.git
cd portal-fornecedor
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure a variável de ambiente DATABASE_URL
Aponte para o mesmo banco PostgreSQL usado pelo AlmoxIF.

### 4. Execute o sistema
```bash
python app.py
```

### 5. Acesse no navegador
```
http://127.0.0.1:8081
```