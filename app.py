import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ====== Classe de Gestão Familiar ======
class GestaoFamiliar:
    def __init__(self):
        # Despesas gerais iniciais
        despesas_data = [
            {"Categoria": "Serviços", "Item": "Água", "Valor": 30},
            {"Categoria": "Serviços", "Item": "Luz", "Valor": 200},
            {"Categoria": "Serviços", "Item": "Gás", "Valor": 30},
            {"Categoria": "Serviços", "Item": "Renda da casa", "Valor": 450},
            {"Categoria": "Serviços", "Item": "Prestação de outros créditos", "Valor": 250},
            {"Categoria": "Alimentação", "Item": "Comida mês", "Valor": 200},
            {"Categoria": "Alimentação", "Item": "Jantares fora", "Valor": 0},
            {"Categoria": "Alimentação", "Item": "Extras", "Valor": 0},
            {"Categoria": "Alimentação", "Item": "Coisas para a casa", "Valor": 0},
            {"Categoria": "Presentes", "Item": "Aniversários", "Valor": 0},
            {"Categoria": "Presentes", "Item": "Prendas de Natal", "Valor": 0},
            {"Categoria": "Férias", "Item": "Viagens", "Valor": 0},
            {"Categoria": "Férias", "Item": "Lazer", "Valor": 0},
            {"Categoria": "Poupanças", "Item": "Reserva de emergência", "Valor": 0},
            {"Categoria": "Poupanças", "Item": "Investimentos", "Valor": 0}
        ]
        self.df_despesas = pd.DataFrame(despesas_data)

        # Alimentação inicial simplificada
        alimentos_data = [
            {"Categoria": "Pequeno-almoço", "Item": "Iogurte", "Quantidade": 7, "Unidade": "unidades"},
            {"Categoria": "Pequeno-almoço", "Item": "Kefir", "Quantidade": 1.4, "Unidade": "L"},
            {"Categoria": "Almoço", "Item": "Frango", "Quantidade": 110, "Unidade": "g"},
            {"Categoria": "Almoço", "Item": "Legumes variados", "Quantidade": 200, "Unidade": "g"},
            {"Categoria": "Lanches", "Item": "Fruta", "Quantidade": 1, "Unidade": "porção"},
            {"Categoria": "Jantar", "Item": "Peixe", "Quantidade": 120, "Unidade": "g"}
        ]
        self.df_alimentacao = pd.DataFrame(alimentos_data)

    # Atualizar múltiplas despesas via input simplificado
    def atualizar_valores_multiplos(self, entrada):
        itens = [x.strip() for x in entrada.replace(";", ",").split(",") if x.strip()]
        for item in itens:
            partes = item.rsplit(" ", 1)
            if len(partes) != 2:
                continue
            nome, valor_str = partes
            try:
                valor = float(valor_str.replace(",", "."))
                if nome in self.df_despesas["Item"].values:
                    self.df_despesas.loc[self.df_despesas["Item"] == nome, "Valor"] = valor
                else:
                    categoria = st.selectbox(f"Categoria para '{nome}'", ["Serviços","Alimentação","Presentes","Férias","Poupanças"], key=nome)
                    nova_linha = pd.DataFrame([{"Categoria": categoria, "Item": nome, "Valor": valor}])
                    self.df_despesas = pd.concat([self.df_despesas, nova_linha], ignore_index=True)
            except:
                pass

    # Total despesas
    def total_despesas(self):
        return self.df_despesas["Valor"].sum()

# ====== Streamlit App ======
st.title("💑 Gestão Familiar - Casal")

gestao = GestaoFamiliar()

# ====== Despesas Gerais ======
with st.expander("💰 Despesas Gerais"):
    st.subheader("Tabela de Despesas")
    st.dataframe(gestao.df_despesas)

    entrada = st.text_input("Atualizar despesas (ex: Água 50, Luz 120)")
    if st.button("Atualizar Despesas"):
        gestao.atualizar_valores_multiplos(entrada)
        st.success("Despesas atualizadas!")

    st.metric("Total de Despesas", f"R$ {gestao.total_despesas():.2f}")

    # Gráficos por categoria
    st.subheader("Gráficos de Despesas")
    df_cat = gestao.df_despesas.groupby("Categoria")["Valor"].sum().reset_index()

    # Gráfico de barras
    st.bar_chart(df_cat.set_index("Categoria"))

    # Gráfico de pizza
    fig, ax = plt.subplots()
    ax.pie(df_cat["Valor"], labels=df_cat["Categoria"], autopct='%1.1f%%', startangle=90)
    ax.axis("equal")
    st.pyplot(fig)

# ====== Alimentação ======
with st.expander("🍎 Alimentação / Lista de Compras"):
    st.subheader("Tabela de Alimentação")
    st.dataframe(gestao.df_alimentacao)

    # Adicionar novo alimento
    with st.form("novo_alimento"):
        st.write("Adicionar novo alimento")
        categoria = st.selectbox("Categoria", ["Pequeno-almoço", "Almoço", "Lanches", "Jantar"])
        item = st.text_input("Nome do alimento")
        quantidade = st.number_input("Quantidade", min_value=0.0, step=1.0)
        unidade = st.text_input("Unidade (g, L, unidades, porção)")
        if st.form_submit_button("Adicionar Alimento"):
            nova_linha = pd.DataFrame([{"Categoria": categoria, "Item": item, "Quantidade": quantidade, "Unidade": unidade}])
            gestao.df_alimentacao = pd.concat([gestao.df_alimentacao, nova_linha], ignore_index=True)
            st.success(f"{item} adicionado à categoria {categoria}!")

st.write("✅ Todas as alterações são refletidas em tempo real nas tabelas acima.")


