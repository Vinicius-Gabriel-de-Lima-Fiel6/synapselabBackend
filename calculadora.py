import math
from chempy.chemistry import Substance

def calcular_analitica_fiel(operacao, dados):
    try:
        f = dados.get('f', 'NaCl')
        if operacao == "Molaridade (m/MM*V)":
            m, v = float(dados['m']), float(dados['v'])
            mm = Substance.from_formula(f).mass
            return m / (mm * (v/1000))
        elif operacao == "Diluição (C1V1=C2V2)":
            v1, c1, v2, c2 = float(dados['v1']), float(dados['c1']), float(dados['v2']), float(dados['c2'])
            if v2 == 0: return (c1 * v1) / c2
            return (c1 * v1) / v2
        elif operacao == "pH de Ácido Forte":
            return -math.log10(float(dados['h']))
        elif operacao == "pH de Base Forte":
            return 14 + math.log10(float(dados['oh']))
        elif operacao == "pOH":
            return -math.log10(float(dados['oh']))
        elif operacao == "Normalidade":
            return float(dados['mol']) * float(dados['eq'])
        elif operacao == "Fração Molar":
            return float(dados['ns']) / (float(dados['ns']) + float(dados['nt']))
        elif operacao == "PPM para Molaridade":
            return (float(dados['ppm'])/1000) / Substance.from_formula(f).mass
        elif operacao == "Porcentagem em Massa (%m/m)":
            return (float(dados['ms']) / float(dados['mt'])) * 100
        elif operacao == "Conversão g/L para mol/L":
            return float(dados['gl']) / Substance.from_formula(f).mass
        elif operacao == "Molalidade":
            return float(dados['ns']) / float(dados['kg'])
        elif operacao == "Rendimento Percentual":
            return (float(dados['exp']) / float(dados['teo'])) * 100
        elif operacao == "Fator de Diluição":
            return float(dados['vf']) / float(dados['vi'])
        elif operacao == "Volume Molar (CNTP)":
            return float(dados['n']) * 22.414
        elif operacao == "Densidade da Solução":
            return float(dados['m']) / float(dados['v'])
        return 0.0
    except: return 0.0

def calcular_termo_fiel(operacao, dados):
    try:
        if operacao == "Gases Ideais (PV=nRT)":
            return (float(dados['n'])*0.08206*float(dados['t_k']))/float(dados['v_l'])
        elif operacao == "Gases Reais (Van der Waals)":
            n, v, te, a, b = float(dados['n']), float(dados['v']), float(dados['te']), float(dados['a']), float(dados['b'])
            return ((n*0.08206*te)/(v-n*b))-(a*(n/v)**2)
        elif operacao == "Energia Livre de Gibbs (ΔG)":
            return float(dados['h']) - (float(dados['te']) * float(dados['s']))
        elif operacao == "Equação de Arrhenius (k)":
            return float(dados['a_f']) * math.exp(-float(dados['ea'])/(8.314*float(dados['te'])))
        elif operacao == "Tempo de Meia-Vida (1ª Ordem)":
            return 0.693 / float(dados['k'])
        elif operacao == "Entalpia (Q = m.c.ΔT)":
            return float(dados['m'])*float(dados['c'])*float(dados['dt'])
        elif operacao == "Equação de Henderson-Hasselbalch":
            return float(dados['pk']) + math.log10(float(dados['ba'])/float(dados['ac']))
        elif operacao == "Pressão Osmótica (π=iMRT)":
            return float(dados['i'])*float(dados['m'])*0.08206*float(dados['te'])
        return 0.0
    except: return 0.0

def converter_si_fiel(tipo, v):
    conv = {
        "Kg para g": v*1000, "g para Kg": v/1000, "mg para g": v/1000, "g para mg": v*1000,
        "L para mL": v*1000, "mL para L": v/1000, "m³ para L": v*1000, "Celsius para Kelvin": v+273.15,
        "Kelvin para Celsius": v-273.15, "Fahrenheit para Celsius": (v-32)*5/9, "atm para mmHg": v*760,
        "mmHg para atm": v/760, "bar para atm": v*0.9869, "psi para bar": v*0.0689, "Joules para Calorias": v/4.184
    }
    return conv.get(tipo, v)
