# ltorres_cotador_app.py
import streamlit as st
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# ---------------- LOGO ------------------
st.image("logo_ltorres_otimizada.png", use_container_width=True)
st.title("Sistema de Cotação - LTorres")

# -------------- INPUT -------------------
produto = st.text_input("Digite o nome do produto a ser cotado:")

# ------------- BOTÃO --------------------
iniciar = st.button("Buscar Cotações")

# ----------- DRIVER CONFIG -----------
def iniciar_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# ----------- FUNÇÃO DE BUSCA -----------
def buscar_preco_marest(produto):
    try:
        driver = iniciar_driver()
        driver.get("https://www.marest.com.br/login")

        # login
        driver.find_element(By.NAME, "username").send_keys(os.getenv("MAREST_USER"))
        driver.find_element(By.NAME, "password").send_keys(os.getenv("MAREST_PASS"))
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)

        # busca
        driver.get("https://www.marest.com.br")
        driver.find_element(By.NAME, "q").send_keys(produto)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)

        preco = driver.find_element(By.CSS_SELECTOR, ".preco .valor").text
        driver.quit()
        return preco
    except Exception as e:
        return f"Erro: {e}"


def buscar_preco_magia(produto):
    try:
        driver = iniciar_driver()
        driver.get("https://www.magia.com.br/login")

        # login
        driver.find_element(By.NAME, "username").send_keys(os.getenv("MAGIA_USER"))
        driver.find_element(By.NAME, "password").send_keys(os.getenv("MAGIA_PASS"))
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)

        # busca
        driver.get("https://www.magia.com.br")
        driver.find_element(By.NAME, "q").send_keys(produto)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)

        preco = driver.find_element(By.CSS_SELECTOR, ".preco .valor").text
        driver.quit()
        return preco
    except Exception as e:
        return f"Erro: {e}"


# ------------ RODANDO ------------------
if iniciar and produto:
    with st.spinner("Buscando preços..."):
        preco_marest = buscar_preco_marest(produto)
        preco_magia = buscar_preco_magia(produto)

    # Tabela de resultado
    data = {
        "Fornecedor": ["Marest", "Magia"],
        "Preço": [preco_marest, preco_magia]
    }
    df = pd.DataFrame(data)

    # Destaque menor preço
    try:
        df["Preço num"] = df["Preço"].replace("[R$ ]", "", regex=True).str.replace(",", ".").astype(float)
        menor = df["Preço num"].idxmin()
        st.success(f"Melhor preço: {df.iloc[menor]['Fornecedor']} ({df.iloc[menor]['Preço']})")
    except:
        st.warning("Não foi possível comparar os preços.")

    st.dataframe(df[["Fornecedor", "Preço"]])
