from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Configurar opções do Chrome (modo headless)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Executa o Chrome no modo headless

# Cria uma única instância do WebDriver fora do loop
driver = webdriver.Chrome(options=chrome_options)

try:
    while True:
        # Acessa a página de login
        driver.get('https://portal.sesisp.org.br/login.aspx')

        # Localiza o campo de login e preenche
        login_input = driver.find_element(By.ID, 'cphPrincipal_txtLogin')
        login_input.send_keys('')  # Coloque seu login aqui

        # Localiza o campo de senha e preenche
        senha_input = driver.find_element(By.ID, 'cphPrincipal_txtSenha')
        senha_input.send_keys('')  # Coloque sua senha aqui

        # Localiza o botão de login e clica
        login_button = driver.find_element(By.ID, 'cphPrincipal_btnEntrar')
        login_button.click()

        # Seleciona todos os elementos com a classe 'imgQuadro'
        elements = driver.find_elements(By.CLASS_NAME, 'imgQuadro')

        # Verifica se há pelo menos três elementos
        if len(elements) >= 3:
            # Seleciona o terceiro elemento (índice 2)
            third_element = elements[2]
            # Realiza a ação de clique no terceiro elemento
            third_element.click()
        else:
            print("Menos de três elementos encontrados com a classe 'imgQuadro'.")

        # Espera 5 minutos (300 segundos) antes de repetir a execução
        time.sleep(300)

finally:
    # Certifica-se de fechar o navegador após a execução do loop
    driver.quit()
