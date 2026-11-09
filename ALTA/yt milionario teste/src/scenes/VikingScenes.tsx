// As 9 animações de "La granja vikinga bajo la arena de Groenlandia" (es, padrão). Pedido do painel (automático, baia 1).
// REGRA (25/09 + 26/09/2026): biblioteca + MAPA — MapaCampanha, Painel, Odometro, LinhaDoTempo, Colunas, Lista.
// Todo número é DITO na narração; cues na grafia do Whisper ("Kingitor Swak", "Norderseta", "985").
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Colunas, LinhaDoTempo, Lista } from "./blocos";
import { MapaCampanha } from "./arquivo2";
import { SceneProps } from "./shared";

// Groenlândia e Islândia simplificadas (lat, lon)
const GROENLANDIA: [number, number][] = [
  [59.8, -43.9], [60.6, -46.2], [61.9, -49.3], [63.2, -50.9], [64.2, -51.8], [65.6, -53.0], [66.9, -53.8], [68.7, -53.2],
  [69.6, -51.4], [70.8, -54.2], [72.6, -55.8], [74.5, -57.6], [76.2, -62.0], [77.5, -70.0], [79.0, -72.0], [81.0, -62.0],
  [82.5, -40.0], [83.3, -30.0], [81.5, -15.0], [79.0, -19.0], [76.0, -19.5], [73.0, -22.0], [70.5, -22.0], [68.5, -28.0],
  [66.0, -35.0], [65.0, -40.0], [63.0, -41.0], [61.0, -42.5], [59.8, -43.9],
];
const ISLANDIA: [number, number][] = [
  [63.4, -19.0], [63.8, -22.6], [64.8, -24.0], [65.5, -24.4], [66.4, -23.0], [66.5, -18.0], [66.2, -15.0], [65.6, -13.6],
  [64.4, -14.5], [63.8, -16.5], [63.4, -19.0],
];

// ---------------- 1. MAPA: o vale a 80 km de Nuuk (p01) ----------------
export const V01Valle: React.FC<SceneProps> = (p) => (
  <MapaCampanha
    {...p}
    kicker="GROENLANDIA · EL VALLE DE LA GRANJA"
    pontos={[
      { nome: "Nuuk", lat: 64.18, lon: -51.72, data: "LA CAPITAL ACTUAL", cue: "nuuk", lado: "esq" },
      { nome: "La granja", lat: 64.15, lon: -49.9, data: "A UNOS 80 KM AL ESTE", cue: "80" },
      { nome: "Capa de hielo", lat: 70.0, lon: -40.0, data: "CUBRE CASI TODA LA ISLA", cue: "capa" },
    ]}
    setas={[{ de: 0, para: 1, cue: "80", cor: "#b3161b" }]}
    costa={[GROENLANDIA]}
  />
);

// ---------------- 2. MAPA: a frota de Erik (p08) ----------------
export const V02Flota: React.FC<SceneProps> = (p) => (
  <MapaCampanha
    {...p}
    kicker="ALREDEDOR DEL AÑO 985 · LA FLOTA DE ERIK EL ROJO"
    pontos={[
      { nome: "Islandia", lat: 64.8, lon: -21.0, data: "PARTIERON UNOS 25 BARCOS", cue: "25" },
      { nome: "Groenlandia", lat: 61.1, lon: -45.5, data: "SOLO 14 LLEGARON", cue: "14", lado: "esq" },
    ]}
    setas={[{ de: 0, para: 1, cue: "25", cor: "#b3161b" }]}
    costa={[GROENLANDIA, ISLANDIA]}
  />
);

// ---------------- 3. os dois assentamentos (p10) ----------------
export const V03Asentamientos: React.FC<SceneProps> = (p) => (
  <Colunas
    {...p}
    kicker="DOS ZONAS DE COLONOS"
    tint={colors.cool}
    cols={[
      { titulo: "Asentamiento Oriental", texto: "el más grande, en el sur", cue: "asentamiento", cor: colors.accent },
      { titulo: "Asentamiento Occidental", texto: "a unos 500 km, más al norte", cue: "500", cor: colors.cool },
      { titulo: "Paralelo 64", texto: "cerca del círculo polar ártico", cue: "64", cor: colors.danger },
    ]}
  />
);

// ---------------- 4. o inverno das vacas (p12) ----------------
export const V04Invierno: React.FC<SceneProps> = (p) => (
  <Lista
    {...p}
    kicker="VACAS EN EL ÁRTICO"
    titulo="El invierno groenlandés"
    tint={colors.danger}
    itens={[
      { titulo: "Siete u ocho meses encerradas", cue: "siete" },
      { titulo: "Alimentadas con el heno del verano", cue: "heno" },
      { titulo: "Si el heno no alcanzaba, el ganado moría", cue: "ganado" },
      { titulo: "Y la familia quedaba al borde del hambre", cue: "familia", cor: colors.danger },
    ]}
  />
);

// ---------------- 5. as camadas da granja (p22) ----------------
export const V05Capas: React.FC<SceneProps> = (p) => (
  <Colunas
    {...p}
    kicker="UN PASTEL DE CAPAS"
    tint={colors.accent}
    cols={[
      { titulo: "Construir", texto: "muros de turba y piedra", cue: "levantado", cor: colors.cool },
      { titulo: "La crecida", texto: "el río deja una capa de arena", cue: "inundaba", cor: colors.accent },
      { titulo: "Reconstruir encima", texto: "cada estrato, un momento distinto", cue: "reconstruia", cor: colors.danger },
    ]}
  />
);

// ---------------- 6. o que o ADN disse (p33) ----------------
export const V06ADN: React.FC<SceneProps> = (p) => (
  <Painel
    {...p}
    spec={{
      kicker: "ADN antiguo en el sedimento · revista Antiquity",
      titulo: "Lo que dijo la genética",
      linhas: [
        { rotulo: "Vacas, ovejas y cabras", valor: "confirmadas", cue: "vacas" },
        { rotulo: "Bisonte", valor: "sin rastro", cue: "bisonte" },
        { rotulo: "Oso pardo, buey almizclero", valor: "sin rastro", cue: "oso" },
        { rotulo: "Los pelos exóticos", valor: "mal clasificados", cue: "clasificados", destaque: true },
      ],
      tint: "cool",
    }}
  />
);

// ---------------- 7. MAPA: Norðrseta e as morsas (p40) ----------------
export const V07Marfil: React.FC<SceneProps> = (p) => (
  <MapaCampanha
    {...p}
    kicker="NORÐRSETA · LOS TERRITORIOS DEL NORTE"
    pontos={[
      { nome: "Asentamientos", lat: 64.2, lon: -51.7, data: "PARTIDA CADA VERANO", cue: "zarpaban", lado: "esq" },
      { nome: "Bahía de Disko", lat: 69.2, lon: -52.0, data: "CAZA DE MORSAS", cue: "disko", lado: "esq" },
    ]}
    setas={[{ de: 0, para: 1, cue: "norte", cor: "#b3161b" }]}
    costa={[GROENLANDIA]}
  />
);

// ---------------- 8. a pedra rúnica de Kingittorsuaq (p43) ----------------
export const V08Runas: React.FC<SceneProps> = (p) => (
  <LinhaDoTempo
    {...p}
    kicker="LA PIEDRA RÚNICA DE KINGITTORSUAQ"
    tint={colors.accent}
    marcos={[
      { ano: "1824", texto: "un groenlandés encuentra la piedra", cue: "1824" },
      { ano: "73° N", texto: "muy por encima del círculo polar", cue: "73" },
      { ano: "Tres hombres", texto: "Erlingur, Bjarni y Eindridi", cue: "tres" },
      { ano: "Siglo XIV", texto: "fechada por el estilo de las runas", cue: "xiv", cor: colors.accent },
    ]}
  />
);

// ---------------- 9. a Pequena Idade do Gelo (p48) ----------------
export const V09Hielo: React.FC<SceneProps> = (p) => (
  <Lista
    {...p}
    kicker="DESDE EL SIGLO XIII · LA PEQUEÑA EDAD DE HIELO"
    titulo="Cuando el clima cambió"
    tint={colors.cool}
    itens={[
      { titulo: "Veranos más cortos", cue: "veranos" },
      { titulo: "El hielo marino bloquea los fiordos", cue: "marino" },
      { titulo: "Tormentas más violentas", cue: "tormentas" },
      { titulo: "Cada verano malo, un golpe directo", cue: "golpe", cor: colors.danger },
    ]}
  />
);
