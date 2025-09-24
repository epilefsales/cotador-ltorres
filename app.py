# ltorres_cotador_app.py
import streamlit as st
import pandas as pd
import os
import requests
from bs4 import BeautifulSoup

# ---------------- LOGO ------------------
st.image("logo_ltorres_otimizada.png", use_container_width=True)
st.title("Sistema de Cotação - LTorres")

# -------------- INPUT -------------------
produto = st.text_input("Digite o nome do produto a ser cotado:")

# ------------- BOTÃO --------------------
iniciar = st.button("Buscar Cotações")

# ----------- FUNÇÃO DE BUSCA -----------
def buscar_preco_marest(produto):
    try:
        url = "https://www.marest.com.br/busca"
        params = {"q": produto}
        r = requests.get(url, params=params, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        preco = soup.select_one(".preco .valor")
        return preco.text.strip() if preco else "Não encontrado"
    except Exception as e:
        return f"Erro: {e}"


def buscar_preco_magia(produto):
    try:
        url = "https://www.magia.com.br/busca"
        params = {"q": produto}
        r = requests.get(url, params=params, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        preco = soup.select_one(".preco .valor")
        return preco.text.strip() if preco else "Não encontrado"
    except Exception as e:
        return f"Erro: {e}"

# ------------ RODANDO ------------------
if iniciar and produto:
    with st.spinner("Buscando preços..."):
        preco_marest = buscar_preco_marest(produto)
        preco_magia = buscar_preco_magia(produto)

    data = {
        "Fornecedor": ["Marest", "Magia"],
        "Preço": [preco_marest, preco_magia]
    }
    df = pd.DataFrame(data)

    try:
        df["Preço num"] = df["Preço"].replace("[R$ ]", "", regex=True).str.replace(",", ".").astype(float)
        menor = df["Preço num"].idxmin()
        st.success(f"Melhor preço: {df.iloc[menor]['Fornecedor']} ({df.iloc[menor]['Preço']})")
    except:
        st.warning("Não foi possível comparar os preços.")

    st.dataframe(df[["Fornecedor", "Preço"]])
