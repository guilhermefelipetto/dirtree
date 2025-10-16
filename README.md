![logo-banner.png](imagens\logo-banner.png)

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![Framework](https://img.shields.io/badge/Framework-PyQt5-green.svg)](https://riverbankcomputing.com/software/pyqt/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Uma aplicação de desktop moderna e intuitiva para gerar representações de estruturas de diretórios de forma rápida e personalizável. Ideal para documentação de projetos, artigos e apresentações.

## Sumário

- [Sobre o Projeto](#sobre-o-projeto)
- [Recursos Principais](#recursos-principais)
- [Demonstração](#demonstração)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação e Execução](#instalação-e-execução)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Como Contribuir](#como-contribuir)
- [Licença](#licença)

## Sobre o Projeto

O **DirTree Generator** foi criado para simplificar a tarefa de gerar árvores de diretórios. Muitas vezes, desenvolvedores _(eu)_, precisam da estrutura de um projeto de forma clara e legível. Esta ferramenta elimina a necessidade de comandos complexos no terminal, oferecendo uma interface gráfica rica em recursos que permite total controle sobre o resultado final.

Com opções de filtragem, ordenação e uma interface que se atualiza em tempo real, você pode criar a representação perfeita da sua estrutura de arquivos em segundos.

## Recursos Principais

**Interface Gráfica Intuitiva:** Construído com PyQt5 para uma experiência de usuário fluida e agradável.

**Tema Claro e Escuro:** Alterne entre os modos para melhor conforto visual a qualquer hora do dia.

**Customização Avançada de Filtros:**
- **Ignorar Pastas:** Exclua diretórios como `__pycache__`, `.git`, `node_modules`, etc.
- **Ignorar Arquivos:** Remova arquivos específicos da listagem, como `.DS_Store`.
- **Ignorar Extensões:** Oculte arquivos por extensão, como `.log`, `.tmp`, ou `.pyc`.
- **Sempre Incluir:** Defina regras para garantir que certos arquivos ou pastas sempre apareçam, mesmo que correspondam a um filtro de exclusão.

**Ordenação Flexível:** Controle total sobre a ordem de exibição dos itens.
- Ordene o diretório raiz e os subdiretórios de forma independente.
- Escolha entre "Diretórios Primeiro" ou "Arquivos Primeiro".
- Classifique em ordem alfabética (A-Z) ou inversa (Z-A).

**Atualização em Tempo Real:** A visualização da árvore é regenerada automaticamente sempre que um parâmetro é alterado, proporcionando feedback instantâneo.

**Cópia Rápida:** Um botão "Copiar" permite enviar a estrutura gerada diretamente para a área de transferência, pronta para ser colada em qualquer lugar.

## Demonstração

| Modo Claro | Modo Escuro |
| :---: | :---: |
| *![Screenshot do Modo Claro](imagens\modo_claro.png)* | *![Screenshot do Modo Escuro](imagens\modo_escuro.png)* |

## Tecnologias Utilizadas

- **Python 3**
- **PyQt5** (para a interface gráfica)

## Instalação e Execução

Siga os passos abaixo para executar o projeto em sua máquina local.

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd dirtree
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    # Para Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Para macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    O projeto utiliza a biblioteca `PyQt5`. Certifique-se de que ela esteja no seu arquivo `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a aplicação:**
    ```bash
    python main_app.py
    ```

## Estrutura do Projeto

A estrutura do código-fonte está organizada da seguinte forma para garantir clareza e manutenibilidade:

```bash
dirtree/
├── draw_structure_logic.py  # Lógica para construir a estrutura da árvore
├── main_app.py              # Lógica principal da aplicação e da interface gráfica
├── styles.py                # Folhas de estilo (QSS) para os modos claro e escuro
├── README.md                # Este arquivo
└── requirements.txt         # Dependências do projeto
```
###### _Sim, isso foi feito pelo **DirTree**._

## Como Contribuir

Contribuições são o que tornam a comunidade de código aberto um lugar incrível para aprender, inspirar e criar. Qualquer contribuição que você fizer será **muito apreciada**.

1.  Faça um **Fork** do projeto.
2.  Crie uma **Branch** para sua feature (`git checkout -b feature/AmazingFeature`).
3.  Faça o **Commit** de suas mudanças (`git commit -m 'Add some AmazingFeature'`).
4.  Faça o **Push** para a Branch (`git push origin feature/AmazingFeature`).
5.  Abra um **Pull Request**.

## Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.
