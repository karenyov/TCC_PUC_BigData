#coding: utf-8

import json

from urllib.request import urlopen # Faz a requisição no servidor e obtem a resposta
import urllib.error

# Definindo variáveis da url de busca
urlBase = 'https://www.webmotors.com.br/api/';
urlDetails = urlBase + 'detail/car/'

print('Obtendo os dados, aguarde!');

# Pegando dados
data = [];
for i in range(1, 500):
    url = urlBase + 'search/car?url=https://www.webmotors.com.br/carros%2Fsp%3Festadocidade%3DS%25C3%25A3o%2520Paulo%26tipoveiculo%3Dcarros&actualPage='+str(i)

    # Exibir erro caso tenha problemas para obter os dados
    try:
        data += json.load(urlopen(url))['SearchResults'];
        print('Dados da Page: %s obtidos com sucesso, aguarde a criação do arquivo!' % i)
    except urllib.error.HTTPError as e:
        print('Erro ao obter dados!' + e)
    except urllib.error.URLError as e:
        print('Erro ao obter dados!' + e)

data_fipe = []
for d in data:
    print("Obtendo dados do UniqueId: %d" % d["UniqueId"])

    dataDetails = None
    
    # Pega informações detalhadas de cada carro (necessário para obter o valor da tabela FIPE)
    try:
        responseDetails = urlopen(urlDetails + str(d["UniqueId"]))
        dataDetails = json.load(responseDetails)
    except urllib.error.HTTPError as e:
        print('Erro ao obter dados!' + e)
    except urllib.error.URLError as e:
        print('Erro ao obter dados!' + e)

    fipe = {}
    fipe["Fipe"] = 0

    if dataDetails is None or "UniqueId" not in dataDetails:
        fipe["UniqueId"] = None
    else:
        fipe["UniqueId"] = dataDetails["UniqueId"]
    
    if dataDetails is not None and "Specification" in dataDetails and "Evaluation" in dataDetails["Specification"]:
        fipe["Fipe"] = dataDetails["Specification"]["Evaluation"]["FIPE"]
        
    data_fipe.append(fipe)
    
    # Parâmetros necessários para categorização
    # Dados bases necessários para a análise do modelo
    d["IPVApaid"] = False
    d["Licensed"] = False
    d["Warranty"] = False
    d["OnlyOwner"] = False

    if "Specification" in d and "VehicleAttributes" in d["Specification"]:
        for atrr in d["Specification"]["VehicleAttributes"]:        
            if (atrr["Name"] == "IPVA pago"): 
                d["IPVApaid"] = True
                
            if (atrr["Name"] == "Licenciado"): 
                d["Licensed"] = True
                  
            if (atrr["Name"] == "Garantia de fábrica"): 
                d["Warranty"] = True
                
            if (atrr["Name"] == "Único dono"): 
                d["OnlyOwner"] = True

# Salvando os dados obtidos em um arquivo formato json
with open('data/data-cars.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

# Salvando os dados FIPE obtidos em um arquivo formato json
    with open('data/data-cars-fipe.json', 'w', encoding='utf-8') as f:
        json.dump(data_fipe, f, ensure_ascii=False, indent=4)

print('Dados salvos com sucesso!');
