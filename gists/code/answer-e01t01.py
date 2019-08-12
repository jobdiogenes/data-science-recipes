# resposta a tarefa 01 do episódio 02
from requests import get
h = "https://fishbase.ropensci.org/"
pars = {
    'Genus' : 'serrasalmus',
    'Species' : ''
}
passo = 12
pars['limit'] = passo
r = get(h+'taxa', params = pars).json()
print('Total:',r['count'],', Recebido:',r['returned'])

total = r['count']
posicao = 0  # posição inicial 

while total > passo:
  # ***observe aqui****, que antes foi verificado que o campo 'data' 
  # é uma lista 'list' por isso é muito importante sempre olhar os dados 
  # para ver como eles são e assim saber como trabalhar com eles 
  especies = r['data']
  print('--------------------------------------------')
  print('de:',posicao,' à ',posicao+passo)
  print('--------------------------------------------')
  for especie in especies:
    for campo, valor in especie.items():
      print(campo,':',valor)
    print('--------------------------------------------')
  posicao += passo
  pars['offset'] = posicao 
  total -= passo

print('Fim :)')
