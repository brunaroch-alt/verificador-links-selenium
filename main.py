from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import csv

def verificar_link(url):
    
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)

        if response.status_code >= 400:
            response = requests.get(url, timeout=5)

        codigo = response.status_code
        auth_header = response.headers.get("WWW-Authenticate")

        if auth_header or codigo in (401, 403):
            tipo_auth = "desconhecida"

            if auth_header:
                if "Basic" in auth_header:
                    tipo_auth = "Basic"
                elif "Digest" in auth_header:
                    tipo_auth = "Digest"
                elif "Bearer" in auth_header:
                    tipo_auth = "Bearer"

            return {
                "status": "exige autenticação",
                "codigo": codigo,
                "auth": tipo_auth
            }

        if 200 <= codigo < 400:
            return {"status" : "válido", "codigo" : codigo}

        return {"status" : "quebrado", "codigo" : codigo}

    except requests.exceptions.RequestException:
        return {"status": "erro", "codigo": None}

def exportar_csv(links, nome_arquivo="relatorio_links.csv"):
    with open(nome_arquivo, mode="w", newline="", encoding="utf-8-sig") as arquivo:
        writer = csv.writer(arquivo)

        writer.writerow([
            "Texto do link",
            "URL",
            "Status",
            "Código HTTP",
            "Tipo de autenticação"
        ])

        # dados
        for link in links:
            resultado = link.get("resultado", {})

            writer.writerow([
                link.get("texto"),
                link.get("url"),
                resultado.get("status"),
                resultado.get("codigo"),
                resultado.get("auth", "")
            ])


# ----> CONFIGURAÇÃO 
BASE_URL = 'https://the-internet.herokuapp.com'


# ----> INICIALIZAÇÃO 
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.maximize_window()

try:
    driver.get(BASE_URL)

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "a")))

    elementos = driver.find_elements(By.TAG_NAME, 'a')

    links = []

    for elemento in elementos:
        href = elemento.get_attribute('href')
        texto = elemento.text.strip()

        if href and href.startswith("http"):
            links.append({"texto": texto if texto else "Sem texto", "url": href})

    links_validos = []
    links_quebrados = []
    links_autenticacao = []
    links_erro = []

    for i, link in enumerate(links, 1):
        texto_exibido = link['texto'][:50]
        print(f"[{i}/{len(links)}] {texto_exibido}")

        respostas = verificar_link(link['url'])
        link['resultado'] = respostas
        
        if respostas['status'] == "válido":
            print(f"OK - {respostas['codigo']}")
            links_validos.append(link)

        elif respostas['status'] == "exige autenticação":
            print(f"AUTH - {respostas['auth']} ({respostas['codigo']})")
            links_autenticacao.append(link)

        elif respostas['status'] == "quebrado":
            print(f"QUEBRADO - {respostas['codigo']}")
            links_quebrados.append(link)

        else:
            print("ERRO DE CONEXÃO / TIMEOUT")
            links_erro.append(link)


    print("\n-----RESUMO-----")
    print(f"\nTotal: {len(links)}")
    print(f"Válidos: {len(links_validos)}")
    print(f"Quebrados: {len(links_quebrados)}")
    print(f"Requer Autenticação: {len(links_autenticacao)}")
    print(f"Erros: {len(links_erro)}")
        
    exportar_csv(links)
    print("\nUm relatório CSV foi gerado.")
        
finally:
    print("\nFechando navegador...")
    driver.quit()
    print("Fim do teste!")
