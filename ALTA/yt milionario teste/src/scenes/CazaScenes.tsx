// As 8 animações de "El caza soviético cancelado que nunca llegó a volar" (es, 27,0 min). Pedido do painel (automático).
// REGRA (25/09 + 26/09/2026): biblioteca + MAPA — Odometro, Documento, Colunas, Painel, MapaCampanha, Lista, LinhaDoTempo.
// Todo número é DITO na narração; cues em scripts/build_plan.py -> CUES na grafia do Whisper ("3 .000" -> "3", "T -37" ->
// "37", "Y -155" -> "155", "MiG -25" -> "25", "Su -27" -> "27").
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Colunas, LinhaDoTempo, Lista } from "./blocos";
import { Documento, Odometro } from "./biblioteca";
import { MapaCampanha } from "./arquivo2";
import { SceneProps } from "./shared";

// ---------------- 1. a exigência de 1957 (p05) ----------------
export const S01Exigencia: React.FC<SceneProps> = (p) => (
  <Odometro
    {...p}
    kicker="DEFENSA AÉREA SOVIÉTICA · EXIGENCIA DE 1957"
    valor={3000}
    cue="3"
    sep="."
    sufixo=" km/h"
    nota={{ texto: "y hasta 27 kilómetros de altitud", cue: "27" }}
  />
);

// ---------------- 2. o decreto de 4 de junho de 1958 (p09) ----------------
export const S02Decreto: React.FC<SceneProps> = (p) => (
  <Documento
    {...p}
    linhas={[
      "CONSEJO DE MINISTROS DE LA URSS · 4 DE JUNIO DE 1958",
      "",
      "Se autoriza la creación de un nuevo sistema de interceptación",
      "Denominación técnica: T-3A-9",
      "Avión del sistema: T-37",
      "Oficina de diseño: P. O. Sujói",
    ]}
    cue="1958"
    chave={4}
    carimbo={{ texto: "T-37", cue: "37", cor: colors.danger }}
  />
);

// ---------------- 3. titânio (p13) ----------------
export const S03Titanio: React.FC<SceneProps> = (p) => (
  <Colunas
    {...p}
    kicker="TITANIO SOLDADO · LA SECCIÓN TRASERA DEL FUSELAJE"
    tint={colors.accent}
    cols={[
      { titulo: "Ligero", texto: "y muy resistente", cue: "ligero", cor: colors.cool },
      { titulo: "Soporta el calor", texto: "que destruiría al aluminio", cue: "aluminio", cor: colors.accent },
      { titulo: "Carísimo", texto: "difícil de trabajar y de soldar", cue: "carisimo", cor: colors.danger },
    ]}
  />
);

// ---------------- 4. as medidas do T-37 (p17) ----------------
export const S04Medidas: React.FC<SceneProps> = (p) => (
  <Painel
    {...p}
    spec={{
      kicker: "Sujói T-37 · el prototipo",
      titulo: "Una flecha con dos aletas",
      linhas: [
        { rotulo: "Largo", valor: "más de 19 m", cue: "19" },
        { rotulo: "Envergadura", valor: "8,5 m", cue: "8" },
        { rotulo: "Diámetro del fuselaje", valor: "1,70 m", cue: "70", destaque: true },
      ],
      tint: "accent",
    }}
  />
);

// ---------------- 5. a ordem de febrero de 1960 (p26) ----------------
export const S05Desguace: React.FC<SceneProps> = (p) => (
  <Documento
    {...p}
    linhas={[
      "COMITÉ ESTATAL DE TECNOLOGÍA AERONÁUTICA · FEBRERO DE 1960",
      "",
      "Programa T-37 (sistema T-3A-9): terminado",
      "El prototipo no será congelado",
      "Orden: desguazar el avión",
    ]}
    cue="1960"
    chave={4}
    carimbo={{ texto: "DESGUAZAR", cue: "desgua", cor: colors.danger }}
  />
);

// ---------------- 6. MAPA: a rota polar dos bombardeiros (p34) ----------------
const NORTEAMERICA: [number, number][] = [
  [70.0, -165.0], [71.3, -156.8], [69.5, -140.0], [69.4, -132.0], [68.5, -115.0], [67.8, -100.0], [69.0, -90.0],
  [66.5, -85.0], [62.0, -93.0], [58.8, -94.2], [55.0, -82.0], [51.5, -80.0], [55.5, -77.0], [60.0, -78.0],
  [62.5, -73.0], [58.5, -65.0], [52.5, -56.0], [47.5, -53.0],
];
const EURASIA: [number, number][] = [
  [69.0, 16.0], [71.0, 25.0], [69.5, 33.0], [66.5, 41.0], [68.5, 44.0], [67.8, 53.0], [69.5, 58.0], [70.5, 66.0],
  [73.0, 70.0], [72.0, 80.0], [74.5, 87.0], [76.5, 100.0], [77.7, 104.0], [73.5, 113.0], [72.5, 127.0],
  [71.5, 139.0], [72.5, 150.0], [70.0, 160.0], [69.5, 170.0], [66.0, 179.0],
];
export const S06Polo: React.FC<SceneProps> = (p) => (
  <MapaCampanha
    {...p}
    kicker="LA RUTA MÁS CORTA · CRUZANDO EL POLO NORTE"
    pontos={[
      { nome: "Norte soviético", lat: 68.0, lon: 70.0, data: "REGIONES INMENSAS · TU-128", cue: "norte" },
      { nome: "Estados Unidos", lat: 58.0, lon: -110.0, data: "BOMBARDEROS ESTRATÉGICOS", cue: "estadounidenses", lado: "esq" },
      { nome: "Polo Norte", lat: 86.0, lon: -20.0, data: "LA RUTA DEL ATAQUE", cue: "polo" },
    ]}
    setas={[
      { de: 1, para: 2, cue: "polo", cor: "#b3161b" },
      { de: 2, para: 0, cue: "128" },
    ]}
    costa={[NORTEAMERICA, EURASIA]}
  />
);

// ---------------- 7. a resposta da MiG (p44) ----------------
export const S07MiG25: React.FC<SceneProps> = (p) => (
  <Lista
    {...p}
    kicker="Mikoyán · Ye-155"
    titulo="La respuesta de MiG"
    tint={colors.cool}
    itens={[
      { titulo: "Más grande, con dos motores", cue: "dos" },
      { titulo: "Acero en lugar de titanio", cue: "acero" },
      { titulo: "Ye-155: primer vuelo en 1964", cue: "1964" },
      { titulo: "Se convertiría en el MiG-25", cue: "25", cor: colors.accent },
    ]}
  />
);

// ---------------- 8. o fim de Sukhoi (p54) ----------------
export const S08Sujoi: React.FC<SceneProps> = (p) => (
  <LinhaDoTempo
    {...p}
    kicker="PÁVEL SUJÓI"
    tint={colors.accent}
    marcos={[
      { ano: "1975", texto: "muere Pável Sujói", cue: "1975" },
      { ano: "T-4", texto: "el avión de titanio que sí voló", cue: "4" },
      { ano: "Su-27", texto: "el éxito que no llegó a ver", cue: "27", cor: colors.accent },
    ]}
  />
);
