// Peças de "La verdadera razón por la que Londres y París no declararon la guerra a Stalin en 1939" (es) — painel 20261104-144653 (baia b1).
// ESTILO ARQUIVO COLORIZADO: só peças de src/scenes/arquivo_colorizado.tsx; todo número é dito; milhar com ponto (es).
import React from "react";
import { BarrasAC, CitacaoAC, DadoAC, LinhaDoTempoAC, MapaPergaminho, Polaroids } from "./arquivo_colorizado";
import { SceneProps } from "./shared";
import { TERRAS_LP } from "./LondresGeo";

const TERRAS = TERRAS_LP;   // Natural Earth 50m (src/scenes/LondresGeo.ts)

// linhas aproximadas (lat, lon)
const CURZON: [number, number][] = [[55.25, 23.0], [54.4, 23.45], [53.68, 23.83], [52.9, 23.9], [52.1, 23.65], [51.4, 23.65],
  [50.75, 24.05], [50.3, 23.9], [49.78, 22.77], [49.15, 22.65]];
const RIGA: [number, number][] = [[55.85, 27.3], [55.3, 27.6], [54.6, 27.0], [53.95, 27.1], [53.2, 26.9], [52.5, 27.4],
  [51.75, 27.6], [51.2, 26.9], [50.6, 26.6], [49.95, 26.05], [49.2, 26.25], [48.5, 26.2]];
const LINHA_AGO: [number, number][] = [[53.6, 21.9], [53.1, 21.6], [52.55, 21.05], [52.25, 21.02], [51.6, 21.5],
  [51.0, 21.75], [50.65, 21.85], [50.25, 22.2], [49.78, 22.77], [49.5, 22.25], [49.15, 22.4]];
const LINHA_SET: [number, number][] = [[54.3, 22.8], [53.6, 23.0], [52.95, 22.9], [52.6, 22.6], [52.1, 23.65], [51.5, 23.6],
  [50.85, 24.0], [50.4, 23.6], [50.2, 23.1], [49.78, 22.77], [49.15, 22.6]];
const ODER: [number, number][] = [[54.1, 14.25], [53.4, 14.55], [52.6, 14.6], [51.95, 14.7], [51.3, 15.0], [50.95, 14.85]];

// 1. dos ejércitos (p03)
export const L01DosEjercitos: React.FC<SceneProps> = (p) => (
  <MapaPergaminho {...p} titulo="Dos ejércitos" ano="1939" terras={TERRAS}
    enquadra={[[56.0, 12.0], [47.5, 33.0]]}
    lugares={[{ nome: "Polonia", lat: 51.2, lon: 18.6, ponto: false, grande: true, cue: "mapa" },
      { nome: "Alemania", lat: 51.2, lon: 13.6, ponto: false }, { nome: "Unión Soviética", lat: 53.6, lon: 30.2, ponto: false },
      { nome: "Varsovia", lat: 52.23, lon: 21.01 }]}
    rotas={[{ pontos: [[52.5, 14.2], [52.4, 17.0], [52.25, 20.6]], cor: "azul", cue: "alemana", seta: true },
      { pontos: [[53.9, 28.6], [53.1, 26.2], [52.4, 24.0]], cor: "vermelho", cue: "soviética", seta: true }]} />
);

// 2. la Línea Curzon y la Paz de Riga (p07)
export const L02Curzon: React.FC<SceneProps> = (p) => (
  <MapaPergaminho {...p} titulo="La Línea Curzon" ano="1920 · 1921" terras={TERRAS}
    enquadra={[[56.3, 17.0], [48.2, 31.5]]}
    lugares={[{ nome: "Varsovia", lat: 52.23, lon: 21.01 },
      { nome: "Vilna", lat: 54.69, lon: 25.28, cue: "vilna", circulo: true },
      { nome: "Leópolis", lat: 49.84, lon: 24.03, cue: "leópolis", circulo: true },
      { nome: "Pinsk", lat: 52.11, lon: 26.10, cue: "pinsk", circulo: true }]}
    rotas={[{ pontos: RIGA, cor: "vermelho", cue: "riga" }, { pontos: CURZON, cor: "azul", cue: "curs" }]} />
);

// 3. la misión militar (p13)
export const L03Mision: React.FC<SceneProps> = (p) => (
  <Polaroids {...p} etiqueta="MOSCÚ · AGOSTO DE 1939"
    fotos={[{ src: "stock/ac_lp_moscu.jpg", legenda: "Moscú · años treinta", cue: "drax" },
      { src: "stock/ac_lp_voroshilov.jpg", legenda: "Mariscal Kliment Voroshílov", cue: "voroshilov" }]} />
);

// 4. el protocolo secreto (p16)
export const L04Protocolo: React.FC<SceneProps> = (p) => (
  <MapaPergaminho {...p} titulo="El protocolo secreto" ano="23 de agosto de 1939" terras={TERRAS}
    enquadra={[[61.0, 14.0], [48.5, 31.5]]}
    lugares={[{ nome: "Finlandia", lat: 61.4, lon: 25.5, ponto: false, cue: "finlandia" },
      { nome: "Estonia", lat: 58.7, lon: 25.8, ponto: false }, { nome: "Letonia", lat: 56.9, lon: 25.6, ponto: false },
      { nome: "Varsovia", lat: 52.23, lon: 21.01 },
      { nome: "Para Stalin", lat: 51.6, lon: 26.8, ponto: false, grande: true, cue: "oriental" },
      { nome: "Para Hitler", lat: 51.6, lon: 17.0, ponto: false, grande: true, cue: "occidental" }]}
    rotas={[{ pontos: LINHA_AGO, cor: "vermelho", cue: "narew" }]} />
);

// 5. la cláusula del protocolo (p18)
export const L05Clausula: React.FC<SceneProps> = (p) => (
  <CitacaoAC {...p} cueDestaque="alemania"
    linhas={["Protocolo secreto · Londres, 25 de agosto de 1939", "Primera cláusula: por «una potencia europea»…"]}
    destaque="había que entender Alemania" />
);

// 6. septiembre de 1939 (p22)
export const L06Septiembre: React.FC<SceneProps> = (p) => (
  <LinhaDoTempoAC {...p} etiqueta="SEPTIEMBRE DE 1939"
    marcos={[{ data: "1 DE SEPTIEMBRE", texto: "Alemania invade Polonia", cue: "invade" },
      { data: "3 DE SEPTIEMBRE · 11 DE LA MAÑANA", texto: "Gran Bretaña declara la guerra a Alemania", cue: "11" },
      { data: "3 DE SEPTIEMBRE · 5 DE LA TARDE", texto: "Francia declara la guerra a Alemania", cue: "5" }]} />
);

// 7. Brest-Litovsk (p31)
export const L07Brest: React.FC<SceneProps> = (p) => (
  <Polaroids {...p} etiqueta="BREST-LITOVSK · 22 DE SEPTIEMBRE DE 1939"
    fotos={[{ src: "stock/ac_lp_brest1.jpg", legenda: "Guderian y Krivoshéin", cue: "guderian" },
      { src: "stock/ac_lp_brest2.jpg", legenda: "La tribuna · Brest, 1939", cue: "tribuna" },
      { src: "stock/ac_lp_brest3.jpg", legenda: "Soldados alemanes y soviéticos", cue: "bandera" }]} />
);

// 8. el acertijo de Churchill (p34)
export const L08Acertijo: React.FC<SceneProps> = (p) => (
  <CitacaoAC {...p} cueDestaque="acertijo"
    linhas={["Winston Churchill · radio, 1 de octubre de 1939", "No puedo predecir la acción de Rusia."]}
    destaque="Un acertijo envuelto en un misterio dentro de un enigma" />
);

// 9. la frontera de 1939 sobre la Línea Curzon (p37)
export const L09Frontera: React.FC<SceneProps> = (p) => (
  <MapaPergaminho {...p} titulo="La frontera de 1939" ano="26 de octubre de 1939" terras={TERRAS}
    enquadra={[[56.0, 16.0], [48.3, 31.0]]}
    lugares={[{ nome: "Varsovia", lat: 52.23, lon: 21.01 }, { nome: "Brest", lat: 52.09, lon: 23.69 },
      { nome: "Alemania", lat: 51.5, lon: 18.4, ponto: false }, { nome: "Unión Soviética", lat: 52.6, lon: 27.6, ponto: false }]}
    rotas={[{ pontos: LINHA_SET, cor: "vermelho", cue: "frontera" }, { pontos: CURZON, cor: "azul", cue: "curs" }]} />
);

// 10. la Sociedad de Naciones (p47)
export const L10Sociedad: React.FC<SceneProps> = (p) => (
  <DadoAC {...p} titulo="La Guerra de Invierno" periodo="Sociedad de Naciones" numero="14 de diciembre de 1939"
    texto="La Unión Soviética, declarada agresora y expulsada" cueNumero="14" />
);

// 11. Narvik y las minas suecas (p49)
export const L11Narvik: React.FC<SceneProps> = (p) => (
  <MapaPergaminho {...p} titulo="El camino de Narvik" ano="1940" terras={TERRAS}
    enquadra={[[70.0, 12.0], [61.0, 31.0]]}
    lugares={[{ nome: "Narvik", lat: 68.44, lon: 17.43, cue: "narvik", circulo: true },
      { nome: "Finlandia", lat: 63.3, lon: 26.8, ponto: false, grande: true, cue: "finlandia" },
      { nome: "Gällivare", lat: 67.13, lon: 20.66, cue: "galib" }, { nome: "Kiruna", lat: 67.86, lon: 20.23, cue: "kiruna" },
      { nome: "Suecia", lat: 63.8, lon: 15.8, ponto: false }, { nome: "Noruega", lat: 61.8, lon: 9.5, ponto: false }]}
    rotas={[{ pontos: [[68.44, 17.43], [67.86, 20.23], [67.13, 20.66], [65.85, 22.4], [65.85, 24.15], [65.0, 26.5]],
      cor: "azul", cue: "narvik", seta: true }]} />
);

// 12. el Cáucaso y las bases (p54)
export const L12Caucaso: React.FC<SceneProps> = (p) => (
  <MapaPergaminho {...p} titulo="El petróleo del Cáucaso" ano="1940" terras={TERRAS}
    enquadra={[[46.0, 33.0], [31.0, 55.0]]}
    lugares={[{ nome: "Bakú", lat: 40.41, lon: 49.87, circulo: true }, { nome: "Grozni", lat: 43.32, lon: 45.69 },
      { nome: "Batumi", lat: 41.64, lon: 41.64 },
      { nome: "Siria", lat: 35.2, lon: 38.6, ponto: false, cue: "siria" }, { nome: "Irak", lat: 33.0, lon: 43.6, ponto: false, cue: "irak" },
      { nome: "Irán", lat: 33.0, lon: 52.5, ponto: false, cue: "irán" }, { nome: "Turquía", lat: 39.0, lon: 35.0, ponto: false, cue: "turquía" }]}
    rotas={[{ pontos: [[33.4, 43.6], [36.8, 46.5], [40.2, 49.5]], cor: "vermelho", cue: "bombas", seta: true },
      { pontos: [[35.5, 38.8], [39.0, 42.0], [43.0, 45.4]], cor: "vermelho", cue: "bombas", seta: true }]} />
);

// 13. los bombarderos (p56)
export const L13Bombarderos: React.FC<SceneProps> = (p) => (
  <BarrasAC {...p} titulo="Bombarderos para el Cáucaso" subtitulo="Primavera de 1940"
    barras={[{ valor: 48, rotulo: "Blenheim · RAF", texto: "48", cue: "48" },
      { valor: 65, rotulo: "Martin Maryland · Francia", texto: "65", cue: "65", destaque: true },
      { valor: 24, rotulo: "Farman · Francia", texto: "24", cue: "24" }]} />
);

// 14. la frontera de la posguerra (p61)
export const L14Posguerra: React.FC<SceneProps> = (p) => (
  <MapaPergaminho {...p} titulo="Polonia, movida en el mapa" ano="1945" terras={TERRAS}
    enquadra={[[56.0, 11.5], [48.3, 31.0]]}
    lugares={[{ nome: "Polonia", lat: 52.2, lon: 19.2, ponto: false, grande: true, cue: "oriental" },
      { nome: "Tierras alemanas", lat: 53.0, lon: 15.9, ponto: false, cue: "alemanas" },
      { nome: "Unión Soviética", lat: 53.0, lon: 27.8, ponto: false }]}
    rotas={[{ pontos: CURZON, cor: "azul", cue: "curs" }, { pontos: ODER, cor: "vermelho", cue: "alemanas" }]} />
);

// 15. la decisión revisada (p65)
export const L15Revision: React.FC<SceneProps> = (p) => (
  <LinhaDoTempoAC {...p} etiqueta="UNA DECISIÓN REVISADA"
    marcos={[{ data: "DICIEMBRE DE 1939", texto: "Expulsión de la Sociedad de Naciones", cue: "diciembre" },
      { data: "FEBRERO DE 1940", texto: "El plan de Narvik", cue: "febrero" },
      { data: "MARZO DE 1940", texto: "El vuelo sobre Bakú", cue: "marzo" }]} />
);
