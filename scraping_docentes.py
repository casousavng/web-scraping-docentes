import os
import csv
import urllib.request
import requests
from bs4 import BeautifulSoup

# Função para obter o caminho do ambiente trabalho em diferentes SO (para MAC e WINDOWS)
def caminho_desktop():
    if os.name == 'nt':  # Windows
        return os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    else:  # Mac/Linux
        return os.path.join(os.path.expanduser('~'), 'Desktop')

# Função para criar o arquivo CSV no ambiente de trabalho e definir o cabeçalho
def ciar_CSV():
    desktop = caminho_desktop()
    caminho_CSV = os.path.join(desktop, 'lista_professores.csv')
    
    # Criar o arquivo CSV com cabeçalhos
    with open(caminho_CSV, mode='w', newline='', encoding='utf-8') as ficheiro:
        writer = csv.writer(ficheiro)
        writer.writerow(['Nome', 'Grau', 'Categoria', 'Regime Contratual', 'Ano de Entrada', 'Outras Habilitações', 'Área Científica', 'ORCID', 'CienciaVitaeID', 'LinkedIn'])
    return caminho_CSV

# Função para adicionar cada linha de dados no arquivo CSV
def adicionar_CSV(caminho_CSV, dados):
    with open(caminho_CSV, mode='a', newline='', encoding='utf-8') as ficheiro:
        writer = csv.writer(ficheiro)
        writer.writerow(dados)

# Função auxiliar para extrair texto de um elemento, tratando o caso de NoneType
def extrair_texto(dado_extraido):
    if dado_extraido:
        return dado_extraido.get_text(strip=True)
    return None

# Função para percorrer a página de um docente
def scrap_pagina_docente(url, caminho_CSV):

    # Realizar a solicitação HTTP para obter o conteúdo da página
    resposta = requests.get(url)
    conteudo = BeautifulSoup(resposta.content, 'html.parser')

    # Extraindo os dados específicos
    label_nome = conteudo.find('p', class_='font-bold text-3xl') #nome do docente
    nome = extrair_texto(label_nome) if label_nome else None

    label_grau = conteudo.find('span', string='Grau') #grau do docente
    grau = extrair_texto(label_grau.find_next('p')) if label_grau else None

    label_categoria = conteudo.find('span', string='Categoria') #categoria do docente
    categoria = extrair_texto(label_categoria.find_next('p')) if label_categoria else None

    label_regime_contratual = conteudo.find('span', string='Regime Contratual') #regime contratual do docente
    regime_contratual = extrair_texto(label_regime_contratual.find_next('p')) if label_regime_contratual else None

    label_ano_entrada = conteudo.find('span', string='Ano de Entrada') #ano de entrada do docente
    ano_entrada = extrair_texto(label_ano_entrada.find_next('p')) if label_ano_entrada else None

    label_habilitacoes = conteudo.find('span', string='Outras Habilitações') #outras habilitacoes do docente
    habilitacoes = extrair_texto(label_habilitacoes.find_next('p')) if label_habilitacoes else None

    label_area_cientifica = conteudo.find('h3', string='Área Científica:') #area cientifica do docente
    area_cientifica = extrair_texto(label_area_cientifica.find_next('p')) if label_area_cientifica else None

    orcID = conteudo.find_all('a', href=True) #orcid do docente
    for link in orcID:
        if 'https://orcid.org/' in link['href']:
            orcID = link['href'].split('/')[-1] #remove o prefixo do link
            break
        else:
            orcID = None

    cienciavitaeID = conteudo.find_all('a', href=True) #cienciavitaeID do docente
    for link in cienciavitaeID:
        if 'https://www.cienciavitae.pt/portal/' in link['href']:
            cienciavitaeID = link['href'].split('/')[-1] #remove o prefixo do link
            break
        else:
            cienciavitaeID = None

    linkedinID = conteudo.find_all('a', href=True) #linkedinID do docente
    for link in linkedinID:
        if 'https://www.linkedin.com/' in link['href'] and link['href'] != 'https://www.linkedin.com/school/ispgaya/':
            linkedinID = link['href'].split("https://www.")[-1] #remove o prefixo do link
            break
        else:
            linkedinID = None

    # Exibindo na linha de comandos os dados extraídos (opcional - em comentario por defeito - remover plicas para ativar)
    '''
    print(f"Nome: {nome}")
    print(f"Grau: {grau}")
    print(f"Categoria: {categoria}")
    print(f"Regime Contratual: {regime_contratual}")
    print(f"Ano de Entrada: {ano_entrada}")
    print(f"Outras Habilitações: {habilitacoes}")
    print(f"Área Científica: {area_cientifica}")
    print(f"ORCID: {orcid_link}")
    print(f"CienciaVitaeID: {cienciavitae_link}")
    print(f"LinkedIn: {linkedin_link}")
    '''

    # Preparando os dados obtidos para adicionar ao CSV
    dados_obtidos = [nome, grau, categoria, regime_contratual, ano_entrada, habilitacoes, area_cientifica, orcID, cienciavitaeID, linkedinID]
    
    # Adicionar os dados obtidos e organizados ao CSV
    adicionar_CSV(caminho_CSV, dados_obtidos)

# Função para obter os links de docentes da página principal (dividida por páginas)
def scrap_pagina_docentes(url, caminho_CSV):

    # Fazendo uma requisição GET à página
    try:
        with urllib.request.urlopen(url) as resposta:
            resposta_conteudo = resposta.read()

        # Inicializa o BeautifulSoup para analisar o HTML
        conteudo = BeautifulSoup(resposta_conteudo, 'html.parser')

        # Exemplo: Extrair os links href que contenham https://ispgaya.pt/pt/instituicao/corpo-docente/ da página
        links = conteudo.find_all('a', href=True)

        for link in links:
            if 'https://ispgaya.pt/pt/instituicao/corpo-docente/' in link['href']:
                scrap_pagina_docente(link['href'], caminho_CSV)
                
                # Exibir os links (opcional)
                '''print(link['href'])''' 
            
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Função principal
def main():

    # Criar o arquivo CSV
    caminho_CSV = ciar_CSV()

    print("A extrair os dados dos docentes...")

    # Número de páginas a serem percorridas e respetivo link geral (no caso das paginas dos docentes, sao 4)
    pagina = 4
    while pagina > 0:
        url_docente = 'https://ispgaya.pt/pt/instituicao/corpo-docente?page=' + str(pagina)
        pagina -= 1

        # Extrair os links das páginas que contêm os docentes
        scrap_pagina_docentes(url_docente, caminho_CSV)

    print("Extração de dados concluída com sucesso!")

if __name__ == '__main__':
    main()
