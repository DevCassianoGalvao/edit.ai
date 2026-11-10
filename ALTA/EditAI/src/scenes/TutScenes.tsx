// As 8 animações de "Arqueólogos abrieron la tumba de Tutankamón — y algo dentro no debía estar ahí" (es, 27,8 min).
// Pedido do painel (ULTRA automático, baia 1). REGRA (25/09 + 26/09/2026): biblioteca + MAPA — Documento, Lista,
// Odometro, Painel, MapaCampanha, LinhaDoTempo. Todo número é DITO na narração; cues em scripts/build_plan.py -> CUES
// na grafia do Whisper ("4", "100", "70", "80%", "2016", "Horem Hep", "Tushrata").
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { LinhaDoTempo, Lista } from "./blocos";
import { Documento, Odometro } from "./biblioteca";
import { MapaCampanha } from "./arquivo2";
import { SceneProps } from "./shared";

// ---------------- 1. o telegrama de Carter a Carnarvon (p04) ----------------
export const S01Telegrama: React.FC<SceneProps> = (p) => (
  <Documento
    {...p}
    linhas={[
      "TELEGRAMA · LUXOR → INGLATERRA · NOVIEMBRE DE 1922",
      "",
      "Por fin he hecho un descubrimiento maravilloso en el Valle;",
      "una tumba magnífica con los sellos intactos;",
      "la he vuelto a cubrir hasta su llegada.",
      "Felicidades.",
      "",
      "— CARTER",
    ]}
    cue="telegrama"
    chave={3}
    carimbo={{ texto: "LUXOR", cue: "semanas", cor: colors.danger }}
  />
);

// ---------------- 2. capelas encaixadas (p16) ----------------
export const S02Capillas: React.FC<SceneProps> = (p) => (
  <Lista
    {...p}
    kicker="Cámara funeraria · 17 de febrero de 1923"
    titulo="Como muñecas rusas"
    tint={colors.accent}
    itens={[
      { titulo: "4 capillas de madera dorada", cue: "4" },
      { titulo: "Un sarcófago de piedra", cue: "sarcofago" },
      { titulo: "3 ataúdes, uno dentro del otro", cue: "3" },
      { titulo: "El último, de oro macizo: más de 100 kilos", cue: "100", cor: colors.accent },
    ]}
  />
);

// ---------------- 3. o prazo ritual: 70 dias (p21) ----------------
export const S03Setenta: React.FC<SceneProps> = (p) => (
  <Odometro
    {...p}
    kicker="EL PLAZO RITUAL DEL ANTIGUO EGIPTO"
    valor={70}
    cue="70"
    sufixo=" días"
    nota={{ texto: "entre la muerte y el entierro — no había tiempo para más", cue: "entierro" }}
  />
);

// ---------------- 4. 80 % do enxoval (p29) ----------------
export const S04Ochenta: React.FC<SceneProps> = (p) => (
  <Odometro
    {...p}
    kicker="NICHOLAS REEVES · EL AJUAR FUNERARIO DE TUTANKAMÓN"
    valor={80}
    cue="80"
    sufixo=" %"
    nota={{ texto: "fabricado en origen para otra persona — no todos aceptan la cifra", cue: "especialistas" }}
  />
);

// ---------------- 5. a adaga: análise de 2016 (p45) ----------------
export const S05Daga: React.FC<SceneProps> = (p) => (
  <Painel
    {...p}
    spec={{
      kicker: "La daga de Tutankamón · análisis de 2016",
      titulo: "Hierro que vino del espacio",
      linhas: [
        { rotulo: "Año", valor: "2016", cue: "2016" },
        { rotulo: "Técnica", valor: "fluorescencia de rayos X", cue: "fluorescencia" },
        { rotulo: "Níquel", valor: "cerca de un 10 %", cue: "10" },
        { rotulo: "Cobalto", valor: "rastros", cue: "cobalto" },
        { rotulo: "Origen", valor: "meteoritos de hierro", cue: "meteoritos", destaque: true },
      ],
      tint: "accent",
    }}
  />
);

// ---------------- 6. MAPA: o presente de Mitanni (p48) ----------------
const MEDITERRANEO: [number, number][] = [
  [31.3, 25.2], [31.1, 27.2], [30.9, 29.0], [31.2, 29.9], [31.5, 31.0], [31.1, 32.3], [31.3, 34.2], [32.8, 34.9],
  [33.9, 35.5], [35.5, 35.8], [36.6, 36.2], [36.8, 34.6], [36.2, 32.9],
];
const NILO: [number, number][] = [[31.4, 30.4], [30.0, 31.2], [28.1, 30.8], [27.6, 30.9], [26.2, 32.7], [25.7, 32.6], [24.1, 32.9]];
const EUFRATES: [number, number][] = [[37.4, 38.3], [36.4, 38.1], [35.9, 39.0], [35.0, 40.4], [34.4, 41.0], [33.4, 43.4], [31.0, 46.0]];
const MAR_ROJO: [number, number][] = [[29.9, 32.6], [28.2, 33.2], [26.5, 34.1], [24.1, 35.6]];
export const S06Mitanni: React.FC<SceneProps> = (p) => (
  <MapaCampanha
    {...p}
    kicker="LAS CARTAS DE AMARNA · UN REGALO DIPLOMÁTICO"
    pontos={[
      { nome: "Amarna", lat: 27.65, lon: 30.9, data: "LA CORRESPONDENCIA DE LOS FARAONES", cue: "amarna", lado: "esq" },
      { nome: "Mitanni", lat: 36.8, lon: 40.0, data: "EL REY TUSHRATTA", cue: "mitanni" },
      { nome: "Tebas", lat: 25.7, lon: 32.65, data: "AMENHOTEP III · ABUELO DE TUTANKAMÓN", cue: "amenhotep" },
    ]}
    setas={[{ de: 1, para: 2, cue: "daga" }]}
    costa={[MEDITERRANEO, NILO, EUFRATES, MAR_ROJO]}
  />
);

// ---------------- 7. o fim da linhagem (p55) ----------------
export const S07Linaje: React.FC<SceneProps> = (p) => (
  <LinhaDoTempo
    {...p}
    kicker="EL FIN DE UNA DINASTÍA"
    tint={colors.accent}
    marcos={[
      { ano: "Tutankamón", texto: "muere sin herederos", cue: "herederos" },
      { ano: "Ay", texto: "un anciano cortesano", cue: "cortesano" },
      { ano: "Horemheb", texto: "un general", cue: "general", cor: colors.danger },
      { ano: "La tumba", texto: "olvidada — y por eso sobrevivió", cue: "olvidada", cor: colors.accent },
    ]}
  />
);

// ---------------- 8. os três escaneamentos (p60) ----------------
export const S08Radar: React.FC<SceneProps> = (p) => (
  <Lista
    {...p}
    kicker="Radar de penetración terrestre · KV62"
    titulo="¿Hay algo detrás de la pared?"
    tint={colors.cool}
    itens={[
      { titulo: "Primer análisis: espacios vacíos detrás de las paredes", cue: "primer" },
      { titulo: "Segundo estudio: no confirma los resultados", cue: "segundo" },
      { titulo: "2018 · Politécnica de Turín: no hay cámaras ocultas", cue: "2018", cor: colors.cool },
    ]}
  />
);
