# Verificador de Links Quebrados com Selenium

Projeto em Python que verifica links de uma página web, detecta links quebrados e autenticação HTTP, e gera relatórios em CSV.

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/selenium-4.0+-green.svg)](https://www.selenium.dev/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)

## Funcionalidades

- Extração automática de todos os links de uma página
- Validação de links (status HTTP 200-599)
- **Detecção de autenticação HTTP** (Basic, Digest, Bearer)

    Observação: alguns sites podem retornar erro 400 em autenticação Digest mesmo com credenciais válidas, devido a restrições do servidor.
    
- Identificação de links quebrados (404, 500, etc)
- Tratamento de erros de conexão/timeout
- **Uso de WebDriverWait** (esperas inteligentes)
- Exportação de relatório em CSV
- Relatório detalhado no console

## Tecnologias Utilizadas

- **Python 3.10+**
- **Selenium WebDriver** - Automação do navegador
- **Requests** - Validação de links HTTP
- **WebDriver Manager** - Gerenciamento automático do ChromeDriver
- **CSV** - Exportação de relatórios

## Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/brunaroch-alt/verificador-links-selenium.git
cd verificador-links-selenium
```

### 2. Crie um ambiente virtual (recomendado)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Execute o projeto
```bash
python main.py
```

### Personalizando a URL
Edite a variável `BASE_URL` no arquivo:
```python
BASE_URL = 'https://seu-site.com'
```

## Relatórios Gerados

### Arquivo CSV
O script gera automaticamente um arquivo `relatorio_links.csv` com:
- Texto do link
- URL completa
- Status (válido, quebrado, exige autenticação, erro)
- Código HTTP (200, 404, 401, etc)
- Tipo de autenticação (Basic, Digest, Bearer)

## Detalhes Técnicos

### Detecção de Autenticação
O projeto identifica links que exigem autenticação HTTP através:
1. **Cabeçalho WWW-Authenticate** nos headers da resposta
2. **Códigos de status 401** (Unauthorized) e **403** (Forbidden)
3. **Tipo de autenticação**: Basic, Digest ou Bearer

### WebDriverWait
Utiliza esperas explícitas ao invés de `time.sleep()`:
```python
WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.TAG_NAME, "a"))
)
```

### Estratégia de Validação
1. **HEAD request** primeiro (mais rápido, só pega headers)
2. Se falhar (status ≥ 400), tenta **GET request**
3. Alguns servidores bloqueiam HEAD mas aceitam GET

## O que Aprendi

Este projeto foi desenvolvido para consolidar conhecimentos em:

- Selenium WebDriver (find_elements, get_attribute, WebDriverWait)
- Expected Conditions (EC) para esperas inteligentes
- Requests library (HTTP requests, headers, status codes)
- Detecção de autenticação HTTP (WWW-Authenticate)
- Manipulação de arquivos CSV
- Tratamento de exceções
- Estruturação de código Python

## Algumas limitações

- Analisa apenas links `<a href>` com protocolo HTTP/HTTPS
- Não verifica imagens, scripts ou outros recursos
- Não segue links recursivamente (crawler)
- Timeout fixo de 5 segundos por link

## Próximos Passos

- [ ] Refatoração e otimização do código
- [ ] Implementar testes automatizados (pytest)
- [ ] Melhorar tratamento de erros e logging
- [ ] Adicionar mais opções de configuração

## Estrutura Final
```
verificador-links-selenium/
├── main.py
├── requirements.txt
├── .gitignore
├── README.md
└── LICENSE
```
## Recursos Utilizados

- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [Requests Documentation](https://requests.readthedocs.io/)
- [The Internet - Heroku](https://the-internet.herokuapp.com/) - Site para testes

## Contato

**Bruna Rocha**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/bruna-rocha-40a90b320/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/brunaroch-alt)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:brunaprbispo@hotmail.com)

---

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

**Projeto desenvolvido para fins educacionais**
