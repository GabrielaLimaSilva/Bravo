import streamlit as st
import pandas as pd
from datetime import datetime
import json

# Configuração da página
st.set_page_config(
    page_title="Quão Brabo Você Está? 😤",
    page_icon="💥",
    layout="centered"
)

# Estilo customizado
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .titulo {
        font-size: 3em !important;
        font-weight: bold;
        text-align: center;
        color: white;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .emoji-display {
        font-size: 150px;
        text-align: center;
        margin: 30px 0;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .nivel-texto {
        font-size: 2em;
        font-weight: bold;
        text-align: center;
        margin: 20px 0;
        padding: 15px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .emoji-scale {
        display: flex;
        justify-content: space-between;
        font-size: 2.5em;
        margin: 30px 0;
        padding: 20px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .emoji-scale span {
        cursor: pointer;
        transition: transform 0.2s;
        padding: 5px;
    }
    
    .emoji-scale span:hover {
        transform: scale(1.3);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.3em;
        font-weight: bold;
        padding: 15px 40px;
        border-radius: 50px;
        border: none;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.4);
    }
    
    div.stSlider > div[data-baseweb="slider"] > div > div {
        background: linear-gradient(to right, #4CAF50, #FFC107, #FF5722);
    }
    
    .resposta-registrada {
        background: white;
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .resposta-registrada h3 {
        color: #667eea;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Configuração dos níveis
NIVEIS = {
    0: {'emoji': '😊', 'texto': 'Zen Total', 'cor': '#4CAF50'},
    1: {'emoji': '🙂', 'texto': 'Tranquilinho', 'cor': '#8BC34A'},
    2: {'emoji': '😐', 'texto': 'Neutro', 'cor': '#CDDC39'},
    3: {'emoji': '😑', 'texto': 'Levemente Irritado', 'cor': '#FFEB3B'},
    4: {'emoji': '😒', 'texto': 'Chateado', 'cor': '#FFC107'},
    5: {'emoji': '😠', 'texto': 'Brabo', 'cor': '#FF9800'},
    6: {'emoji': '😡', 'texto': 'Muito Brabo', 'cor': '#FF5722'},
    7: {'emoji': '🤬', 'texto': 'Xingando Tudo', 'cor': '#F44336'},
    8: {'emoji': '💢', 'texto': 'Explosivo', 'cor': '#E91E63'},
    9: {'emoji': '🔥', 'texto': 'Fervendo de Raiva', 'cor': '#9C27B0'},
    10: {'emoji': '💥', 'texto': 'DETONADO!!!', 'cor': '#673AB7'}
}

# Inicializar session state
if 'respostas' not in st.session_state:
    st.session_state.respostas = []
if 'nivel_atual' not in st.session_state:
    st.session_state.nivel_atual = 0
if 'mostrar_confirmacao' not in st.session_state:
    st.session_state.mostrar_confirmacao = False

# Título
st.markdown('<h1 class="titulo">Quão Brabo Você Está? 😤</h1>', unsafe_allow_html=True)

# Container branco para o conteúdo
with st.container():
    # Emoji grande
    nivel_info = NIVEIS[st.session_state.nivel_atual]
    st.markdown(f'<div class="emoji-display">{nivel_info["emoji"]}</div>', unsafe_allow_html=True)
    
    # Texto do nível
    st.markdown(
        f'<div class="nivel-texto" style="color: {nivel_info["cor"]}">Nível {st.session_state.nivel_atual}: {nivel_info["texto"]}</div>',
        unsafe_allow_html=True
    )
    
    # Slider
    nivel = st.slider(
        "Arraste para escolher o nível:",
        min_value=0,
        max_value=10,
        value=st.session_state.nivel_atual,
        key="slider_nivel"
    )
    
    # Atualizar estado quando slider mudar
    if nivel != st.session_state.nivel_atual:
        st.session_state.nivel_atual = nivel
        st.session_state.mostrar_confirmacao = False
        st.rerun()
    
    # Escala de emojis (labels)
    st.markdown("---")
    cols = st.columns(11)
    for i, col in enumerate(cols):
        with col:
            st.markdown(f"<div style='text-align: center; font-size: 0.8em;'>{i}</div>", unsafe_allow_html=True)
    
    # Escala de emojis clicáveis
    emoji_cols = st.columns(11)
    for i, col in enumerate(emoji_cols):
        with col:
            if st.button(NIVEIS[i]['emoji'], key=f"emoji_{i}", use_container_width=True):
                st.session_state.nivel_atual = i
                st.session_state.mostrar_confirmacao = False
                st.rerun()
    
    st.markdown("---")
    
    # Botão de registrar
    if st.button("📊 Registrar Resposta", key="btn_registrar"):
        # Criar registro
        registro = {
            'nivel': st.session_state.nivel_atual,
            'emoji': NIVEIS[st.session_state.nivel_atual]['emoji'],
            'texto': NIVEIS[st.session_state.nivel_atual]['texto'],
            'timestamp': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        }
        
        # Adicionar às respostas
        st.session_state.respostas.append(registro)
        st.session_state.mostrar_confirmacao = True
        st.rerun()
    
    # Mostrar confirmação
    if st.session_state.mostrar_confirmacao and len(st.session_state.respostas) > 0:
        ultima = st.session_state.respostas[-1]
        st.markdown(f"""
            <div class="resposta-registrada">
                <h3>✅ Resposta Registrada!</h3>
                <p style="font-size: 1.5em; margin: 15px 0;">{ultima['emoji']} <strong>Nível {ultima['nivel']}: {ultima['texto']}</strong></p>
                <p style="color: #666;">Registrado em: {ultima['timestamp']}</p>
                <p style="color: #666;">Total de registros: {len(st.session_state.respostas)}</p>
            </div>
        """, unsafe_allow_html=True)

# Seção de histórico (se houver respostas)
if len(st.session_state.respostas) > 0:
    st.markdown("---")
    st.markdown("## 📊 Histórico de Respostas")
    
    # Criar DataFrame
    df = pd.DataFrame(st.session_state.respostas)
    
    # Estatísticas rápidas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Respostas", len(st.session_state.respostas))
    
    with col2:
        media = df['nivel'].mean()
        st.metric("Nível Médio", f"{media:.1f}")
    
    with col3:
        mais_comum = df['nivel'].mode()[0]
        st.metric("Mais Comum", f"{mais_comum} {NIVEIS[mais_comum]['emoji']}")
    
    with col4:
        ultimo_nivel = st.session_state.respostas[-1]['nivel']
        st.metric("Último Nível", f"{ultimo_nivel} {NIVEIS[ultimo_nivel]['emoji']}")
    
    # Mostrar tabela de respostas
    st.markdown("### Últimas 10 Respostas")
    df_display = df[['timestamp', 'emoji', 'nivel', 'texto']].tail(10).iloc[::-1]
    df_display.columns = ['Data/Hora', 'Emoji', 'Nível', 'Descrição']
    st.dataframe(df_display, use_container_width=True, hide_index=True)
    
    # Gráfico de distribuição
    st.markdown("### Distribuição por Nível")
    distribuicao = df['nivel'].value_counts().sort_index()
    st.bar_chart(distribuicao)
    
    # Botões de ação
    col_a, col_b = st.columns(2)
    
    with col_a:
        # Botão de exportar
        json_data = json.dumps(st.session_state.respostas, indent=2, ensure_ascii=False)
        st.download_button(
            label="💾 Exportar Dados (JSON)",
            data=json_data,
            file_name=f"respostas_brabo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    with col_b:
        # Botão de limpar
        if st.button("🗑️ Limpar Histórico", type="secondary"):
            st.session_state.respostas = []
            st.session_state.mostrar_confirmacao = False
            st.rerun()
