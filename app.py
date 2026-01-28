import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestão Familiar", layout="wide")

# ---------- Classe ----------
class GestaoFamiliar:
    def __init__(self):
        # Categorias e despesas
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

        # Lista de compras com valor inicial 0
        lista_itens = [
            # Laticínios
            "Iogurte magro natural/aromas sem açúcar",
            "Kefir",
            "Leite magro ou bebida vegetal sem açúcar",
            "Queijo magro fatiado",
            "Queijo fresco",

            # Cereais / Grãos
            "Flocos de aveia fina",
            "Cereais sem açúcar adicionado",
            "Tapioca",

            # Frutos Secos / Sementes
            "Frutos secos variados",
            "Sementes (linhaça, girassol, abóbora, sésamo)",
            "Chia",

            # Frutas
            "Maçã",
            "Laranja",
            "Kiwi",
            "Frutos vermelhos",
            "Banana",
            "Limão",

            # Óleos / Gorduras
            "Azeite",
            "Óleo de coco",

            # Adoçantes / Temperos
            "Mel",
            "Xarope de agave",
            "Canela em pó",
            "Essência de baunilha",

            # Proteínas
            "Fiambre de aves",
            "Whey protein",
            "Ovos",
            "Carne de aves",
            "Peixe",
            "Salmão fumado",
            "Atum em lata",
            "Camarões",
            "Queijo fresco",
            "Requeijão",
            "Mozarela de búfala light",
            "Grão-de-bico",
            "Feijão",
            "Favas",
            "Edamame",
            "Ervilhas",

            # Vegetais
            "Alface",
            "Rúcula",
            "Espinafre",
            "Agrião",
            "Couve",
            "Cenoura",
            "Brócolos",
            "Abobrinha",
            "Pimentos",
            "Tomate",
            "Pepino",
            "Beterraba",
            "Legumes congelados",

            # Bebidas
            "Chá",
            "Tisana",
            "Cevada",
            "Chicória",
            "Água",

            # Extras alimentares
            "Compota sem açúcar",
            "Gelatina",
            "Pudim de gelatina",
            "Mousse de gelatina",
            "Barrita saudável",
            "Bolachas simples",
            "Tostas integrais",
            "Tortilhas de milho",
            "Tortilhas de arroz",
            "Tortilhas de grão-de-bico",

            # Outros
            "Guardanapos",
            "Gel de banho",
            "Papel higiénico",
            "Desentupidor",
            "Limpador de sanitas"
        ]

        # Criar DataFrame da lista de compras
        self.df_compras = pd.DataFrame(lista_itens, columns=["Item"])
        self.df_compras["Valor"] = 0  # Inicializa valores com 0

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
        return False


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

    # Mostrar tabela de despesas simples
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

# ---------- LISTA DE COMPRAS ----------
elif menu == "Lista de Compras":
    st.subheader("🛒 Lista de Compras")

    st.dataframe(gestao.df_compras, use_container_width=True)

    st.markdown("### ✏️ Atualizar valor da compra")
    st.caption("Formato: `Leite magro 2.5`")

    entrada_compra = st.text_input("Introduz item e valor:")

    if st.button("Atualizar Compra"):
        try:
            nome_item, valor_item = entrada_compra.rsplit(" ", 1)
            valor_item = float(valor_item)

            if gestao.atualizar_compra(nome_item, valor_item):
                st.success(f"✅ {nome_item} atualizado para {valor_item} €")
            else:
                st.error("❌ Item não encontrado na lista de compras")

        except ValueError:
            st.error("⚠️ Formato inválido. Usa: Leite magro 2.5")
