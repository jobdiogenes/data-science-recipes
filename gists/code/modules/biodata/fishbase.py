'''
    This file are published in Data Science Recipes Series gist.github.com/jobdiogenes

    This file are part of module example Multiquery

    Copyright 2019 by Job Diógenes Ribeiro Borges <jobdiogenes@gmail.com>
    Barman is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    Barman is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with Barman.  If not, see <http://www.gnu.org/licenses/>.
'''    
from requests import get
host = "https://fishbase.ropensci.org"

def epcont(pais='Brazil',genero='Serrasalmus',status='',presence=''):
   """ Retorna uma lista de especies de um gênero para um determinado continente
   
   Parameters:
     pais (str):Nome de um país do continente desejado (padrão:Brazil)
     genero (str):Nome do gênero desejado (padrão: Serrasalmus)
     status (str):Se a espécie é considerada 'native' (padrão) ou 'questionable'
     presence (str):Se a espécie esta existe 'present' ou é possível 'possible'

   Returns:
     epcont(pais,genero,status,presence):Retorna uma lista com nome do pais e especie no formato {'Genus':'','Species','Be','Is'}

   """ 
   
   # achando o continente
   continente = get(host+'/countref',params={'PAESE':'Brazil','fields':'continent'}).json()['data'][0]['Continent']
   paises = get(host+'/countref',params={'limit':99,'Continent': continente, 'fields' : 'C_Code,PAESE'}).json()['data']
   genero = get(host+'/taxa',params={'Genus':'Serrasalmus','limit':99}).json()['data']
   especies = []
   for pais in paises:
     print('Pais:',pais['PAESE'])
     for especie in genero:
       pars = {"C_Code":pais['C_Code'],'SpecCode':especie['SpecCode'],"fields":"Status,CurrentPresence"}
       if status != '':
           pars['Status'] = status
       if presence != '':
           pars['CurrentPresence'] = presence
       r = get(host+'/country',params=pars).json()['data']
       if r is not None:
         especies.append({'Genus':especie['Genus'], 'Species': especie['Species'],'Be':r[0]['Status'],'Is':r[0]['CurrentPresence']})
   return(especies) 