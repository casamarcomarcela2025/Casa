import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestão Familiar", layout="wide")

# ---------- Classe ----------
class GestaoFamiliar:
    def __init__(self):

        categorias = {
            "Despesas Fixas": {
                "Água": 30,
                "Luz": 200,
                "Gás": 30,
                "Renda da casa": 450,
                "Créditos": 250,
            },
            "Alimentação": {
                "Comida mês": 200,
                "Jantares fora": 0,
                "Extras": 0,
                "Coisas para a casa": 0,
            },
            "Presentes": {
                "Aniversários": 0,
                "Natal": 0,
            },
            "Férias": {
                "Férias": 0,
            },
            "Poupanças": {
                "Poupanças": 0,
            },
        }

        data = []
        for categoria, despesas in categorias.items():
            for despesa, valor in despesas.items():
                data.append((categoria, despesa, valor))

        self.df = pd.DataFrame(data, columns=["Categoria", "Despesa", "Valor"])

    def atualizar_valor(self, despesa, valor):
        mask = self.df["Despesa"].str.lower() == despesa.lower()
        if mask.any():
            self.df.loc[mask, "Valor"] = valor
            return True
        return False


# ---------- Estado ----------
if "gestao" not in st.session_state:
    st.session_state.gestao = GestaoFamiliar()

gestao = st.session_state.gestao

# ---------- UI ----------
st.title("🏠 Gestão Familiar Mensal")

menu = st.selectbox(
    "Escolhe a secção:",
    ["Despesas Mensais", "Resumo", "Alimentação (em breve)"]
)

# ---------- DESPESAS ----------
if menu == "Despesas Mensais":
    st.subheader("📋 Despesas Mensais")

    st.dataframe(gestao.df, use_container_width=True)

    st.markdown("### ✏️ Atualizar despesa")
    st.caption("Formato: `água 50`")

    entrada = st.text_input("Introduz despesa e valor:")

    if st.button("Atualizar"):
        try:
            nome, valor = entrada.rsplit(" ", 1)
            valor = float(valor)

            if gestao.atualizar_valor(nome, valor):
                st.success(f"✅ {nome} atualizado para {valor} €")
            else:
                st.error("❌ Despesa não encontrada")

        except ValueError:
            st.error("⚠️ Formato inválido. Usa: água 50")

# ---------- RESUMO ----------
elif menu == "Resumo":
    st.subheader("📊 Resumo Mensal")

    total_mensal = gestao.df["Valor"].sum()
    st.metric("💰 Total mensal", f"{total_mensal:.2f} €")

    st.markdown("### Totais por categoria")
    resumo = gestao.df.groupby("Categoria")["Valor"].sum().reset_index()
    st.dataframe(resumo, use_container_width=True)

# ---------- ALIMENTAÇÃO ----------
elif menu == "Alimentação (em breve)":
    st.info("🍽️ A secção de alimentação detalhada será adicionada aqui (listas de compras, pequeno-almoço, almoço, jantar).")





