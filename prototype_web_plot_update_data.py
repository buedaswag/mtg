#!/usr/bin/env python
# coding: utf-8

# In[2]:


card_names = [
    'Snow Covered Island', 
    'Fabled Passage', 
    'Once Upon a Time', 
    'Murderous Rider // Swift End', 
    'Questing Beast', 
    'Oko, Thief of Crowns'
]
file_names = [card_name.replace('/', '').replace(',', '').replace('  ', '_').replace(' ', '_') for card_name in card_names]
index = 5
file_name = file_names[index]
card_name = card_names[index]
file_names


# In[3]:


'''
loading the pickled data to plot, produce it in a format ready to be consumed by fusion
'''
import pandas as pd 
from matplotlib import pyplot as plt 
import numpy as np 
import matplotlib 
from sqlalchemy import create_engine
import pickle
from scipy.stats import zscore

get_ipython().run_line_magic('matplotlib', 'inline')
idx = pd.IndexSlice


# In[20]:


def get_db_connection_test(local = False):
    '''
    close connections by doing:
    engine.dispose()
    server.close()
    '''
    
    username = 'mig'
    password = 'password' 
    host_name = 'localhost'
    port = 5432
    db_name = 'mtg'
    conn_str = 'postgresql://{}:{}@{}:{}/{}'.format(username, password, host_name, port, db_name)

    engine = create_engine(conn_str)
    
    return engine, None

def get_db_connection_ssh(local = False):
    
    '''
    close connections by doing:
    engine.dispose()
    server.close()
    '''
    
    server_host = '192.168.1.8' if local == True else 'mtgdata.ddns.net'
    server = SSHTunnelForwarder(
         (server_host, 49000),
         ssh_password="red",
         ssh_username="mig",
         remote_bind_address=('127.0.0.1', 5432)
    )

    server.start()

    username = 'mig'
    password = 'password' 
    host_name = 'localhost'
    port = server.local_bind_port # assigned local port
    db_name = 'mtg'
    conn_str = 'postgresql://{}:{}@{}:{}/{}'.format(username, password, host_name, port, db_name)

    engine = create_engine(conn_str)
    
    return engine, server

#fix the ts
def correct_ts(ts):
    minute = 0 if ts.minute < 30 else 30
    ts_corrected = pd.Timestamp(ts.year, ts.month, ts.day, ts.hour, minute)
    return ts_corrected

def data_transformer(df):
    df = df.copy()
    df.ts = df.ts.map(correct_ts)
    df = df.set_index(['ts', 'card_name'])
    df = df.sort_index(level=['ts', 'card_name'])
    return df

##########################################################################
# set local param
engine, server = get_db_connection_test(local=True)

query = '''
SELECT card_name, ts, item_price, item_amount
FROM card_listings;
'''#%(str(now_minus_24_hours), str(now))

df = pd.read_sql_query(query, engine)
engine.dispose()
if server is not None:
    server.close()

#fix the ts and set multiindex
df = data_transformer(df)


# In[21]:


df.head()


# In[22]:


#with open('./pickles/df.pickle', 'rb') as handle:
#    df = pickle.load(handle)


# #javascript code
# var flask_data = JSON.parse('{{ data_price_distribution_lastest_time_stamp | tojson | safe}}');
# var dataSource = {
#     chart: {
#         caption: "Item Amount Distribution",
#         subcaption: "From latest timestamp",
#         xaxisname: "Price",
#         yaxisname: "Amount",
#         numbersuffix: "units",
#         theme: "fusion"
#     },
#     data: flask_data
# };
# FusionCharts.ready(function() {
#     var chart = new FusionCharts({
#         type: 'column2d',
#         renderAt: 'chart-container-price_distribution_lastest_time_stamp',
#         width: '100%',//100% 700
#         height: '700%',//300% 400
#         dataFormat: 'json',
#         dataSource
#     });
#     chart.render();

# # web_plot_price_distribution_lastest_time_stamp_all

# In[25]:


for card_name, file_name in zip(card_names, file_names):
    print(card_name)
    '''
    from and stock
    '''
    from_ = df.xs(card_name, level='card_name', drop_level=True).        groupby(level='ts').item_price.first().to_frame()
    stock_ = df.xs(card_name, level='card_name', drop_level=True).            groupby(level='ts').item_amount.sum().to_frame()
    df_ = from_.join(stock_)

    df_pickle = df_.copy().reset_index() 
    df_pickle.ts = df_pickle.ts.dt.strftime('%Y-%m-%d %H-%M') 
    list_pickle = df_pickle.values.tolist() 
    print(list_pickle[0])
    
    with open('./app/app/pickles/' + file_name + '_item_cheapest_price_item_amount.pickle', 'wb') as handle:
        pickle.dump(list_pickle, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    '''
    item price distribution
    '''
    df_ = df.loc[idx[str(df.index[-1][0]), card_name], ['item_price', 'item_amount']].        reset_index(drop=True)
    df_repeated = pd.DataFrame(np.repeat(df_.item_price.values, df_.item_amount.values), columns=['item_price'])
    df_amount = df_.groupby('item_price').sum().reset_index()
    
    df_filtered = df_repeated
    for i in range(5):
        df_filtered = df_filtered[(zscore(df_filtered.item_price) < 3)]

    df_ = df_amount.loc[df_amount.item_price.isin(df_filtered.item_price)]
    
    plot_constant = 25
    start = 0.0
    stop = df_.item_price.max()
    step = round(df_.item_price.max()/plot_constant, 2)
    item_price_ = np.arange(start, stop, step)
    df__ = pd.DataFrame([(item_price_[i], 0) for i in range(len(item_price_))], columns=['item_price', 'item_amount'])
    df_dummy = df__.append(df_).sort_values(by=['item_price']).reset_index(drop=True)

    '''
    let's try to plot with the interpolated points
    Now it runs!! and we have the data that is relevant to us
    '''
    df_plot = df_dummy.loc[df_dummy.item_price <= df_filtered.item_price.max()]

    '''
    Finally, lets bin the data so that we can actually see the bars

    TODO: come up with a way to set the bin span automatically
    '''

    df_plot_ = df_plot.set_index('item_price')

    # the range of each bin
    bin_span = round(df_plot_.index.max()/plot_constant, 2)

    df_plot_binned = df_plot_.        groupby(pd.cut(df_plot_.index, np.arange(0, df_plot_.index.max() + bin_span, bin_span))).sum()

    df_pickle = df_plot_binned.reset_index().copy()
    df_pickle = df_pickle.rename(columns={'index':'label', 'item_amount':'value'})
    df_pickle = df_pickle.astype({'label':str, 'value':str})
    df_pickle.loc[:, 'label'] = df_pickle.loc[:, 'label'].str[1:-1].to_frame()
    list_pickle = list(df_pickle.T.to_dict().values())
    print(list_pickle[0])

    with open('./app/app/pickles/' + file_name + '_price_distribution_lastest_time_stamp.pickle', 'wb') as handle:
        pickle.dump(list_pickle, handle, protocol=pickle.HIGHEST_PROTOCOL)


# In[ ]:


get_ipython().system('jupyter nbconvert --to script prototype_web_plot_update_data.ipynb')

