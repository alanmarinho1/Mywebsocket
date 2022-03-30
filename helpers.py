import tabula
import pandas as pd
import re
import os


def df_ajust_first_page(df, listadrop, empresa, ag, conta):
    
    for n in range(df.iloc[-1].name):
    
        if(df.columns[0] == 'Data Lançamento'):
            df = df.drop(columns=["Unnamed: 0"])
            df = df.rename(columns={"Data Lançamento": "Lançamento"})
            df.insert(0, 'Data', None)
        
        if('SALDO ANTERIOR' in str(df.loc[n, 'Lançamento'])):
            listadrop.append(n)
            continue

        texto = df.loc[n, 'Lançamento']

        if(pd.isnull(df.loc[n, 'Lançamento'])):
            pass
        
        elif(re.search('\w(\d+\/\d+\/\d+)', texto)):

            data = re.search('(\d+\/\d+\/\d+)', texto).group(1)
            df.loc[n, 'Lançamento'] = df.loc[n, 'Lançamento'][:-10] + ' ' + df.loc[n+1, 'Lançamento']
            df.loc[n, 'Data'] = data
            listadrop.append(n+1)

        if not pd.isnull(df['Saldo (R$)'][n]) and pd.isnull(df['Lançamento'][n]):
            df.loc[n, 'Lançamento'] = str(df.loc[n-1, 'Lançamento']) + ' ' + str(df.loc[n+1, 'Lançamento'])
            listadrop.append(n-1)
            listadrop.append(n+1)

    listadrop = list(set(listadrop))

    for n in listadrop:
        df = df.drop(index=n)
        
    df.insert(0, 'Empresa', empresa)
    df.insert(1, 'Agencia', ag)
    df.insert(2, 'Conta', conta)
    
    if(pd.isnull(df.loc[df.last_valid_index(), df.columns[2]]) and pd.isnull(df.loc[df.last_valid_index(), df.columns[3]]) and pd.isnull(df.loc[df.last_valid_index(), df.columns[4]]) and pd.isnull(df.loc[df.last_valid_index(), df.columns[5]])):
        lastrownull = True
    else:
        lastrownull = False
        
    return df, lastrownull

def df_ajust_pages(df, listadrop, lastrow):
          
    
    for n in range(df.last_valid_index() + 1):

        if(n==0):
       
            if(len(df.columns) != 6):
                df.insert(0, 'Data', None)
            else:
                if not 'Unnamed' in df.columns[0] and pd.isnull(df.loc[n, df.columns[0]]):
                    df.loc[n, df.columns[0]] = df.columns[0]
            if(lastrow):
                if(df.columns[-2][0] == '-'):
                    new_row = pd.DataFrame({df.columns[0]:None, df.columns[1]:df.columns[1], df.columns[2]: df.columns[2], df.columns[3]:None,
                                        df.columns[4]:df.columns[4], df.columns[5]:df.columns[5]}, index=[0])
                else:
                    new_row = pd.DataFrame({df.columns[0]:None, df.columns[1]:df.columns[1], df.columns[2]: df.columns[2], df.columns[3]: df.columns[3], 
                                        df.columns[4]:None, df.columns[5]:df.columns[5]}, index=[0])
                df = pd.concat([new_row, df])
                df.reset_index(inplace=True, drop=True)
                
            elif('Unnamed' in df.columns[2] and 'Unnamed' in df.columns[3] and 'Unnamed' in df.columns[5]):
                    new_row = pd.DataFrame({df.columns[0]:None, df.columns[1]:df.columns[1], df.columns[2]: None, df.columns[3]:None,
                                        df.columns[4]:None, df.columns[5]:None}, index=[0])
                    df = pd.concat([new_row, df])
                    df.reset_index(inplace=True, drop=True)
            else:
           
                if(df.columns[-2][0] == '-' and len(df.columns) == 5):
                    df.insert(3, 'Crédito (R$)', None)
                elif(len(df.columns) == 5):
                    df.insert(4, 'Débito (R$)', None)
                if not pd.isnull(df.loc[n, df.columns[1]]):    
                    df.loc[n, df.columns[1]] = df.columns[1] + ' ' + df.loc[n, df.columns[1]]
                else:
                    df.loc[n, df.columns[1]] = df.columns[1]
                df.loc[n, df.columns[2]] = df.columns[2]
                if not 'Unnamed' in df.columns[2]:
                    df.loc[n, df.columns[2]] = df.columns[2]
                if not 'Unnamed' in df.columns[3]:
                    df.loc[n, df.columns[3]] = df.columns[3]
                if not 'Unnamed' in df.columns[4]:
                    df.loc[n, df.columns[4]] = df.columns[4]
                if not 'Unnamed' in df.columns[5]:
                    df.loc[n, df.columns[5]] = df.columns[5]

        df.columns = ['Data','Lançamento','Dcto.','Crédito (R$)','Débito (R$)','Saldo (R$)']

        if(str(df['Lançamento'][n]) == 'SALDO ANTERIOR'):
                listadrop.append(n)
                continue

        if not pd.isnull(df['Saldo (R$)'][n]) and pd.isnull(df['Lançamento'][n]):
            df.loc[n, 'Lançamento'] = str(df.loc[n-1, 'Lançamento']) + ' ' + str(df.loc[n+1, 'Lançamento'])
            listadrop.append(n-1)
            listadrop.append(n+1)

    listadrop = list(set(listadrop))

    for n in listadrop:
        df = df.drop(index=n)
       
    if(pd.isnull(df.loc[df.last_valid_index(), df.columns[2]]) and pd.isnull(df.loc[df.last_valid_index(), df.columns[3]]) and pd.isnull(df.loc[df.last_valid_index(), df.columns[4]]) and pd.isnull(df.loc[df.last_valid_index(), df.columns[5]])):

        lastrownull = True
    else:
        lastrownull = False
    
    return df, lastrownull

def last_df_ajust(df, listadrop):
    index = None
    for n in range(df.iloc[-1].name + 1):
    
        if(n == df.last_valid_index()):
            continue

        if(n == 0):
            pass
        else:

            if not pd.isnull(df['Saldo (R$)'][n]) and pd.isnull(df['Saldo (R$)'][n+1] and pd.isnull(df['Saldo (R$)'][n-1])):

                if(index == n-1):
                    print(f'deu pass no {n}')
                    pass
                else:
                    if pd.isnull(df.loc[n, 'Lançamento']):
                        df.loc[n, 'Lançamento'] = ''
                    df.loc[n, 'Lançamento'] = str(df.loc[n-1, 'Lançamento']) + ' '  + df.loc[n, 'Lançamento'] + ' ' + str(df.loc[n+1, 'Lançamento'])
                    listadrop.append(n-1)
                    listadrop.append(n+1)
                    index = n+1
            elif not pd.isnull(df['Saldo (R$)'][n]) and pd.isnull(df['Saldo (R$)'][n-1]):
                if pd.isnull(df.loc[n, 'Lançamento']):
                        df.loc[n, 'Lançamento'] = ''
                df.loc[n, 'Lançamento'] = str(df.loc[n-1, 'Lançamento']) + ' '  + df.loc[n, 'Lançamento']
                listadrop.append(n-1)
        
        if not pd.isnull(df['Data'][n]) and pd.isnull(df['Data'][n+1]):
            df.loc[n+1, 'Data'] = df.loc[n, 'Data']
        if(df.loc[n, 'Data'] == 'Total'):
            listadrop.append(n)
        if not pd.isnull(df['Empresa'][n]) and pd.isnull(df['Empresa'][n+1]):
            df.loc[n+1, 'Empresa'] = df.loc[n, 'Empresa']
        if not pd.isnull(df['Agencia'][n]) and pd.isnull(df['Agencia'][n+1]):
            df.loc[n+1, 'Agencia'] = df.loc[n, 'Agencia']
        if not pd.isnull(df['Conta'][n]) and pd.isnull(df['Conta'][n+1]):
            df.loc[n+1, 'Conta'] = df.loc[n, 'Conta']


    listadrop = list(set(listadrop))
    for n in listadrop:
        df = df.drop(index=n)

    df.reset_index(inplace=True, drop=True)

    return df