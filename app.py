# ltorres_cotador_app.py
import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os

# ---------------- LOGO ------------------
st.image("logo_ltorres_otimizada.png", use_column_width=True)
st.title("Sistema de Cotação - LTorres")

# -------------- INPUT -------------------
produto = st.text_input("Digite o nome do produto a ser cotado:")

# ------------- BOTÃO --------------------
iniciar = st.button("Buscar Cotações")

# ----------- FUNÇÃO DE BUSCA -----------
def buscar_preco_marest(produto):
    try:
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)

        driver.get("https://www.marest.com.br/login")
        time.sleep(1)

        driver.find_element(By.NAME, "username").send_keys(os.getenv("MAREST_USER"))
        driver.find_element(By.NAME, "password").send_keys(os.getenv("MAREST_PASS"))
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)

        driver.get("https://www.marest.com.br")
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(produto)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)

        preco = driver.find_element(By.CSS_SELECTOR, ".preco .valor").text
        driver.quit()
        return preco
    except Exception as e:
        return f"Erro: {e}"

def buscar_preco_magia(produto):
    try:
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)

        driver.get("https://www.magia.com.br/login")
        time.sleep(1)

        driver.find_element(By.NAME, "username").send_keys(os.getenv("MAGIA_USER"))
        driver.find_element(By.NAME, "password").send_keys(os.getenv("MAGIA_PASS"))
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)

        driver.get("https://www.magia.com.br")
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(produto)
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
