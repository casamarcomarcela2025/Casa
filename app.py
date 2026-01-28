import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestão Familiar", layout="wide")

# ---------- Classe ----------
class GestaoFamiliar:
    def __init__(self):
        # Despesas mensais
        data = [
            # Despesas Fixas
            ("Despesas Fixas", "Água", 30),
            ("Despesas Fixas", "Luz", 200),
            ("Despesas Fixas", "Gás", 30),
            ("Despesas Fixas", "Renda da casa", 450),
            ("Despesas Fixas", "Créditos", 250),

            # Alimentação
            ("Alimentação", "Comida mês", 200),
            ("Alimentação", "Jantares fora", 0),
            ("Alimentação", "Extras", 0),
            ("Alimentação", "Coisas para a casa", 0),

            # Outros
            ("Presentes", "Aniversários", 0),
            ("Presentes", "Natal", 0),
            ("Férias", "Férias", 0),
            ("Poupanças", "Poupanças", 0),
        ]
        self.df = pd.DataFrame(data, columns=["Categoria", "Despesa", "Valor"])

        # Lista de compras inicial com categoria simplificada
        alimentos = [
            ("Pequeno-almoço & Lanches", "Iogurte magro natural/aromas sem açúcar", 0),
            ("Pequeno-almoço & Lanches", "Kefir", 0),
            ("Pequeno-almoço & Lanches", "Leite magro ou bebida vegetal sem açúcar", 0),
            ("Pequeno-almoço & Lanches", "Flocos de aveia fina", 0),
            ("Pequeno-almoço & Lanches", "Cereais sem açúcar adicionado", 0),
            ("Carnes/Proteínas", "Fiambre de aves", 0),
            ("Carnes/Proteínas", "Whey protein", 0),
            ("Carnes/Proteínas", "Ovos", 0),
            ("Carnes/Proteínas", "Carne de aves", 0),
            ("Carnes/Proteínas", "Peixe", 0),
            ("Carnes/Proteínas", "Salmão fumado", 0),
            ("Carnes/Proteínas", "Atum em lata", 0),
            ("Carnes/Proteínas", "Camarões", 0),
            ("Acompanhamentos", "Tapioca", 0),
            ("Acompanhamentos", "Quinoa", 0),
            ("Acompanhamentos", "Batata", 0),
            ("Acompanhamentos", "Mandioca", 0),
            ("Acompanhamentos", "Legumes", 0),
            ("Outros", "Azeite", 0),
            ("Outros", "Óleo de coco", 0),
            ("Outros", "Mel", 0),
            ("Outros", "Xarope de agave", 0),
            ("Outros", "Canela em pó", 0),
            ("Outros", "Essência de baunilha", 0),
            ("Outros", "Guardanapos", 0),
            ("Outros", "Gel de banho", 0),
            ("Outros", "Papel higiénico", 0),
            ("Outros", "Desentupidor", 0),
            ("Outros", "Limpador de sanitas", 0)
        ]
        self.df_compras = pd.DataFrame(alimentos, columns=["Categoria", "Item", "Valor"])

    def atualizar_valor(self, despesa, valor):
        mask = self.df["Despesa"].str.lower() == despesa.lower()
        if mask.any():
            self.df.loc[mask, "Valor"] = valor
            return True
        return False

    def atualizar_compra(self, item, valor):
        mask = self.df_compras["Item"].str.lower() == item.lower()
        if mask.any():
            self.df_compras.loc[mask, "Valor"] = valor
            return True
        else:
            # Adiciona na categoria "Outros" se não existir
            self.df_compras = pd.concat(
                [self.df_compras, pd.DataFrame([["Outros", item, valor]], columns=["Categoria", "Item", "Valor"])],
                ignore_index=True
            )
            return True

# ---------- Estado ----------
if "gestao" not in st.session_state:
    st.session_state.gestao = GestaoFamiliar()

gestao = st.session_state.gestao

# ---------- UI ----------
st.title("🏠 Gestão Familiar Mensal")

menu = st.selectbox(
    "Escolhe a secção:",
    ["Despesas Mensais", "Resumo", "Lista de Compras"]
)

# ---------- DESPESAS ----------
if menu == "Despesas Mensais":
    st.subheader("📋 Despesas Mensais")
    st.dataframe(gestao.df, use_container_width=True)

    st.markdown("### ✏️ Atualizar despesa")
    st.caption("Formato: água 50")
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

# ---------- LISTA DE COMPRAS ----------
elif menu == "Lista de Compras":
    st.subheader("🛒 Lista de Compras")

    # ---- Resumo por categoria ----
    st.markdown("### 💡 Resumo por categoria")
    resumo_compras = gestao.df_compras.groupby("Categoria")["Valor"].sum().reset_index()
    st.dataframe(resumo_compras, use_container_width=True)

    # ---- Lista detalhada ----
    st.markdown("### 📋 Detalhe dos itens")
    st.dataframe(gestao.df_compras, use_container_width=True)

    st.markdown("### ✏️ Atualizar valor do item")
    st.caption("Formato: Leite magro 2.5 (se não existir, será adicionado)")
    entrada_compra = st.text_input("Introduz item e valor:")

    if st.button("Atualizar Compra"):
        try:
            nome_item, valor_item = entrada_compra.rsplit(" ", 1)
            valor_item = float(valor_item)
            gestao.atualizar_compra(nome_item, valor_item)
            st.success(f"✅ {nome_item} atualizado/adicionado com valor {valor_item} €")
        except ValueError:
            st.error("⚠️ Formato inválido. Usa: Leite magro 2.5")
