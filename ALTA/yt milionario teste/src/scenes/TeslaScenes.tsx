// As 8 animações de "A linha Tesla 2027" (pt, 23,5 min). 20 % vídeo / 80 % foto.
// REGRA (25/09 + 26/09/2026): animação em JavaScript pela BIBLIOTECA e todo filme com MAPA — Painel (3), Barras (2),
// MapaCampanha, LinhaDoTempo, Lista. Todo número é DITO na narração; cues em scripts/build_plan.py -> CUES
// (grafia do Whisper: "1 .400" -> cue "400"; "1 .020" -> "020"; "US $ 1 .990" -> "990"; "AI -5").
import React from "react";
import { colors } from "../design/tokens";
import { Painel, PainelSpec } from "./Painel";
import { Barras, LinhaDoTempo, Lista } from "./blocos";
import { MapaCampanha } from "./arquivo2";
import { SceneProps } from "./shared";

const painel = (spec: PainelSpec): React.FC<SceneProps> => {
  const C: React.FC<SceneProps> = (p) => <Painel {...p} spec={spec} />;
  return C;
};

// ---------------- 1. Cybercab ----------------
export const T01Cybercab = painel({
  kicker: "Tesla Cybercab",
  titulo: "Dois lugares, nenhum volante",
  linhas: [
    { rotulo: "Motor", valor: "um só, 219 cv", cue: "219" },
    { rotulo: "Bateria", valor: "~48 kWh (células 4680)", cue: "48" },
    { rotulo: "Autonomia", valor: "~470 km", cue: "470", destaque: true },
    { rotulo: "Peso", valor: "pouco mais de 1.400 kg", cue: "400" },
  ],
  tint: "accent",
});

// ---------------- 2. Semi ----------------
export const T02Semi: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="Tesla Semi · nova versão"
    titulo="Autonomia rodando carregado"
    tint={colors.accent}
    max={800}
    barras={[
      { rotulo: "Alcance padrão · 548 kWh", valor: "~520 km", v: 520, cue: "548", cor: colors.textDim },
      { rotulo: "Longo alcance · 822 kWh", valor: "~800 km", v: 800, cue: "822", cor: colors.accent },
    ]}
    nota={{ texto: "+15 % de eficiência · 1,7 kWh por milha", cue: "15" }}
  />
);

// ---------------- 3. expansão do robotáxi (MAPA obrigatório) ----------------
export const T03Expansao: React.FC<SceneProps> = (p) => (
  <MapaCampanha
    {...p}
    kicker="CYBERCAB · AUSTIN É SÓ O COMEÇO"
    pontos={[
      { nome: "Austin", lat: 30.27, lon: -97.74, data: "SET 2026 · CORRIDAS PAGAS", cue: "austin" },
      { nome: "Miami", lat: 25.76, lon: -80.19, cue: "miami" },
      { nome: "Dallas", lat: 32.78, lon: -96.8, cue: "dallas" },
      { nome: "Phoenix", lat: 33.45, lon: -112.07, cue: "phoenix" },
      { nome: "Las Vegas", lat: 36.17, lon: -115.14, cue: "vegas" },
    ]}
    setas={[
      { de: 0, para: 1, cue: "miami" },
      { de: 0, para: 2, cue: "dallas" },
      { de: 0, para: 3, cue: "phoenix" },
      { de: 0, para: 4, cue: "vegas" },
    ]}
  />
);

// ---------------- 4. Roadster ----------------
export const T04Roadster = painel({
  kicker: "Tesla Roadster · 2ª geração",
  titulo: "O último carro para dirigir",
  linhas: [
    { rotulo: "Potência", valor: "mais de 1.020 cv", cue: "020" },
    { rotulo: "Torque", valor: "mais de 1.400 N·m", cue: "newton" },
    { rotulo: "Velocidade máxima", valor: "acima de 400 km/h", cue: "quilometros", destaque: true },
    { rotulo: "Produção", valor: "Gigafactory Texas, 2027", cue: "2027" },
  ],
  tint: "danger",
});

// ---------------- 5. Optimus ----------------
export const T05Optimus: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="Optimus · capacidade planejada"
    titulo="Robôs por ano"
    tint={colors.cool}
    max={10}
    barras={[
      { rotulo: "Linha de Fremont", valor: "1 milhão", v: 1, cue: "milhao", cor: colors.textDim },
      { rotulo: "Gigafactory Texas", valor: "10 milhões", v: 10, cue: "10", cor: colors.cool },
    ]}
    nota={{ texto: "Musk: cerca de 80 % do valor futuro da Tesla virá do Optimus.", cue: "80" }}
  />
);

// ---------------- 6. Model Y L ----------------
export const T06ModelYL = painel({
  kicker: "Tesla Model Y L",
  titulo: "Seis lugares em três fileiras",
  linhas: [
    { rotulo: "Preço de lançamento (EUA)", valor: "US$ 61.990", cue: "990", destaque: true },
    { rotulo: "0 a 96 km/h", valor: "4,4 s", cue: "96" },
    { rotulo: "Autonomia", valor: "~520 km", cue: "520" },
    { rotulo: "Recarga", valor: "250 kW · ~260 km em 15 min", cue: "260" },
  ],
  tint: "accent",
});

// ---------------- 7. chips ----------------
export const T07Chips: React.FC<SceneProps> = (p) => (
  <LinhaDoTempo
    {...p}
    kicker="Os chips da Tesla"
    tint={colors.cool}
    marcos={[
      { ano: "AI5", texto: "Samsung + TSMC, em ~1 ano", cue: "tsmc" },
      { ano: "até 50x", texto: "o chip atual, AI4", cue: "50" },
      { ano: "AI6", texto: "só na fábrica da Samsung no Texas", cue: "exclusivamente" },
      { ano: "AI7 · AI8", texto: "fábrica própria de semicondutores", cue: "semicondutores", cor: colors.accent },
    ]}
  />
);

// ---------------- 8. o mapa de invasão ----------------
export const T08Invasao: React.FC<SceneProps> = (p) => (
  <Lista
    {...p}
    kicker="Um mapa de invasão"
    titulo="Quem está na mira"
    tint={colors.danger}
    itens={[
      { titulo: "Cybercab", texto: "táxis e transporte por aplicativo", cue: "cybercab" },
      { titulo: "Semi", texto: "fabricantes de caminhões e transportadoras", cue: "semi" },
      { titulo: "Roadster", texto: "supercarros europeus", cue: "roadster" },
      { titulo: "Optimus", texto: "o trabalho manual", cue: "optimus", cor: colors.danger },
    ]}
  />
);
