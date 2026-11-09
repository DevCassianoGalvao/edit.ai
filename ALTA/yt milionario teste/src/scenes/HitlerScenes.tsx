// Peças de "La verdadera razón por la que Hitler nunca invadió Turquía" (es) — painel 20261104-143541 (baia b1).
// ESTILO ARQUIVO COLORIZADO: só peças de src/scenes/arquivo_colorizado.tsx; todo número é dito; milhar com ponto (es).
import React from "react";
import { BarrasAC, CitacaoAC, DadoAC, LinhaDoTempoAC, MapaPergaminho, Polaroids } from "./arquivo_colorizado";
import { SceneProps } from "./shared";
import { TERRAS_HT } from "./HitlerGeo";

const TERRAS = TERRAS_HT;   // Natural Earth 50m (src/scenes/HitlerGeo.ts)

// 1. o mapa da primavera de 1941 (p01)
export const H01Primavera: React.FC<SceneProps> = (p) => (
  <MapaPergaminho {...p} titulo="La primavera de 1941" ano="1941" terras={TERRAS}
    enquadra={[[46.0, 18.5], [35.5, 36.0]]}
    lugares={[{ nome: "Turquía", lat: 39.0, lon: 33.5, ponto: false, grande: true },
      { nome: "Yugoslavia", lat: 44.2, lon: 20.5, ponto: false }, { nome: "Grecia", lat: 39.4, lon: 21.9, ponto: false },
      { nome: "Bulgaria", lat: 42.7, lon: 25.3, ponto: false, cue: "bulgaria" },
      { nome: "Ankara", lat: 39.93, lon: 32.86, cue: "ankara" }]}
    rotas={[{ pontos: [[44.6, 26.1], [43.7, 25.6], [42.9, 25.4], [41.9, 26.1]], cor: "vermelho", cue: "danubio", seta: true }]} />
);

// 2. Turquía, un puente (p04)
export const H02Puente: React.FC<SceneProps> = (p) => (
  <MapaPergaminho {...p} titulo="Turquía, un puente" ano="1941" terras={TERRAS}
    enquadra={[[42.6, 24.5], [29.6, 45.0]]}
    lugares={[{ nome: "Estambul", lat: 41.01, lon: 28.97, cue: "estambul" },
      { nome: "Anatolia", lat: 39.0, lon: 33.5, ponto: false, grande: true, cue: "anatolia" },
      { nome: "Siria", lat: 35.0, lon: 38.5, ponto: false, cue: "siria" }, { nome: "Irak", lat: 33.0, lon: 43.0, ponto: false, cue: "irak" },
      { nome: "Mosul", lat: 36.34, lon: 43.13, cue: "mosul" }, { nome: "Canal de Suez", lat: 30.3, lon: 32.4, cue: "suez", circulo: true }]}
    rotas={[{ pontos: [[41.3, 26.4], [41.01, 28.97], [39.93, 32.86], [37.0, 37.4], [36.34, 43.13]], cor: "vermelho", cue: "anatolia", seta: true },
      { pontos: [[37.0, 37.4], [33.5, 36.3], [30.3, 32.4]], cor: "vermelho", cue: "suez", seta: true }]} />
);

// 3. la carta de Hitler (p07)
export const H03Carta: React.FC<SceneProps> = (p) => (
  <DadoAC {...p} titulo="La carta de Hitler a İnönü" periodo="4 de marzo de 1941" numero="20 millas · 32 km"
    texto="Lejos de la frontera turca" cueNumero="papen" />
);

// 4. junio de 1941 (p11)
export const H04Junio: React.FC<SceneProps> = (p) => (
  <LinhaDoTempoAC {...p} etiqueta="JUNIO DE 1941"
    marcos={[{ data: "18 DE JUNIO DE 1941", texto: "Tratado de Amistad germano-turco", cue: "18" },
      { data: "22 DE JUNIO DE 1941", texto: "Más de tres millones de soldados del Eje invaden la URSS", cue: "22" }]} />
);

// 5. la Directiva 32 (p13)
export const H05Directiva: React.FC<SceneProps> = (p) => (
  <CitacaoAC {...p} cueDestaque="presion"
    linhas={["Directiva n.º 32 · 11 de junio de 1941", "Una operación desde Bulgaria, a través de Turquía,",
      "contra la posición británica en el canal de Suez…"]}
    destaque="una fuerte presión sobre Turquía" />
);

// 6. el acuerdo Clodius (p19)
export const H06Clodius: React.FC<SceneProps> = (p) => (
  <BarrasAC {...p} titulo="El acuerdo Clodius" subtitulo="Cromita turca prometida a Alemania"
    barras={[{ valor: 45, rotulo: "1941-1942", texto: "45.000 t", cue: "45" },
      { valor: 90, rotulo: "1943", texto: "90.000 t al año", cue: "90" },
      { valor: 90, rotulo: "1944", texto: "90.000 t al año", cue: "1944", destaque: true }]} />
);

// 7. el memorando de Speer (p24)
export const H07Speer: React.FC<SceneProps> = (p) => (
  <DadoAC {...p} titulo="Memorando de Albert Speer" periodo="10 de noviembre de 1943" numero="5,6 meses"
    texto="de cromo sin Turquía" cueNumero="speer" />
);

// 8. la puerta de entrada (p29)
export const H08Puerta: React.FC<SceneProps> = (p) => (
  <MapaPergaminho {...p} titulo="La puerta de entrada" ano="1941" terras={TERRAS}
    enquadra={[[42.4, 25.4], [39.7, 30.2]]}
    lugares={[{ nome: "Tracia", lat: 41.75, lon: 27.4, ponto: false, grande: true, cue: "tracia" },
      { nome: "Edirne", lat: 41.68, lon: 26.56 },
      { nome: "Estambul", lat: 41.01, lon: 28.97, cue: "estambul" },
      { nome: "Bósforo", lat: 41.15, lon: 29.07, cue: "bosforo", circulo: true },
      { nome: "Dardanelos", lat: 40.15, lon: 26.4, cue: "dardanelos", circulo: true }]}
    rotas={[{ pontos: [[41.1, 25.9], [41.68, 26.56], [41.25, 27.9], [41.01, 28.85]], cor: "vermelho", cue: "tracia", seta: true }]} />
);

// 9. el censo de 1940 (p33)
export const H09Censo: React.FC<SceneProps> = (p) => (
  <DadoAC {...p} titulo="Censo de Turquía" periodo="20 de octubre de 1940" numero="17.820.950"
    texto="habitantes · más de un millón movilizados" cueNumero="17" />
);

// 10. el juego a tres bandas (p46)
export const H10TresBandas: React.FC<SceneProps> = (p) => (
  <Polaroids {...p} etiqueta="EL JUEGO A TRES BANDAS"
    fotos={[{ src: "stock/ac_ht_hitler.jpg", legenda: "Hitler · amistad y cromo", cue: "hitler" },
      { src: "stock/ac_ht_churchill.jpg", legenda: "Churchill · una alianza en el papel", cue: "churchill" },
      { src: "stock/ac_ht_stalin.jpg", legenda: "Stalin · lo mínimo", cue: "stalin" }]} />
);

// 11. Teherán (p49)
export const H11Teheran: React.FC<SceneProps> = (p) => (
  <Polaroids {...p} etiqueta="TEHERÁN · 1943"
    fotos={[{ src: "stock/ac_ht_stalin2.jpg", legenda: "Stalin · Teherán 1943", cue: "stalin" },
      { src: "stock/ac_ht_roosevelt.jpg", legenda: "Roosevelt · Teherán 1943", cue: "roosevelt" },
      { src: "stock/ac_ht_churchill2.jpg", legenda: "Churchill · Teherán 1943", cue: "churchill" }]} />
);

// 12. lo que pedía Moscú (p61)
export const H12Moscu: React.FC<SceneProps> = (p) => (
  <MapaPergaminho {...p} titulo="Lo que pedía Moscú" ano="1945" terras={TERRAS}
    enquadra={[[44.0, 26.0], [37.0, 45.5]]}
    lugares={[{ nome: "Turquía", lat: 39.0, lon: 34.0, ponto: false, grande: true },
      { nome: "Unión Soviética", lat: 43.2, lon: 43.5, ponto: false, cue: "molotov" },
      { nome: "Kars", lat: 40.6, lon: 43.1, cue: "kars", circulo: true },
      { nome: "Ardahan", lat: 41.11, lon: 42.7, cue: "ardahan", circulo: true },
      { nome: "Los estrechos", lat: 41.05, lon: 29.0, cue: "estrechos", circulo: true }]} />
);
