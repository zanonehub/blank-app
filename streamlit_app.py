import streamlit as st
import scipy
from iapws import IAPWS97

# Funções para converter unidades
def converter_temperatura(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    if from_unit == "°C" and to_unit == "K":
        return value + 273.15
    elif from_unit == "K" and to_unit == "°C":
        return value - 273.15
    elif from_unit == "°C" and to_unit == "°F":
        return (value * 9/5) + 32
    elif from_unit == "°F" and to_unit == "°C":
        return (value - 32) * 5/9
    elif from_unit == "K" and to_unit == "°F":
        return (value - 273.15) * 9/5 + 32
    elif from_unit == "°F" and to_unit == "K":
        return (value - 32) * 5/9 + 273.15
    return value  # Caso padrão

def converter_pressao(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    if from_unit == "MPa" and to_unit == "Pa":
        return value * 1e6
    elif from_unit == "Pa" and to_unit == "MPa":
        return value / 1e6
    elif from_unit == "MPa" and to_unit == "bar":
        return value * 10
    elif from_unit == "bar" and to_unit == "MPa":
        return value / 10
    return value  # Caso padrão

def converter_entalpia(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    if from_unit == "kJ/kg" and to_unit == "J/kg":
        return value * 1e3
    elif from_unit == "J/kg" and to_unit == "kJ/kg":
        return value / 1e3
    return value  # Caso padrão

def converter_entropia(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    if from_unit == "kJ/kg·K" and to_unit == "J/kg·K":
        return value * 1e3
    elif from_unit == "J/kg·K" and to_unit == "kJ/kg·K":
        return value / 1e3
    return value  # Caso padrão

def converter_densidade(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    if from_unit == "kg/m³" and to_unit == "g/cm³":
        return value / 1e3
    elif from_unit == "g/cm³" and to_unit == "kg/m³":
        return value * 1e3
    return value  # Caso padrão

# Título da aplicação
st.title("Calculadora de Propriedades da Água - IAPWS")

# Entrada de dados
st.subheader("Selecione duas propriedades para calcular as demais")
st.text("Somente são válidos os pares: TP, Ph, Ps, hs, Tx e Px.")

# Propriedades disponíveis
propriedades = {
    "Temperatura": "T",
    "Pressão": "P",
    "Entalpia": "h",
    "Entropia": "s",
    "Densidade": "rho",
    "Título": "x"
}

# Unidades disponíveis para cada propriedade
unidades = {
    "Temperatura": ["°C", "K", "°F"],
    "Pressão": ["MPa", "Pa", "bar"],
    "Entalpia": ["kJ/kg", "J/kg"],
    "Entropia": ["kJ/kg·K", "J/kg·K"],
    "Densidade": ["kg/m³", "g/cm³"]
}

# Selecionar primeira propriedade e sua unidade
prop1_label = st.selectbox("Escolha a primeira propriedade", list(propriedades.keys()))
prop1_unidade = st.selectbox(f"Unidade de {prop1_label}", unidades.get(prop1_label, [""]))

# Entrada de valores para a primeira propriedade
prop1_value = st.number_input(f"Insira o valor de {prop1_label} ({prop1_unidade})")

# Filtrar a segunda propriedade para excluir a primeira
filtered_props = {k: v for k, v in propriedades.items() if k != prop1_label}

# Selecionar segunda propriedade e sua unidade
prop2_label = st.selectbox("Escolha a segunda propriedade", list(filtered_props.keys()))
prop2_unidade = st.selectbox(f"Unidade de {prop2_label}", unidades.get(prop2_label, [""]))

# Entrada de valores para a segunda propriedade
prop2_value = st.number_input(f"Insira o valor de {prop2_label} ({prop2_unidade})")

# Botão para calcular
if st.button("Calcular"):
    if propriedades[prop1_label] + propriedades[prop2_label] in ["TP","PT","Ph","hP","Ps","sP","hs","sh","Tx","xT","Px","xP"]:
        try:
            # Convertendo os valores de entrada para o formato correto
            if propriedades[prop1_label] == "T":
                prop1_value = converter_temperatura(prop1_value, prop1_unidade, "K")
            if propriedades[prop2_label] == "T":
                prop2_value = converter_temperatura(prop2_value, prop2_unidade, "K")
            if propriedades[prop1_label] == "P":
                prop1_value = converter_pressao(prop1_value, prop1_unidade, "MPa")
            if propriedades[prop2_label] == "P":
                prop2_value = converter_pressao(prop2_value, prop2_unidade, "MPa")
            if propriedades[prop1_label] == "h":
                prop1_value = converter_entalpia(prop1_value, prop1_unidade, "kJ/kg")
            if propriedades[prop2_label] == "h":
                prop2_value = converter_entalpia(prop2_value, prop2_unidade, "kJ/kg")
            if propriedades[prop1_label] == "s":
                prop1_value = converter_entropia(prop1_value, prop1_unidade, "kJ/kg·K")
            if propriedades[prop2_label] == "s":
                prop2_value = converter_entropia(prop2_value, prop2_unidade, "kJ/kg·K")
            if propriedades[prop1_label] == "rho":
                prop1_value = converter_densidade(prop1_value, prop1_unidade, "kg/m³")
            if propriedades[prop2_label] == "rho":
                prop2_value = converter_densidade(prop2_value, prop2_unidade, "kg/m³")

            # Criando uma instância do IAPWS97 com as propriedades fornecidas
            kwargs = {propriedades[prop1_label]: prop1_value, propriedades[prop2_label]: prop2_value}
            agua = IAPWS97(**kwargs)
            
            # Exibindo as propriedades restantes com conversão para as unidades escolhidas
            st.subheader("Propriedades da Água Calculadas")
            st.write(f"Energia Interna (kJ/kg): {agua.u:.2f}")
            if propriedades[prop1_label] != "T" and propriedades[prop2_label] != "T":
                temperatura = converter_temperatura(agua.T, "K", "°C")
                st.write(f"Temperatura (°C): {temperatura:.2f}")
            if propriedades[prop1_label] != "P" and propriedades[prop2_label] != "P":
                pressao = converter_pressao(agua.P, "MPa", "MPa")
                st.write(f"Pressão (MPa): {pressao:.2f}")
            if propriedades[prop1_label] != "h" and propriedades[prop2_label] != "h":
                entalpia = converter_entalpia(agua.h, "kJ/kg", "kJ/kg")
                st.write(f"Entalpia (kJ/kg): {entalpia:.2f}")
            if propriedades[prop1_label] != "s" and propriedades[prop2_label] != "s":
                entropia = converter_entropia(agua.s, "kJ/kg·K", "kJ/kg·K")
                st.write(f"Entropia (kJ/kg·K): {entropia:.4f}")
            if propriedades[prop1_label] != "rho" and propriedades[prop2_label] != "rho":
                densidade = converter_densidade(agua.rho, "kg/m³", "kg/m³")
                st.write(f"Densidade (kg/m³): {densidade:.2f}")
                st.write(f"Volume específico (m³/kg): {agua.v:.5f}")
            if propriedades[prop1_label] == "x" or propriedades[prop2_label] == "x":
                st.write(f"Título (x): {agua.x:.2f}")
        except Exception as e:
            st.error(f"Erro ao calcular as propriedades: {str(e)}")

        try:
            st.write(f"Energia Livre de Gibbs (kJ/kg): {agua.g:.2f}")
        except Exception as e:
            st.caption(f":red[Não foi possível calcular a Energia Livre de Gibbs.]")
        try:
            st.write(f"Energia Livre de Helmholtz (kJ/kg): {agua.a:.2f}")
        except Exception as e:
            st.caption(f":red[Não foi possível calcular a Energia Livre de Helmholtz.]")
        try:
            st.write(f"Calor Específico a Pressão Constante (kJ/kg·K): {agua.cp:.2f}")
        except Exception as e:
            st.caption(f":red[Não foi possível calcular o Calor Específico a Pressão Constante.]")
        try:
            st.write(f"Calor Específico a Volume Constante (kJ/kg·K): {agua.cv:.2f}")
        except Exception as e:
            st.caption(f":red[Não foi possível calcular o Calor Específico a Volume Constante.]")
        try:
            st.write(f"Fator de Compressibilidade: {agua.Z:.2f}")
        except Exception as e:
            st.caption(f":red[Não foi possível calcular a Fator de Compressibilidade.]")
        try:
            st.write(f"Fugacidade (MPa): {agua.Z:.2f}")
        except Exception as e:
            st.caption(f":red[Não foi possível calcular a Fugacidade.]")
        try:
            st.write(f"Viscosidade Dinâmica (Pa·s): {agua.mu:.6f}")
        except Exception as e:
            st.caption(f":red[Não foi possível calcular a Viscosidade Dinâmica.]")
        try:
            st.write(f"Viscosidade Cinemática (m²/ss): {agua.nu:.6f}")
        except Exception as e:
            st.caption(f":red[Não foi possível calcular a Viscosidade Cinemática.]")
        try:
            st.write(f"Condutividade Térmica (W/m·K): {agua.k:.5f}")
        except Exception as e:
            st.caption(f":red[Não foi possível calcular a Condutividade Térmica.]")
        try:
            st.write(f"Difusividade Térmica (m²/s): {agua.alfa:.5f}")
        except Exception as e:
            st.caption(f":red[Não foi possível calcular a Difusividade Térmica.]")
        try:
            st.write(f"Velocidade do Som (m/s): {agua.w:.5f}")
        except Exception as e:
            st.caption(f":red[Não foi possível calcular a Velocidade do Som.]")
        try:
            st.write(f"Tensão de Superfície (N/m): {agua.sigma:.5f}")
        except Exception as e:
            st.caption(f":red[Não foi possível calcular a Tensão de Superfície.]")
        try:
            st.write(f"Número de Prandtl: {agua.Prandt:.5f}")
        except Exception as e:
            st.caption(f":red[Não foi possível calcular o Número de Prandtl.]")
        try:
            st.write(f"Temperatura Reduzida: {agua.Tr:.5f}")
        except Exception as e:
            st.caption(f":red[Não foi possível calcular a Temperatura Reduzida.]")
        try:
            st.write(f"Pressão Reduzida: {agua.Pr:.5f}")
        except Exception as e:
            st.caption(f":red[Não foi possível calcular a Pressão Reduzida.]")
    else:
        st.error(f"Essa combinação de propriedades não está implementada ainda :(")
