import pandas as pd
import numpy as np

df1=pd.read_csv('tmdb_5000_credits.csv', error_bad_lines=False)
df2=pd.read_csv('tmdb_5000_movies.csv', error_bad_lines=False)
df1.columns = ['id','tittle','cast','crew']
df = df2.merge(df1,on='id')

from ast import literal_eval

features = ['cast', 'crew']

for feature in features:
    df[feature] = df[feature].apply(literal_eval)

def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan

def get_screenplay(x):
    for i in x:
        if i['job'] == 'Screenplay':
            return i['name']
    return np.nan

# def get_screenplay(x):
#     for i in x:
#         if i['job'] == 'Screenplay':
#             return i['name']
#     return np.nan

def get_actor(x):
    b = []
    for i in x:
      for a in i:
        if a == 'name' and i['order'] in range(0,10):
          b.append(i['name'].replace(' ' , '').strip("'"))
    return(str(b).strip('[]'))

#ef get_summarize(x):



df['director'] = df['crew'].apply(get_director)
df['actor'] = df['cast'].apply(get_actor)
df['Screenplay'] = df['crew'].apply(get_screenplay)

df = df[['original_title', 'director' , 'Screenplay', 'actor' , 'overview' ]]

#df['actor'] = df['actor'].map(lambda x: x.lstrip("'").rstrip("'"))

df['actor'] = df['actor'].map(lambda x: str(x).replace("'", " ").replace(',',' '))
df['director'] = df['director'].map(lambda x: str(x).replace(" ", ""))
df['Screenplay'] = df['Screenplay'].map(lambda x: str(x).replace(" ", ""))
df['original_title'] =  df['original_title'].str.lower()


df['common'] = df[df.columns[1:-1]].apply(
    lambda x: ' '.join(x.dropna().astype(str)),
    axis=1
)


df.to_csv('movie.csv')
