// Exemplos do estilo ARQUIVO COLORIZADO (src/scenes/arquivo_colorizado.tsx) — prévias do painel e teste das peças.
import React from "react";
import { BarrasAC, CitacaoAC, DadoAC, LinhaDoTempoAC, MapaPergaminho, Polaroids } from "../scenes/arquivo_colorizado";

const D = 180;
const CUBA: [number, number][] = [[21.86, -84.95], [22.4, -84.4], [23.0, -83.2], [23.15, -82.4], [23.2, -81.6], [23.1, -80.6],
  [22.6, -79.6], [22.3, -78.3], [21.6, -77.2], [21.2, -76.0], [20.9, -75.4], [20.2, -74.15], [19.9, -75.0], [19.85, -76.0],
  [19.95, -77.5], [20.4, -77.7], [20.7, -78.5], [21.5, -78.8], [21.7, -80.3], [22.0, -81.2], [22.1, -81.9], [21.9, -82.8], [22.2, -84.0]];
const FLORIDA: [number, number][] = [[28.5, -82.8], [27.0, -82.4], [26.6, -82.1], [25.9, -81.7], [25.2, -81.1], [25.1, -80.5],
  [25.8, -80.2], [26.8, -80.05], [28.5, -80.6]];

export const ExACPolaroids: React.FC = () => (
  <Polaroids dur={D} t0={0} cues={{ a: 10, b: 50, c: 90 }} etiqueta="THE WAR OF 1898"
    fotos={[{ src: "exemplos_ac/a.jpg", legenda: "U.S. troops, Honolulu · 1898", cue: "a" },
      { src: "exemplos_ac/b.jpg", legenda: "U.S. troops, Puerto Rico · 1898", cue: "b" },
      { src: "exemplos_ac/c.jpg", legenda: "U.S. troops, Philippines · 1899", cue: "c" }]} />
);
export const ExACLinha: React.FC = () => (
  <LinhaDoTempoAC dur={D} t0={0} cues={{ a: 10, b: 55, c: 100 }} etiqueta="THE WAR OF 1898"
    marcos={[{ data: "FEBRUARY 15, 1898", texto: "The Maine explodes", cue: "a" }, { data: "JULY 3, 1898", texto: "Santiago", cue: "b" },
      { data: "DECEMBER 1898", texto: "The Treaty of Paris", cue: "c" }]} />
);
export const ExACBarras: React.FC = () => (
  <BarrasAC dur={D} t0={0} cues={{ a: 20, b: 70 }} titulo="Cuba's sugar crop" subtitulo="1894–1925"
    barras={[{ valor: 1, rotulo: "1894", texto: "One million tons", cue: "a" }, { valor: 5, rotulo: "mid-1920s", texto: "Over 5 million tons", cue: "b", destaque: true }]} />
);
export const ExACDado: React.FC = () => (
  <DadoAC dur={D} t0={0} cues={{ n: 40 }} titulo="The Philippine War" periodo="1899–1902" numero="More than 4,000" texto="American soldiers died" cueNumero="n" />
);
export const ExACCitacao: React.FC = () => (
  <CitacaoAC dur={D} t0={0} cues={{ d: 70 }} cueDestaque="d"
    linhas={["For the preservation of Cuban independence,", "the maintenance of a government adequate", "for the protection of life, property,"]}
    destaque="and individual liberty" />
);
export const ExACMapa: React.FC = () => (
  <MapaPergaminho dur={D} t0={0} cues={{ h: 30, d: 60 }} titulo="The richest prize" ano="1898" terras={[CUBA, FLORIDA]}
    enquadra={[[27.6, -86.2], [19.4, -73.6]]}
    lugares={[{ nome: "Florida", lat: 27.3, lon: -81.6, ponto: false }, { nome: "Cuba", lat: 21.2, lon: -78.6, ponto: false, grande: true },
      { nome: "Havana", lat: 23.13, lon: -82.38, cue: "h" }, { nome: "Key West", lat: 24.55, lon: -81.8, cue: "h", circulo: true }]}
    distancia={{ de: [24.55, -81.8], ate: [23.13, -82.38], texto: "90 MILES", cue: "d" }}
    rotas={[{ pontos: [[20.6, -79.5], [19.6, -76.6], [19.95, -75.85]], cor: "vermelho", cue: "d" }]} />
);
export const EXEMPLOS_AC = [["ExACPolaroids", ExACPolaroids], ["ExACLinha", ExACLinha], ["ExACBarras", ExACBarras],
  ["ExACDado", ExACDado], ["ExACCitacao", ExACCitacao], ["ExACMapa", ExACMapa]] as const;
