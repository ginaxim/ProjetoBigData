Original file is located at
    https://colab.research.google.com/drive/1cpXms1PPtK7eGrEDiRBn8djqyIUIP44V
"""

import pandas as pd
import re

pd.set_option('display.max_columns', None)

compras = pd.read_csv('VendasGrano_csv.csv', encoding='latin1', delimiter=';', decimal=',', thousands='.')

print(compras.columns)

def itens_semelhantes(compras, top_fornecedores):
    compras_fornecedores = compras[compras['Fornecedor'].isin(top_fornecedores)]
    produtos_por_fornecedor = compras_fornecedores.groupby(['Descrição Material', 'Fornecedor']).agg({'Qtde.': 'sum'}).reset_index()
    produtos_por_quantidade_fornecedores = produtos_por_fornecedor.groupby('Descrição Material').size().reset_index(name='Quantidade_Fornecedores')
    produtos_com_mais_de_um_fornecedor = produtos_por_quantidade_fornecedores[produtos_por_quantidade_fornecedores['Quantidade_Fornecedores'] > 1]['Descrição Material']

    return produtos_com_mais_de_um_fornecedor

def valores_por_fornecedor(compras, top_fornecedores, itens_semelhantes):
    produtos_com_mais_de_um_fornecedor = itens_semelhantes(compras, top_fornecedores)
    
    for produto in produtos_com_mais_de_um_fornecedor:
        print('Produto:', produto)
        fornecedores_produto = compras[compras['Descrição Material'] == produto].groupby('Fornecedor').agg({'Total (R$)': 'sum', 'Preço Unitário (R$)': 'mean', 'Qtde.': 'sum', 'Unidade': 'first'}).reset_index()
        fornecedores_produto.columns = ['Fornecedor', 'Total Gasto', 'Valor Unitário Médio (R$)', 'Quantidade', 'Unidade']
        
        for index, row in fornecedores_produto.iterrows():
            fornecedor = row['Fornecedor']
            total_gasto = row['Total Gasto']
            quantidade = row['Quantidade']
            valor_unitario_medio = row['Valor Unitário Médio (R$)']
            unidade_comprada = row['Unidade']
            total_gasto_decimal = '{:.2f}'.format(total_gasto)
            valor_unitario_medio_decimal = '{:.2f}'.format(valor_unitario_medio)
            
            print(f'Fornecedor: {fornecedor}')
            print(f'Quantidade de itens comprados: {quantidade}')
            print(f'Total gasto: {total_gasto_decimal}')
            print(f'Valor Unitário Médio (R$): {valor_unitario_medio_decimal}')
            print(f'Unidade Comprada: {unidade_comprada}')
        print()

top_fornecedores = ['UMEHARA ALIMENTOS LTDA', 'Hortifruti Genesis Ltda', 'Supermercados unidos (pai da luiza)']
valores_por_fornecedor(compras, top_fornecedores, itens_semelhantes)