import pandas as pd
import numpy as np
import scipy.stats as st

def load_df():
    '''Função que carrega o df e realiza algumas formatações'''
    df = pd.read_csv('series_dolar.csv',sep=';')
    df.columns = ['date','price']
    #Coluna de preços está como string e com ',' ao invés de '.'
    df['price'] = df['price'].str.replace(',','.').astype(float)
    return df

def calcula_retorno(pd_series,hp,descending):
    '''Recebe uma pd series um parâmetro de janela e uma indicação se é descendente ou não'''
    if not isinstance(pd_series, pd.Series):
        return 'Não foi inserido uma pandas series'
    elif not isinstance(pd_series.values, int) and not not isinstance(pd_series.values, float):
        return 'Foi inserido uma pandas series que não é inteira ou float'  
    elif not isinstance(hp,str) and not isinstance(hp,int):
        return 'Foi inserido um valor de hp que não é string ou inteiro'
    elif not isinstance(descending,bool):
        return 'Foi inserido um valor de descending que não é boleano'
    else:
        df = pd_series.reset_index()
        if descending:
            df.sort_index(inplace=True,ascending=False)
        df['price_'+str(hp)] = df['price'].shift(hp)
        df['ret_rel_simples_'+str(hp)] = (df['price'] - df['price_'+str(hp)])/df['price_'+str(hp)]
        df.drop(columns=['index'],inplace=True)
        
        return df

def calcula_log_retorno(pd_series,hp,descending):
    '''Recebe uma pd series um parâmetro de janela e uma indicação se é descendente ou não'''
    if not isinstance(pd_series, pd.Series):
        return 'Não foi inserido uma pandas series'
    elif not isinstance(pd_series.values, int) and not not isinstance(pd_series.values, float):
        return 'Foi inserido uma pandas series que não é inteira ou float'  
    elif not isinstance(hp,str) and not isinstance(hp,int):
        return 'Foi inserido um valor de hp que não é um inteiro'
    elif not isinstance(descending,bool):
        return 'Foi inserido um valor de descending que não é boleano'
    else:
        df = pd_series.reset_index()
        if descending:
            df.sort_index(inplace=True,ascending=False)
        df['price_'+str(hp)] = df['price'].shift(int(hp))
        df['log_retorno_'+str(hp)] = np.log(df['price']/df['price_'+str(hp)])
        df.drop(columns=['index'],inplace=True)
        
        return df

def calcula_var(pandas_serie_retornos, alpha, vlr_carteira_atual,descending):
    '''
    Recebe uma panda series de retornos, um alpha, um vlr da carteira atual e se é ascendente ou não

    Retorna a métrica de risco var
    '''
    if not isinstance(descending,bool):
        return 'Foi inserido um valor de descending que não é boleano'
    elif not isinstance(pandas_serie_retornos, pd.Series):
        return 'Não foi inserido uma pandas series'
    elif not isinstance(float(alpha),float):
        return 'Foi inserido um valor de alpha que não é um float'
    elif not isinstance(vlr_carteira_atual, int) and not isinstance(vlr_carteira_atual, float):
        return 'Valor carteira atual não é inteiro e nem float'
    else:
        pandas_serie_retornos.dropna(inplace=True)
        df = pandas_serie_retornos.reset_index(drop=True)
        if descending:
            df.sort_index(inplace=True,ascending=False)
        df = df.to_frame()
        #preço_auxiliar = p(t) - p(t-hp)
        #p(t) - p(t-1) = retorno * p(t- hp)
        df['preco_auxiliar'] = np.ones(pandas_serie_retornos.shape[0])
        df.loc[0,'preco_auxiliar'] = vlr_carteira_atual
        #final_idx_preco_auxiliar = df.shape[0] - 1
        for i in range(1,pandas_serie_retornos.shape[0]):
            df.loc[i,'preco_auxiliar'] = df.iloc[(i-1),0]* df.loc[(i-1),'preco_auxiliar'] + df.loc[(i-1),'preco_auxiliar'] 
        #TODO corrigir essa lina abaixo para não precisar do loop (por algum motivo que ainda não entendi está dando pau)
        #df.loc[1:,'preco_auxiliar'] = df.iloc[0:final_idx_preco_auxiliar,0]* df.loc[1:,'preco_auxiliar'] +  df.loc[1:,'preco_auxiliar']
        df['pnl'] = df.iloc[:,0] * df.loc[:,'preco_auxiliar']
        
        
        var_quantile = df['pnl'].quantile(alpha)

        mu, sigma = st.norm.fit(df['pnl'])
        z = st.norm.ppf(alpha)
        var_parametrico = z*sigma

        return var_quantile, var_parametrico

def calcula_es(pandas_serie_retornos, var,vlr_carteira_atual,descending):
    '''
    Recebe uma panda series de retornos, um var, um vlr da carteira atual e se é ascendente ou não

    Retorna a métrica de risco var
    '''
    if not isinstance(descending,bool):
        return 'Foi inserido um valor de descending que não é boleano'
    elif not isinstance(pandas_serie_retornos, pd.Series):
        return 'Não foi inserido uma pandas series'
    elif not isinstance(var, int) and not isinstance(var, float):
        return 'Valor do var não é inteiro e nem float'
    elif not isinstance(vlr_carteira_atual, int) and not isinstance(vlr_carteira_atual, float):
        return 'Valor carteira atual não é inteiro e nem float'
    else:
        pandas_serie_retornos.dropna(inplace=True)
        df = pandas_serie_retornos.reset_index(drop=True)
        if descending:
            df.sort_index(inplace=True,ascending=False)
        df = df.to_frame()
        
        df['preco_auxiliar'] = np.ones(pandas_serie_retornos.shape[0])
        df.loc[0,'preco_auxiliar'] = vlr_carteira_atual
        #final_idx_preco_auxiliar = df.shape[0] - 1
        for i in range(1,pandas_serie_retornos.shape[0]):
            df.loc[i,'preco_auxiliar'] = df.iloc[(i-1),0]* df.loc[(i-1),'preco_auxiliar'] + df.loc[(i-1),'preco_auxiliar'] 
        #TODO corrigir essa lina abaixo para não precisar do loop (por algum motivo que ainda não entendi está dando pau)
        #df.loc[1:,'preco_auxiliar'] = df.iloc[0:final_idx_preco_auxiliar,0]* df.loc[1:,'preco_auxiliar'] +  df.loc[1:,'preco_auxiliar']
        df['pnl'] = df.iloc[:,0] * df.loc[:,'preco_auxiliar']
        
        es = df.loc[df['pnl'] <= var,'pnl'].mean()

        return es
