# ltorres_cotador_app.py
import streamlit as st
import pandas as pd
import asyncio
import os
from playwright.async_api import async_playwright

# ---------------- LOGO ------------------
st.image("logo_ltorres_otimizada.png", use_container_width=True)
st.title("Sistema de Cotação - LTorres")

# -------------- INPUT -------------------
produto = st.text_input("Digite o nome do produto a ser cotado:")

# ------------- BOTÃO --------------------
iniciar = st.button("Buscar Cotações")

# ----------- FUNÇÃO DE BUSCA -----------
async def buscar_preco_marest(produto):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"]
            )
            page = await browser.new_page()
            await page.goto("https://www.marest.com.br/login")

            # login
            await page.fill("input[name='username']", os.getenv("MAREST_USER"))
            await page.fill("input[name='password']", os.getenv("MAREST_PASS"))
            await page.click("button[type='submit']")
            await page.wait_for_timeout(2000)

            # busca
            await page.goto("https://www.marest.com.br")
            await page.fill("input[name='q']", produto)
            await page.click("button[type='submit']")
            await page.wait_for_timeout(2000)

            preco = await page.text_content(".preco .valor")
            await browser.close()
            return preco
    except Exception as e:
        return f"Erro: {e}"


async def buscar_preco_magia(produto):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"]
            )
            page = await browser.new_page()
            await page.goto("https://www.magia.com.br/login")

            # login
            await page.fill("input[name='username']", os.getenv("MAGIA_USER"))
            await page.fill("input[name='password']", os.getenv("MAGIA_PASS"))
            await page.click("button[type='submit']")
            await page.wait_for_timeout(2000)

            # busca
            await page.goto("https://www.magia.com.br")
            await page.fill("input[name='q']", produto)
            await page.click("button[type='submit']")
            await page.wait_for_timeout(2000)

            preco = await page.text_content(".preco .valor")
            await browser.close()
            return preco
    except Exception as e:
        return f"Erro: {e}"

# ------------ RODANDO ------------------
if iniciar and produto:
    with st.spinner("Buscando preços..."):
        preco_marest = asyncio.run(buscar_preco_marest(produto))
        preco_magia = asyncio.run(buscar_preco_magia(produto))

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
