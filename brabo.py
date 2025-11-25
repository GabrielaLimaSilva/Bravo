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
        padding: 15px;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 100%;
    }
    
    .titulo {
        font-size: 2em !important;
        font-weight: bold;
        text-align: center;
        color: white;
        margin-bottom: 15px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        padding: 0 10px;
    }
    
    .emoji-display {
        font-size: 100px;
        text-align: center;
        margin: 20px 0;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .nivel-texto {
        font-size: 1.3em;
        font-weight: bold;
        text-align: center;
        margin: 15px 0;
        padding: 12px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-size: 1.1em !important;
        font-weight: bold !important;
        padding: 12px 30px !important;
        border-radius: 50px !important;
        border: none !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3) !important;
        width: 100% !important;
        height: auto !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.4) !important;
    }
    
    /* Slider com gradiente */
    div.stSlider > div[data-baseweb="slider"] > div > div {
        background: linear-gradient(to right, #4CAF50, #FFC107, #FF5722) !important;
    }
    
    .resposta-registrada {
        background: white;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .resposta-registrada h3 {
        color: #667eea;
        margin-bottom: 10px;
        font-size: 1.2em;
    }
    
    .resposta-registrada p {
        margin: 8px 0;
        font-size: 1em;
    }
    
    /* Ajustes para mobile */
    @media (max-width: 640px) {
        .titulo {
            font-size: 1.5em !important;
            margin-bottom: 10px;
        }
        
        .emoji-display {
            font-size: 80px;
            margin: 15px 0;
        }
        
        .nivel-texto {
            font-size: 1.1em;
            padding: 10px;
            margin: 10px 0;
        }
        
        .stButton>button {
            font-size: 1em !important;
            padding: 10px 20px !important;
        }
        
        .resposta-registrada {
            padding: 15px;
        }
        
        .resposta-registrada p {
            font-size: 0.9em;
        }
    }
    
    /* Métricas responsivas */
    div[data-testid="stMetricValue"] {
        font-size: 1.5em;
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 0.9em;
    }
    
    @media (max-width: 640px) {
        div[data-testid="stMetricValue"] {
            font-size: 1.2em;
        }
        
        div[data-testid="stMetricLabel"] {
            font-size: 0.8em;
        }
    }
    
    /* Tabela responsiva */
    div[data-testid="stDataFrame"] {
        font-size: 0.85em;
    }
    
    @media (max-width: 640px) {
        div[data-testid="stDataFrame"] {
            font-size: 0.75em;
        }
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
    st.markdown("---")
    nivel = st.slider(
        "Arraste a barra:",
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
                <p style="font-size: 1.3em; margin: 12px 0;">{ultima['emoji']} <strong>Nível {ultima['nivel']}</strong></p>
                <p style="font-size: 1em; margin: 8px 0;"><strong>{ultima['texto']}</strong></p>
                <p style="color: #666; font-size: 0.85em;">{ultima['timestamp']}</p>
                <p style="color: #666; font-size: 0.85em;">Total: {len(st.session_state.respostas)} registro(s)</p>
            </div>
        """, unsafe_allow_html=True)

# Seção de histórico (se houver respostas)
if len(st.session_state.respostas) > 0:
    st.markdown("---")
    st.markdown("## 📊 Histórico de Respostas")
    
    # Criar DataFrame
    df = pd.DataFrame(st.session_state.respostas)
    
    # Estatísticas rápidas
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total", len(st.session_state.respostas))
        mais_comum = df['nivel'].mode()[0]
        st.metric("Mais Comum", f"{mais_comum} {NIVEIS[mais_comum]['emoji']}")
    
    with col2:
        media = df['nivel'].mean()
        st.metric("Média", f"{media:.1f}")
        ultimo_nivel = st.session_state.respostas[-1]['nivel']
        st.metric("Último", f"{ultimo_nivel} {NIVEIS[ultimo_nivel]['emoji']}")
    
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
    st.markdown("### Ações")
    col_a, col_b = st.columns(2)
    
    with col_a:
        # Botão de exportar
        json_data = json.dumps(st.session_state.respostas, indent=2, ensure_ascii=False)
        st.download_button(
            label="💾 Exportar",
            data=json_data,
            file_name=f"respostas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col_b:
        # Botão de limpar
        if st.button("🗑️ Limpar", type="secondary", use_container_width=True):
            st.session_state.respostas = []
            st.session_state.mostrar_confirmacao = False
            st.rerun()
