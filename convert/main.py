import tabula
import pandas as pd
from glob import glob
import re
import os
import helpers_new_model
from keyword_position import keyword_first_page, keyword_last_page
from PyPDF2 import PdfFileReader, PdfFileWriter
import PyPDF2
import fitz

file = 'MARDISA/EXTRATOS PDF/Extrato_Veiculos_2018.pdf'

def main (file):

    xreader = PyPDF2.PdfFileReader(file)

    df_final = pd.DataFrame()

    lastrow = False

    for x in range(1, xreader.numPages + 1):
        
        print(f'Lendo {x} de {xreader.numPages}')
        
        listadrop = []
        texto = xreader.pages[x-1].extractText()
        doc = fitz.open(file)

    #     area = 0
        
        if(re.search('Folha 1\/', texto)):
            
            if(re.search('\(A\+B\)(\d+)', texto)):
                ag = re.search('\(A\+B\)(\d+)', texto).group(1)
            else:
                ag = re.search('\(R\$\)(\d+) \|', texto).group(1)
            conta = re.search('\| (\d+\-\d+)', texto).group(1)
            if(re.search('Por Período(.*) \|', texto)):  
                empresa = re.search('Por Período(.*) \|', texto).group(1)
            else:
                empresa = None
            
            if(re.search('Total', texto) and re.search('Os dados acima têm como base', texto)):

                area = keyword_first_page(file, x)
                pass
            else:
                area = (208.526,33.91,926.48,581.145)

            df = tabula.read_pdf(file, stream=True, pages=str(x), area=area)
            
            retorno = helpers_new_model.df_ajust_first_page(df[0], listadrop, empresa, ag, conta)
            df = retorno[0]
            lastrow = retorno[1]
                
            df_final = pd.concat([df_final, df])
            
        elif((re.search('Os dados acima têm como base', texto) or re.search('Não há histórico de saldo nas datas pesquisadas', texto) and not re.search('Total', texto))
            or (len(doc[x-1].searchFor("Total")) == 1 and re.search('Saldos Invest', texto))):
            continue

        else:
            
            if(re.search('Últimos Lançamentos', texto) or re.search('Total', texto)):
                    
                area = keyword_last_page(file, x)
                df = tabula.read_pdf(file, stream=True, pages=str(x), area=area)
                
            else:
                
                df = tabula.read_pdf(file, stream=True, pages=str(x), area=(122.777,38.587,926.362,571.791))
                
            if(df == []):
                continue
    #         print(area)
            retorno = helpers_new_model.df_ajust_pages(df[0], listadrop, lastrow)
            df = retorno[0]
            lastrow = retorno[1]
                
            df_final = pd.concat([df_final, df])

    df_final.reset_index(inplace=True, drop=True)

    listadrop = []

    df_final = helpers_new_model.last_df_ajust(df_final, listadrop)

    df_final.to_excel('teste.xlsx', index = False)