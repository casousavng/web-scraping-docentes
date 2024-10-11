# Projeto de Extração de Dados de Professores

Este projeto foi desenvolvido como parte da disciplina de **Processamento de Informação** do curso de **Engenharia Informática**. O objetivo é criar um script em Python que realiza a extração de dados sobre professores de uma instituição específica e salva essas informações em um arquivo CSV.

## Funcionalidades

- **Extração de Dados**: O script acessa uma página da web e coleta informações sobre professores, incluindo:
  - Nome
  - Grau
  - Categoria
  - Regime Contratual
  - Ano de Entrada
  - Outras Habilitações
  - Área Científica
  - ORCID
  - CiênciaVitaeID
  - LinkedIn

- **Geração de CSV**: Os dados extraídos são organizados e armazenados em um arquivo CSV chamado `lista_professores.csv`, que é criado na área de trabalho do usuário.

- **Compatibilidade de Sistemas Operacionais**: O script detecta automaticamente o sistema operacional (Windows ou Mac/Linux) para criar o arquivo CSV na área de trabalho correta.

- **Múltiplas Páginas**: O script percorre várias páginas de professores, permitindo a coleta de dados de todos os docentes disponíveis.

## Estrutura do Código

1. **Função `caminho_desktop()`**: Obtém o caminho da área de trabalho do usuário, adaptando-se ao sistema operacional.

2. **Função `ciar_CSV()`**: Cria um arquivo CSV com cabeçalhos apropriados para armazenar os dados dos professores.

3. **Função `adicionar_CSV()`**: Adiciona uma nova linha de dados ao arquivo CSV.

4. **Função `extrair_texto()`**: Extrai o texto de um elemento HTML, lidando com casos de valores `None`.

5. **Função `scrap_pagina_docente()`**: Coleta dados de uma página individual de um docente.

6. **Função `scrap_pagina_docentes()`**: Coleta os links das páginas dos docentes a partir da página principal.

7. **Função `main()`**: Executa a criação do CSV e inicia o processo de extração de dados.

## Como Usar

1. Certifique-se de ter o Python instalado em seu sistema.
2. Instale as bibliotecas necessárias:
   ```bash
   pip install requests beautifulsoup4
