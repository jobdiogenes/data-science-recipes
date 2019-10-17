#! /usrbin/python3
"""
Exemplo de obtenção de dados das Bases Elsevier.
Usando a biblieteca elsapy fornecida pela Elsecier.

Para usar a API é necessário ter uma chave que pode
ser obtida em: dev.elsevier.com

Guarde esta Chave(apikey) em segurança e não empreste a ninguém,
O acesso fornecido com ela impõe restrições, e outros ao usarem
pode fazer que limites sejam atingindos e assim fique bloqueado 
seu acesso por um tempo ou mesm definitivamente.

Por isso apesar de ser possível passar a configuração
direta no programa, deve-se optar por colocar a configuração
num arquivo externo o qual deve ficar isolado de possíveis
publicações ou envios.

A biblioteca elsapy deve estar instalada

faça isso usando: 
pip3 install elsapy

No computador local isso deve ser feito apenas uma vez.
Em ambientes remotos que não mentem o estado como o Colab 
no modo Cloud. Deve ser executado a cada sessão com:

! pip install elsapy

É também necessário a bibliotteca pandas, que pode ser
instalada com:

pip3 install pandas

ou se tiver só python3 (recomendado)com:
pip install pandas

"""

# Importando as funções da Elsapy
from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json
    
## Obtendo a chave de configuração
con_file = open("keys/elsevier.json")
config = json.load(con_file)
con_file.close()

## Iniciando como cliente individual
## Comente a linha abaixo caso possa usar uma chave institucional 
client = ElsClient(config['apikey'])

## Iniciando como cliente institucional
## descomente a linha abaixo caso possa usar uma chave institucional 
#client.inst_token = config['insttoken']

# Iniciando para acessar o Fishbase
from requests import get

# seguindo o método DRY vamos importar nossas rotinas do modulo fishbase
# primeiro vamos incluir como 
import sys
sys.path.append('./modules')

#import fishbase
#h = fishbase.host

## Author example
# Initialize author with uri
my_auth = ElsAuthor(
        uri = 'https://api.elsevier.com/content/author/author_id/7004367821')
# Read author data, then write to disk
if my_auth.read(client):
    print ("my_auth.full_name: ", my_auth.full_name)
    my_auth.write()
else:
    print ("Read author failed.")

## Affiliation example
# Initialize affiliation with ID as string
my_aff = ElsAffil(affil_id = '60101411')
if my_aff.read(client):
    print ("my_aff.name: ", my_aff.name)
    my_aff.write()
else:
    print ("Read affiliation failed.")

## Scopus (Abtract) document example
# Initialize document with ID as integer
scp_doc = AbsDoc(scp_id = 84872135457)
if scp_doc.read(client):
    print ("scp_doc.title: ", scp_doc.title)
    scp_doc.write()   
else:
    print ("Read document failed.")

## ScienceDirect (full-text) document example using PII
pii_doc = FullDoc(sd_pii = 'S1674927814000082')
if pii_doc.read(client):
    print ("pii_doc.title: ", pii_doc.title)
    pii_doc.write()   
else:
    print ("Read document failed.")

## ScienceDirect (full-text) document example using DOI
doi_doc = FullDoc(doi = '10.1016/S1525-1578(10)60571-5')
if doi_doc.read(client):
    print ("doi_doc.title: ", doi_doc.title)
    doi_doc.write()   
else:
    print ("Read document failed.")


## Load list of documents from the API into affilation and author objects.
# Since a document list is retrieved for 25 entries at a time, this is
#  a potentially lenghty operation - hence the prompt.
print ("Load documents (Y/N)?")
s = input('--> ')

if (s == "y" or s == "Y"):

    ## Read all documents for example author, then write to disk
    if my_auth.read_docs(client):
        print ("my_auth.doc_list has " + str(len(my_auth.doc_list)) + " items.")
        my_auth.write_docs()
    else:
        print ("Read docs for author failed.")

    ## Read all documents for example affiliation, then write to disk
    if my_aff.read_docs(client):
        print ("my_aff.doc_list has " + str(len(my_aff.doc_list)) + " items.")
        my_aff.write_docs()
    else:
        print ("Read docs for affiliation failed.")

## Initialize author search object and execute search
auth_srch = ElsSearch('authlast(keuskamp)','author')
auth_srch.execute(client)
print ("auth_srch has", len(auth_srch.results), "results.")

## Initialize affiliation search object and execute search
aff_srch = ElsSearch('affil(amsterdam)','affiliation')
aff_srch.execute(client)
print ("aff_srch has", len(aff_srch.results), "results.")

## Initialize doc search object using Scopus and execute search, retrieving 
#   all results
doc_srch = ElsSearch("AFFIL(dartmouth) AND AUTHOR-NAME(lewis) AND PUBYEAR > 2011",'scopus')
doc_srch.execute(client, get_all = True)
print ("doc_srch has", len(doc_srch.results), "results.")

## Initialize doc search object using ScienceDirect and execute search, 
#   retrieving all results
doc_srch = ElsSearch("star trek vs star wars",'sciencedirect')
doc_srch.execute(client, get_all = False)
print ("doc_srch has", len(doc_srch.results), "results.")