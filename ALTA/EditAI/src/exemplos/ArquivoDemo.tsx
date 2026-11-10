// Amostras das animações de ARQUIVO (src/scenes/arquivo.tsx) — 6 variações para o usuário escolher (26/09/2026).
// Sem cues: cada elemento entra pela fração da duração (fallback do shared.cue).
import React from "react";
import { Checklist, FichaCirculo, QuadroProvas } from "../scenes/arquivo";
import { AntesDepois, Lupa, Manchete, MapaCampanha, Paralaxe, Revela, RoloFilme, Teletipo } from "../scenes/arquivo2";
import { CartelaCapitulo } from "../overlays/Ultra";
import { CadernoCampo, PainelMercado, PlantaTecnica, RadarTatico, VhsRetro } from "../scenes/estilos5";
import { AbsoluteFill, Img, staticFile } from "remotion";

const D = 210;
const base = { dur: D, t0: 0 };
const F = (n: string) => `demo_arquivo/${n}.jpg`;

export const ArqQuadro: React.FC = () => (
  <QuadroProvas {...base} titulo="INVESTIGAÇÃO" tituloCue="-" tom="sepia"
    provas={[
      { src: F("pd181f781"), x: 560, y: 560, rot: -5, cue: "-", w: 560 },
      { src: F("pca21b11a"), x: 1350, y: 590, rot: 4, cue: "-", w: 520 },
    ]} />
);

export const ArqQuadroFio: React.FC = () => (
  <QuadroProvas {...base} titulo="A CORRENTE" tituloCue="-" tom="pb" fio
    provas={[
      { src: F("pca21b11a"), x: 380, y: 560, rot: -6, cue: "-", w: 360, legenda: "o produtor" },
      { src: F("pd181f781"), x: 800, y: 700, rot: 3, cue: "-", w: 360, legenda: "a revenda" },
      { src: F("p5bb6b198"), x: 1180, y: 520, rot: -3, cue: "-", w: 360, legenda: "o banco" },
      { src: F("pa72330dc"), x: 1580, y: 690, rot: 5, cue: "-", w: 360, legenda: "a justiça" },
    ]} />
);

export const ArqChecklist: React.FC = () => (
  <Checklist {...base} fundo={F("p7e4adbe8")} titulo="CLÁUSULAS DO CRA"
    itens={[
      { texto: "Liquidez ≥ 0,9", cue: "-", marca: "check" },
      { texto: "Dívida ≤ 2,5x patrimônio", cue: "-", marca: "check" },
      { texto: "Dívida ≤ 4x o caixa", cue: "-", marca: "vazio" },
    ]} />
);

export const ArqChecklistX: React.FC = () => (
  <Checklist {...base} fundo={F("pe6b0e6c5")} titulo="O QUE FOI PROMETIDO" cor="#3d4a2a" lado="esquerda"
    itens={[
      { texto: "R$ 4 bilhões até 2027", cue: "-", marca: "x" },
      { texto: "Mil máquinas por ano", cue: "-", marca: "risco" },
      { texto: "Dívida sem susto", cue: "-", marca: "x" },
    ]} />
);

export const ArqFicha: React.FC = () => (
  <FichaCirculo {...base} nome="SLC MÁQUINAS" nomeCue="-" orgao="ASSEMBLEIA DE CREDORES — CRA"
    campos={[
      { rotulo: "Data", valor: "9 de janeiro de 2026" },
      { rotulo: "Pedido", valor: "Waiver de alavancagem" },
      { rotulo: "Presença", valor: "1,79 %", tarja: true },
      { rotulo: "Mínimo", valor: "30 %", tarja: true },
    ]}
    relatorio={2} foto={F("pd181f781")} carimbo="CONFIDENCIAL" />
);

export const ArqFichaRevela: React.FC = () => (
  <FichaCirculo {...base} nome="TECNOMAAC" nomeCue="-" orgao="5ª VARA CÍVEL DE DOURADOS — MS" modo="revelar"
    campos={[
      { rotulo: "Pedido", valor: "Recuperação judicial" },
      { rotulo: "Passivo", valor: "R$ 276 milhões", tarja: true },
      { rotulo: "Credores", valor: "352", tarja: true },
      { rotulo: "Suspensão", valor: "180 dias", tarja: true },
    ]}
    foto={F("p1eefee9a")} carimbo="DEFERIDO" />
);

// ---- efeitos que viraram regra (26/09/2026) — na duração REAL do cartão no filme (~5 s)

const C = { dur: 150, t0: 0 };
export const ArqManchete: React.FC = () => (
  <Manchete {...C} jornal="O Correio Rural" data="SÃO PAULO · AGOSTO DE 2026" titulo="Revendas de tratores no vermelho"
    sub="Prejuízo dobra mesmo com vendas em alta" foto={F("pd181f781")} />
);
export const ArqTelex: React.FC = () => (
  <Teletipo {...C} cabecalho="TELEX · ASSEMBLEIA DE CREDORES" data="09 JAN 2026 · 10:42"
    linhas={["QUORUM NAO ATINGIDO.", "PRESENCA: 1,79 POR CENTO.", "MINIMO EXIGIDO: 30 POR CENTO.", "NOVA DATA A DEFINIR."]} />
);
export const ArqLupa: React.FC = () => (
  <Lupa {...C} src={F("pd181f781")} x={0.36} y={0.44} r={0.1} rotulo="REVENDA JOHN DEERE · RS" />
);
export const ArqAntesDepois: React.FC = () => (
  <AntesDepois {...C} a={{ src: F("p7e4adbe8"), rotulo: "SAFRA CHEIA" }} b={{ src: F("pe6b0e6c5"), rotulo: "QUEBRA DE SAFRA" }} />
);
export const ArqRolo: React.FC = () => (
  <RoloFilme {...C} fotos={[F("p08b811fe"), F("pd181f781"), F("pca21b11a"), F("pa72330dc"), F("p5bb6b198")]} titulo="A CORRENTE DO AGRO" />
);
export const ArqRevela: React.FC = () => <Revela {...C} src={F("pca21b11a")} legenda="o produtor, 2026" />;
export const ArqParalaxe: React.FC = () => <Paralaxe {...C} src={F("pca21b11a")} fg="demo_arquivo/pca21b11a_fg.png" />;
export const ArqMapa: React.FC = () => (
  <MapaCampanha dur={180} t0={0} kicker="A CRISE SE ESPALHA · 2026"
    pontos={[
      { nome: "Rio Grande do Sul", lat: -29.7, lon: -53.2, data: "FEV 2026 · WAIVER", cue: "a" },
      { nome: "Rondonópolis", lat: -16.47, lon: -54.64, data: "JAN 2026 · RJ", cue: "b" },
      { nome: "Maracaju", lat: -21.61, lon: -55.17, data: "AGO 2026 · RJ", cue: "c" },
      { nome: "São Paulo", lat: -23.55, lon: -46.63, data: "B3 · PREJUÍZO", cue: "d" },
    ]}
    setas={[{ de: 3, para: 0, cue: "s1" }, { de: 3, para: 2, cue: "s2" }, { de: 2, para: 1, cue: "s3" }]} />
);
export const ArqCapitulo: React.FC = () => (
  <AbsoluteFill>
    <Img src={staticFile(F("p08b811fe"))} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
    <CartelaCapitulo nome="O OUTRO LADO DO BALCÃO" lugar="BRASÍLIA — JUNHO DE 2026" entra={6} fica={100} />
  </AbsoluteFill>
);


// ---------------------------------------------------------------- 04/10/2026: 5 estilos por gênero (prévias do painel)
const E = { dur: 180, t0: 0 };
export const ArqPlanta: React.FC = () => (
  <PlantaTecnica {...E} src={F("est_carro")} titulo="BYD Seal"
    cotas={[{ x1: 0.12, y1: 0.86, x2: 0.88, y2: 0.86, rotulo: "4,6 m" }, { x1: 0.93, y1: 0.2, x2: 0.93, y2: 0.82, rotulo: "1,7 m" }]}
    chamadas={[{ x: 0.28, y: 0.55, rotulo: "motor elétrico" }, { x: 0.55, y: 0.72, rotulo: "bateria" }]} folha="FOLHA 01 · ESC. 1:20" />
);
export const ArqCaderno: React.FC = () => (
  <CadernoCampo {...E} src={F("est_egito")} titulo="Câmara funerária" local="Vale dos Reis · Tumba 62" data="4 de novembro de 1922"
    notas={["selo intacto na porta", "degraus cobertos de entulho", "objetos de ouro"]} achado="ACHADO Nº 0427" escala="0 — 50 cm"
    circulo={{ x: 0.5, y: 0.45, r: 0.12 }} />
);
export const ArqMercado: React.FC = () => (
  <PainelMercado {...E} titulo="Área financiada · crédito rural" serie={[34.2, 33.5, 31.9, 30.1, 28.4, 27.0, 25.4]}
    rotulos={["jul/25", "out/25", "jan/26", "abr/26", "jul/26"]} valor="25,4" unidade="mi ha" variacao="25,8 %" sobe={false}
    ticker={["SOJA ▼ 2,1 %", "SELIC 14 %", "MILHO ▲ 0,8 %", "DÓLAR ▲ 0,4 %"]} />
);
export const ArqRadar: React.FC = () => (
  <RadarTatico {...E} src={F("est_navio")} titulo="USS GERALD R. FORD · ATLÂNTICO" coord="34°12'N  032°47'E" hora="0412 ZULU"
    alvos={[{ x: 0.5, y: 0.48, rotulo: "CVN-78" }]} />
);
export const ArqVhs: React.FC = () => (
  <VhsRetro {...E} src={F("est_retro")} data="12 MAR 1990" slogan="O carro do ano" marca="CANAL 4" />
);
