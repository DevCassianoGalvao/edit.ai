// As 7 animações de "O motor a água da Toyota" (pt, 24,1 min). 20 % vídeo / 80 % foto. Pedido do painel (car-pt).
// REGRA (25/09 + 26/09/2026): animação em JavaScript pela BIBLIOTECA e todo filme com MAPA — Barras, Lista, Documento,
// MapaCampanha, Odometro, Painel, Colunas (7 tipos). Todo número é DITO na narração; cues em scripts/build_plan.py ->
// CUES na grafia do Whisper ("1 .360", "1 .200", "moto perpétuo", "40 %"). Separador de milhar em pt = ponto.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Barras, Colunas, Lista } from "./blocos";
import { Documento, Odometro } from "./biblioteca";
import { MapaCampanha } from "./arquivo2";
import { SceneProps } from "./shared";

// ---------------- 1. balanço de energia da eletrólise (p07) ----------------
export const S01Balanco: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="Eletrólise · a conta da energia"
    titulo="Separar a água custa mais do que devolve"
    tint={colors.accent}
    max={100}
    barras={[
      { rotulo: "Energia para separar a água", valor: "no mínimo a mesma", v: 100, cue: "eletrolise", cor: colors.cool },
      { rotulo: "Energia devolvida ao queimar o hidrogênio", valor: "nunca mais do que isso", v: 82, cue: "minimo", cor: colors.textDim },
      { rotulo: "Perdas: calor, resistência, atrito", valor: "a conta nunca fecha", v: 18, cue: "calor", cor: colors.danger },
    ]}
  />
);

// ---------------- 2. o ciclo "perpétuo" (p08) ----------------
export const S02Ciclo: React.FC<SceneProps> = (p) => (
  <Lista
    {...p}
    kicker="O carro a água, passo a passo"
    titulo="O velho sonho do moto-perpétuo"
    tint={colors.cool}
    itens={[
      { titulo: "O motor queima hidrogênio e gera energia", cue: "queima" },
      { titulo: "Um alternador transforma parte dela em eletricidade", cue: "alternador" },
      { titulo: "A eletrólise separa a água em hidrogênio", cue: "eletrolise" },
      { titulo: "O hidrogênio volta para o motor", cue: "volta" },
      { titulo: "Em cada volta, o ciclo perde energia", cue: "perpetuo", cor: colors.danger },
    ]}
    nota={{ texto: "Não andaria nem 2 metros", cue: "metros" }}
  />
);

// ---------------- 3. o processo de Stanley Meyer (p11) ----------------
export const S03Meyer: React.FC<SceneProps> = (p) => (
  <Documento
    {...p}
    linhas={[
      "TRIBUNAL DO ESTADO DE OHIO · EUA",
      "",
      "Autores: dois investidores",
      "Réu: Stanley Meyer — “célula de combustível de água”",
      "Promessa: cruzar os EUA com 80 litros de água",
      "Perícia: eletrólise comum, nada de revolucionário",
      "Decisão (1996): devolver o dinheiro aos investidores",
    ]}
    cue="1996"
    chave={5}
    carimbo={{ texto: "FRAUDE GROSSEIRA", cue: "fraude", cor: colors.danger }}
  />
);

// ---------------- 4. o recorde do Mirai (MAPA, p31) ----------------
export const S04Recorde: React.FC<SceneProps> = (p) => (
  <MapaCampanha
    {...p}
    kicker="TOYOTA MIRAI · RECORDE GUINNESS · UM ÚNICO TANQUE · 1.360 KM"
    pontos={[
      { nome: "Gardena", lat: 33.89, lon: -118.31, data: "AGOSTO DE 2021 · PARTIDA E CHEGADA", cue: "agosto" },
      { nome: "San Diego", lat: 32.72, lon: -117.16, data: "SUL DA CALIFÓRNIA", cue: "sul" },
    ]}
    setas={[
      { de: 0, para: 1, cue: "360" },
      { de: 1, para: 0, cue: "845" },
    ]}
    costa={[
      // litoral do sul da Califórnia (Point Conception -> Tijuana) e a fronteira com o México: dá lugar ao mapa e
      // mantém San Diego acima da barra de cinema (sem a costa, os 2 pontos ocupavam a caixa inteira)
      [[34.45, -120.47], [34.41, -119.7], [34.27, -119.29], [34.03, -118.78], [34.01, -118.5], [33.74, -118.41],
       [33.75, -118.19], [33.6, -117.9], [33.46, -117.7], [33.19, -117.38], [32.85, -117.27], [32.7, -117.23], [32.53, -117.12]],
      [[32.53, -117.12], [32.62, -116.1], [32.72, -114.72]],
    ]}
  />
);

// ---------------- 5. a distorção do boato (p33) ----------------
export const S05Distorcao: React.FC<SceneProps> = (p) => (
  <Odometro
    {...p}
    kicker="O BOATO INFLOU O RECORDE EM MAIS DE"
    valor={40}
    cue="40"
    sufixo=" %"
    barras={[
      { rotulo: "Boato: 1.200 milhas", v: 1200, cue: "200" },
      { rotulo: "Recorde real: 845 milhas", v: 845, cue: "real", destaque: true },
    ]}
    nota={{ texto: "Três distorções numa frase só", cue: "tres" }}
  />
);

// ---------------- 6. a cadeia de eficiência do hidrogênio (p38) ----------------
export const S06Eficiencia: React.FC<SceneProps> = (p) => (
  <Painel
    {...p}
    spec={{
      kicker: "Da tomada até a roda · carro a hidrogênio",
      titulo: "Energia perdida em cada etapa",
      linhas: [
        { rotulo: "Eletrólise", valor: "perde energia", cue: "eletrolise" },
        { rotulo: "Comprimir a 700 atmosferas", valor: "perde mais", cue: "700" },
        { rotulo: "Caminhão até o posto", valor: "perde mais", cue: "caminhao" },
        { rotulo: "Célula de combustível", valor: "perde mais uma vez", cue: "celula" },
        { rotulo: "Sobra no fim da cadeia", valor: "cerca de 30 %", cue: "30", destaque: true },
      ],
      tint: "danger",
    }}
  />
);

// ---------------- 7. estratégia de múltiplos caminhos (p43) ----------------
export const S07Caminhos: React.FC<SceneProps> = (p) => (
  <Colunas
    {...p}
    kicker="TOYOTA · ESTRATÉGIA DE MÚLTIPLOS CAMINHOS"
    tint={colors.accent}
    cols={[
      { titulo: "Elétrico a bateria", texto: "cidades com boa rede elétrica", cue: "eletricos", cor: colors.cool },
      { titulo: "Híbrido", texto: "onde a recarga ainda é difícil", cue: "hibridos" },
      { titulo: "Biocombustível", texto: "o etanol no Brasil", cue: "biocombustiveis", cor: colors.accent },
      { titulo: "Hidrogênio", texto: "onde a bateria tem limites", cue: "hidrogenio", cor: colors.danger },
    ]}
  />
);
