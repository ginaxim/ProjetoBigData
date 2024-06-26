import pandas as pd

compras = pd.read_csv('VendasGrano_csv.csv', encoding='latin1', delimiter=';')

print(compras.columns)

empresas_fornecedores = compras['Fornecedor'].drop_duplicates()
print(empresas_fornecedores)

frequencia_fornecedores = compras['Fornecedor'].value_counts()
print(frequencia_fornecedores)

produtos_umehara = compras[compras['Fornecedor'] == 'UMEHARA ALIMENTOS LTDA']['Descrição Material'].unique()
print(produtos_umehara)

produtos_hortifruti_genesis = compras[compras['Fornecedor'] == 'Hortifruti Genesis Ltda']['Descrição Material'].unique()
print(produtos_hortifruti_genesis)

produtos_unidos = compras[compras['Fornecedor'] == 'Supermercados unidos (pai da luiza)']['Descrição Material'].unique()
print(produtos_unidos)

def imprimir_informacoes(compras, item):
    print('Mercadoria:', item)

    item_compras = compras[compras['Descrição Material'] == item]

    preco_unitario_por_fornecedor = {}
    valor_total_por_fornecedor = {}
    quantidade_por_fornecedor = {}

    for index, row in item_compras.iterrows():
        fornecedor = row['Fornecedor']
        preco_unitario = float(row['Preço Unitário (R$)'].replace(',', '.'))
        quantidade = float(row['Qtde.'].replace(',', '.'))
        valor_total = row['Total (R$)']

        if isinstance(valor_total, float):
            valor_total = str(valor_total)

        valor_total = float(valor_total.replace(',', '.'))

        if fornecedor in preco_unitario_por_fornecedor:
            preco_unitario_por_fornecedor[fornecedor] += preco_unitario * quantidade
            valor_total_por_fornecedor[fornecedor] += valor_total
            quantidade_por_fornecedor[fornecedor] += quantidade
        else:
            preco_unitario_por_fornecedor[fornecedor] = preco_unitario * quantidade
            valor_total_por_fornecedor[fornecedor] = valor_total
            quantidade_por_fornecedor[fornecedor] = quantidade

    for fornecedor in preco_unitario_por_fornecedor.keys():
        preco_unitario = preco_unitario_por_fornecedor[fornecedor] / quantidade_por_fornecedor[fornecedor]
        valor_total = valor_total_por_fornecedor[fornecedor]
        quantidade = quantidade_por_fornecedor[fornecedor]
        print('\n')
        print(f'Fornecedor: {fornecedor}')
        print(f'  Preço Unitário(R$): {preco_unitario:.2f}')
        print(f'  Valor Total(R$): {valor_total:.2f}')
        print(f'  Quantidade: {quantidade}')
    print()

top_fornecedores = ['UMEHARA ALIMENTOS LTDA', 'Hortifruti Genesis Ltda', 'Supermercados unidos (pai da luiza)']
itens_comuns = encontrar_itens_semelhantes(compras, top_fornecedores)

for item in itens_comuns:
    imprimir_informacoes(compras, item)
