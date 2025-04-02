import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.title("Dashboard BCMED por Raphael Schwanke")
st.write("Com base nos dados fornecidos, este dashboard responde às 7 questões propostas.")

@st.cache_data
def load_data():
    df = pd.read_csv("dados_analise_original.csv")
    return df

df = load_data()
# Questão 1: Produtos com Sales_Volume = 100 (Tabela)
with st.expander("Pergunta 1: Produto com maior volume de vendas"):
    st.markdown("""
    **Conclusão:**  
    Foram identificados 15 produtos com Sales_Volume igual a 100, distribuídos entre as categorias, com destaque para Dairy.
   
    **Insights:**  
    - Verificar se 100 é o teto ou o desempenho máximo real para uma análise mais aprofundada.
    """)
    df_max = df[df['Sales_Volume'] == 100]
    st.dataframe(df_max[['Product_Name', 'Catagory', 'Sales_Volume']].reset_index(drop=True))

# Questão 2: Produtos com Status "Backordered"
with st.expander("Pergunta 2: Produtos com Status 'Backordered'"):
    st.markdown("""
    **Conclusão:**  
    Foram identificados 325 produtos com status 'Backordered', com maior incidência na categoria Fruits & Vegetables.
   
    **Insights:**  
    - Indica falhas na previsão de demanda ou problemas na cadeia de suprimentos.
    """)
    df_backordered = df[df['Status'].str.lower().str.contains("backordered", na=False)]
    backorder_counts = df_backordered['Catagory'].value_counts().reset_index()
    backorder_counts.columns = ['Catagory', 'Count']
    backorder_counts = backorder_counts.sort_values(by='Count', ascending=False)
    
    fig_back, ax_back = plt.subplots(figsize=(6,4))
    ax_back.bar(backorder_counts['Catagory'], backorder_counts['Count'], color='orange', edgecolor='black')
    ax_back.set_xlabel("Categoria")
    ax_back.set_ylabel("Número de Produtos Backordered")
    ax_back.set_title("Incidência de Backordered por Categoria")
    plt.xticks(rotation=45)
    st.pyplot(fig_back)

# Questão 3: Comparação entre Stock_Quantity e Reorder_Level (Boxplot do Déficit)
with st.expander("Pergunta 3: Comparação entre Stock_Quantity e Reorder_Level"):
    st.markdown("""
    **Conclusão:**  
    455 produtos possuem Stock_Quantity inferior ao Reorder_Level, principalmente em categorias como Fruits & Vegetables e Grains & Pulses.
   
    **Insights:**  
    - Necessidade de revisar os parâmetros de reposição e a previsão de demanda.
    """)
    df['Deficit'] = df['Reorder_Level'] - df['Stock_Quantity']
    categorias = df['Catagory'].unique()
    data_box = [df[df['Catagory'] == cat]['Deficit'].dropna() for cat in categorias]
    
    fig_box, ax_box = plt.subplots(figsize=(8,6))
    ax_box.boxplot(data_box, labels=categorias, showfliers=True)
    ax_box.set_xlabel("Categoria")
    ax_box.set_ylabel("Déficit (Reorder_Level - Stock_Quantity)")
    ax_box.set_title("Distribuição do Déficit por Categoria")
    plt.xticks(rotation=45)
    st.pyplot(fig_box)

# Questão 4: Análise das Datas de Validad
with st.expander("Pergunta 4: Análise das Datas de Validade"):
    st.markdown("""
    **Conclusão:**  
    Os registros indicam que todos os produtos estão vencidos, o que pode acarretar sérios impactos operacionais e financeiros. Isso evidencia problemas no cadastro das datas ou na política de reposição, comprometendo a qualidade dos produtos e a satisfação dos clientes.
   
    **Insights:**  
    - Parece que os dados estão invertidos. Para uma análise aprofundada, eu precisaria revisar o cadastro de datas e se confirmado que estão corretas, ajustar estratégias para evitar vencimentos.
    """)
    df['Expiration_Date'] = pd.to_datetime(df['Expiration_Date'], format="%m/%d/%Y", errors='coerce')
    df['Date_Received'] = pd.to_datetime(df['Date_Received'], format="%m/%d/%Y", errors='coerce')
    df['Shelf_Life'] = (df['Expiration_Date'] - df['Date_Received']).dt.days
    fig_exp, ax_exp = plt.subplots(figsize=(6,4))
    ax_exp.hist(df['Shelf_Life'].dropna(), bins=30, edgecolor='black', color='lightgreen')
    ax_exp.set_xlabel("Shelf_Life (dias)")
    ax_exp.set_ylabel("Frequência")
    ax_exp.set_title("Distribuição do Shelf_Life")
    st.pyplot(fig_exp)

# Questão 5: Análise do Inventory_Turnover_Rate e Demanda
with st.expander("Pergunta 5: Análise do Inventory_Turnover_Rate e Demanda"):
    st.markdown("""
    **Conclusão:**  
    A análise segmentada por categoria sugere que, embora as médias do giro (Inventory_Turnover_Rate) sejam relativamente próximas entre as categorias, existem variações sutis. Por exemplo, alguns segmentos (como Dairy ou Seafood) podem apresentar uma demanda um pouco maior, refletida em um giro ligeiramente superior, enquanto outros (como Grains & Pulses) podem ter uma demanda menor. No entanto, essa relação não é muito forte, o que indica que fatores adicionais – como estratégias de marketing, sazonalidade e características específicas dos produtos – também influenciam a quantidade demandada.    
    **Insights:**  
    -  Segmentos como Dairy e Seafood tendem a apresentar uma demanda ligeiramente superior, indicando que a categoria exerce alguma influência.
    """)
    df['Inventory_Turnover_Rate'] = pd.to_numeric(df['Inventory_Turnover_Rate'], errors='coerce')
    media_turnover = df.groupby("Catagory")["Inventory_Turnover_Rate"].mean().reset_index()
    fig_turnover, ax_turnover = plt.subplots(figsize=(6,4))
    ax_turnover.bar(media_turnover['Catagory'], media_turnover['Inventory_Turnover_Rate'], color='skyblue', edgecolor='black')
    ax_turnover.set_xlabel("Categoria")
    ax_turnover.set_ylabel("Média do Giro de Estoque")
    ax_turnover.set_title("Média do Inventory_Turnover_Rate por Categoria")
    plt.xticks(rotation=45)
    st.pyplot(fig_turnover)

# Questão 6: Relação entre Unit_Price, Sales_Volume e Inventory_Turnover_Rate
with st.expander("Pergunta 6: Relação entre Unit_Price, Sales_Volume e Inventory_Turnover_Rate"):
    st.markdown("""
    **Conclusão:**  
    A análise revelou que a correlação entre Unit_Price e os indicadores Sales_Volume e Inventory_Turnover_Rate é praticamente nula, indicando que o preço unitário isoladamente não explica o desempenho dos produtos.
   
    **Insights:**  
    - Outros fatores (qualidade, promoção, sazonalidade) devem ser considerados.
    """)
    df['Unit_Price'] = pd.to_numeric(df['Unit_Price'], errors='coerce')
    df['Sales_Volume'] = pd.to_numeric(df['Sales_Volume'], errors='coerce')
    df['Catagory'] = df['Catagory'].astype(str)
    df_corr = df[['Catagory', 'Unit_Price', 'Sales_Volume', 'Inventory_Turnover_Rate']].dropna()
    
    corr_sales = df_corr['Unit_Price'].corr(df_corr['Sales_Volume'])
    corr_turnover = df_corr['Unit_Price'].corr(df_corr['Inventory_Turnover_Rate'])
    st.write(f"**Correlação entre Unit_Price e Sales_Volume:** {corr_sales:.5f}")
    st.write(f"**Correlação entre Unit_Price e Inventory_Turnover_Rate:** {corr_turnover:.5f}")
    
    fig6, ax6 = plt.subplots(figsize=(6,4))
    ax6.scatter(df_corr['Unit_Price'], df_corr['Sales_Volume'], alpha=0.7, color='blue')
    ax6.set_xlabel("Unit_Price")
    ax6.set_ylabel("Sales_Volume")
    ax6.set_title("Unit_Price vs Sales_Volume")
    st.pyplot(fig6)
    
    fig7, ax7 = plt.subplots(figsize=(6,4))
    ax7.scatter(df_corr['Unit_Price'], df_corr['Inventory_Turnover_Rate'], alpha=0.7, color='green')
    ax7.set_xlabel("Unit_Price")
    ax7.set_ylabel("Inventory_Turnover_Rate")
    ax7.set_title("Unit_Price vs Inventory_Turnover_Rate")
    st.pyplot(fig7)

# Questão 7: Análise dos Padrões de Datas
with st.expander("Pergunta 7: Análise dos Padrões de Datas"):
    st.markdown("""
    **Conclusão:**  
    A análise dos padrões de datas revela uma grande dispersão nos intervalos entre recebimento, último pedido e validade, com valores negativos sugerindo inconsistências no cadastro ou processos atípicos. Isso indica que há riscos de expiração e possíveis falhas na reposição, exigindo uma revisão dos ciclos de pedido para garantir a qualidade e disponibilidade dos produtos.    
    **Insights:**  
    - É necessário revisar e corrigir os registros de datas para garantir que os ciclos de reposição estejam de acordo com os prazos de validade.
    """)
    df['Date_Received'] = pd.to_datetime(df['Date_Received'], format="%m/%d/%Y", errors='coerce')
    df['Last_Order_Date'] = pd.to_datetime(df['Last_Order_Date'], format="%m/%d/%Y", errors='coerce')
    df['Expiration_Date'] = pd.to_datetime(df['Expiration_Date'], format="%m/%d/%Y", errors='coerce')
    
    df['Interval_Order'] = (df['Last_Order_Date'] - df['Date_Received']).dt.days
    df['Shelf_Life'] = (df['Expiration_Date'] - df['Date_Received']).dt.days
    
    fig8, (ax8, ax9) = plt.subplots(1, 2, figsize=(12,4))
    ax8.hist(df['Interval_Order'].dropna(), bins=30, edgecolor='black', color='skyblue')
    ax8.set_xlabel("Interval_Order (dias)")
    ax8.set_ylabel("Frequência")
    ax8.set_title("Distribuição do Interval_Order")
    ax9.hist(df['Shelf_Life'].dropna(), bins=30, edgecolor='black', color='lightgreen')
    ax9.set_xlabel("Shelf_Life (dias)")
    ax9.set_ylabel("Frequência")
    ax9.set_title("Distribuição do Shelf_Life")
    st.pyplot(fig8)
    
    st.subheader("Shelf_Life vs. Interval_Order")
    df_plot = df[['Interval_Order', 'Shelf_Life']].dropna()
    fig9, ax10 = plt.subplots(figsize=(8,6))
    ax10.scatter(df_plot['Interval_Order'], df_plot['Shelf_Life'], alpha=0.6, color='teal')
    ax10.set_xlabel("Interval_Order (dias)")
    ax10.set_ylabel("Shelf_Life (dias)")
    ax10.set_title("Shelf_Life vs. Interval_Order")
    min_val = min(df_plot['Interval_Order'].min(), df_plot['Shelf_Life'].min())
    max_val = max(df_plot['Interval_Order'].max(), df_plot['Shelf_Life'].max())
    ax10.plot([min_val, max_val], [min_val, max_val], 'r--', label='Linha de Equilíbrio')
    ax10.legend()
    st.pyplot(fig9)
