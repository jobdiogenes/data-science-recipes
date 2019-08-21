# Serie de receitas para Ciência de Dados
# resposta da tarefa 1 do episódio 3
# 
# link: https://github.com/jobdiogenes/data-science-recipes/blob/master/gists/data_science_gist_02_pt.ipynbfrom requests import get
#
from requests import get
h = "https://fishbase.ropensci.org"
# achando o continente
continente = get(h+'/countref',params={'PAESE':'Brazil','fields':'continent'}).json()['data'][0]['Continent']
americadosul = get(h+'/countref',params={'limit':99,'Continent': continente, 'fields' : 'C_Code,PAESE'}).json()['data']
serrasalmus = get(h+'/taxa',params={'Genus':'Serrasalmus','limit':99}).json()['data']

for pais in americadosul:
    print('Pais:',pais['PAESE'])
    for especie in serrasalmus:
        r = get(h+'/country',params={"C_Code":pais['C_Code'],'SpecCode':especie['SpecCode'],"fields":"Status,CurrentPresence"}).json()['data']
        if r is not None:
            v = r[0]
            print(f"{especie['Genus']}, {especie['Species']} is {v['Status']} and {v['CurrentPresence']}")