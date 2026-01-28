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

        # Lista de compras
        self.lista_compras = {
            "Laticínios / Alternativas": [
                "Iogurte magro natural/aromas sem açúcar",
                "Kefir",
                "Leite magro ou bebida vegetal sem açúcar",
                "Queijo magro fatiado",
                "Queijo fresco",
            ],
            "Cereais / Grãos": [
                "Flocos de aveia fina",
                "Cereais sem açúcar adicionado",
                "Tapioca",
            ],
            "Frutos Secos / Sementes": [
                "Frutos secos variados",
                "Sementes (linhaça, girassol, abóbora, sésamo)",
                "Chia",
            ],
            "Frutas": [
                "Maçã",
                "Laranja",
                "Kiwi",
                "Frutos vermelhos",
                "Banana",
                "Limão",
            ],
            "Óleos / Gorduras": [
                "Azeite",
                "Óleo de coco",
            ],
            "Adoçantes / Temperos": [
                "Mel",
                "Xarope de agave",
                "Canela em pó",
                "Essência de baunilha",
            ],
            "Proteínas": [
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
            ],
            "Vegetais": [
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
            ],
            "Bebidas": [
                "Chá",
                "Tisana",
                "Cevada",
                "Chicória",
                "Água",
            ],
            "Extras Alimentares": [
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
            ],
            "Outros (Casa / Higiene)": [
                "Guardanapos",
                "Gel de banho",
                "Papel higiénico",
                "Desentupidor",
                "Limpador de sanitas",
            ],
        }

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
    ["Despesas Mensais", "Resumo", "Lista de Compras"]
)

# ---------- DESPESAS ----------
if menu == "Despesas Mensais":
    st.subheader("📋 Despesas Mensais")

    # Mostrar tabela agrupada por categoria
    for categoria, grupo in gestao.df.groupby("Categoria"):
        st.markdown(f"### {categoria}")
        st.table(grupo[["Despesa", "Valor"]].reset_index(drop=True))

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
    st.table(resumo)

# ---------- LISTA DE COMPRAS ----------
elif menu == "Lista de Compras":
    st.subheader("🛒 Lista de Compras")

    for categoria, itens in gestao.lista_compras.items():
        st.markdown(f"### {categoria}")
        for item in itens:
            st.write(f"- {item}")







