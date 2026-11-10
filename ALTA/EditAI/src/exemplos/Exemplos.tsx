// VITRINE da biblioteca de animações (src/scenes/biblioteca.tsx) com dados de filmes já feitos.
// Serve de teste e de modelo de uso: `node scripts/render_exemplos.mjs` -> out/exemplos/*.mp4 + .png.
// Os cues aqui são quadros fixos (num filme vêm do CUES do build_plan.py, palavra dita na narração).
import React from "react";
import { Documento, FotoMedidor, MapaRota, Odometro } from "../scenes/biblioteca";

export const ExMapaRota: React.FC = () => (
  <MapaRota dur={200} t0={0} cues={{ neryungri: 20, aldan: 60, tommot: 85, bestyakh: 150, yakutsk: 155 }}
    kicker="AMUR–YAKUTSK MAINLINE" unidade="km"
    lugares={[
      { nome: "NERYUNGRI", lat: 56.66, lon: 124.72, valor: 0, cue: "neryungri" },
      { nome: "ALDAN", lat: 58.6, lon: 125.4, valor: 250, cue: "aldan" },
      { nome: "TOMMOT", lat: 58.96, lon: 126.29, valor: 360, cue: "tommot" },
      { nome: "NIZHNY BESTYAKH", lat: 61.96, lon: 129.92, valor: 810, cue: "bestyakh", abaixo: true },
    ]}
    linhas={[{ pontos: [[60.0, 127.6], [60.9, 128.5], [61.6, 129.3], [62.03, 129.75], [62.6, 129.9], [63.4, 129.6]] }]}
    marca={{ nome: "YAKUTSK", lat: 62.03, lon: 129.4, nota: "sem ponte — o trem para no rio", cue: "yakutsk" }} />
);

export const ExOdometro: React.FC = () => (
  <Odometro dur={170} t0={0} cues={{ mil: 10, recorde: 60, "2023": 80, "2024": 88, "2025": 96 }}
    kicker="PEDIDOS DE RECUPERAÇÃO JUDICIAL · 2025" valor={1990} cue="mil" sep="." foto="exemplos/trem.jpg"
    nota={{ texto: "recorde histórico — +56 % em um ano", cue: "recorde" }}
    barras={[
      { rotulo: "2023", v: 534, cue: "2023" },
      { rotulo: "2024", v: 1272, cue: "2024" },
      { rotulo: "2025", v: 1990, cue: "2025", destaque: true },
    ]} />
);

export const ExDocumento: React.FC = () => (
  <Documento dur={180} t0={0} cues={{ ministerio: 18, investigacao: 135 }} cue="ministerio" chave={7}
    linhas={[
      "MINISTÉRIO PÚBLICO FEDERAL",
      "Procedimento de investigação — abril de 2026",
      "",
      "Sinais de alerta apontados pelos técnicos:",
      "1. cobrança obrigatória de taxas de revendedores;",
      "2. venda de produto não homologado;",
      "3. pressão psicológica, urgência e escassez;",
      "4. dependência da entrada de novos clientes.",
    ]}
    carimbo={{ texto: "INVESTIGADA", cue: "investigacao" }} />
);

export const ExTermometro: React.FC = () => (
  <FotoMedidor dur={170} t0={0} cues={{ graus: 15 }} foto="exemplos/yakutsk.jpg" de={0} ate={-45} unidade="°C"
    cue="graus" efeito="gelo" legenda="Yakutsk, janeiro — às 6 da tarde" />
);
