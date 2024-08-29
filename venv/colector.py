from selenium import webdriver
from selenium.webdriver.common.by import By
import time

while True:
    nav = webdriver.Chrome()

    nav.get('https://portal.sesisp.org.br/login.aspx')

    # Localizar o campo de login e preencher
    login_input = nav.find_element(By.ID, 'cphPrincipal_txtLogin')
    login_input.send_keys('')

    # Localizar o campo de senha e preencher
    senha_input = nav.find_element(By.ID, 'cphPrincipal_txtSenha')
    senha_input.send_keys('')

    # Localizar o botão de login e clicar
    login_button = nav.find_element(By.ID, 'cphPrincipal_btnEntrar')
    login_button.click()

    # Seleciona todos os elementos com a classe 'imgQuadro'
    elements = nav.find_elements(By.CLASS_NAME, 'imgQuadro')

    # Verifica se há pelo menos três elementos
    if len(elements) >= 3:
        # Seleciona o terceiro elemento (índice 2, já que os índices começam em 0)
        third_element = elements[2]
        # Realiza aação de clique no terceiro elemento, 
        third_element.click()
    else:
        print("Menos de três elementos encontrados com a classe 'imgQuadro'.")

    nav.quit()  # Fecha o navegador após a execução

    time.sleep(300)  # Espera 5 minutos (300 segundos)
    