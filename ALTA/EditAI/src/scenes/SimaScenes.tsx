// Animações de "Hallaron 28 humanos en un pozo de 430.000 años" (es) — painel 20261014-135858 (baia 1, modo enxuto).
// REGRA: biblioteca + MAPA; motion curto (cues <= 12 s); todo número é dito; milhar com ponto (es).
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { LinhaDoTempo, Barras } from "./blocos";
import { MapaRota, Documento } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. MAPA: Sierra de Atapuerca -> Burgos (p01)
export const S01Atapuerca: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="SIERRA DE ATAPUERCA · BURGOS · ESPAÑA" lugares={[
    { nome: "Sierra de Atapuerca", lat: 42.352, lon: -3.519, cue: "atapuerca", esquerda: true },
    { nome: "Burgos", lat: 42.344, lon: -3.697, cue: "burgos", abaixo: true },
  ]} tint={colors.accent} />
);

// 2. a sima em números (p03)
export const S02Sima: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Sima de los Huesos · Cueva Mayor", titulo: "Una trampa de piedra", linhas: [
    { rotulo: "Caída libre del pozo", valor: `13${NB}m`, cue: "18" },
    { rotulo: "Largo de la cámara", valor: `unos 18${NB}m`, cue: "18" },
    { rotulo: "Bajo la superficie", valor: `unos 30${NB}m`, cue: "30", destaque: true },
  ], tint: "accent" }} />
);

// 3. o que a sima entregou (p10)
export const S03Restos: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Sima de los Huesos · hasta hoy", titulo: "Lo que salió del barro", linhas: [
    { rotulo: "Restos humanos", valor: `cerca de 7.000`, cue: "reconstruido" },
    { rotulo: "Cráneos reconstruidos", valor: "17", cue: "17" },
    { rotulo: "Individuos", valor: "al menos 28", cue: "28", destaque: true },
  ], tint: "accent" }} />
);

// 4. as datas que dançaram (p18)
export const S04Fechas: React.FC<SceneProps> = (p) => (
  <LinhaDoTempo {...p} kicker="¿Cuándo cayeron al pozo?" tint={colors.accent} marcos={[
    { ano: "Años 90", texto: `uranio y torio: 350.000${NB}años`, cue: "350" },
    { ano: "2007", texto: `más de 530.000${NB}años`, cue: "530" },
    { ano: "Otros", texto: `600.000 o 300.000${NB}años`, cue: "600", cor: colors.accent },
  ]} />
);

// 5. escala: sima x Homo sapiens x pirâmides (p20)
export const S05Escala: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="Años de antigüedad" titulo="Antes de nosotros" tint={colors.accent} max={430000} barras={[
    { rotulo: "Sima de los Huesos", valor: "430.000", v: 430000, cue: "300", cor: colors.accent },
    { rotulo: "Homo sapiens en África", valor: "300.000", v: 300000, cue: "300" },
    { rotulo: "Pirámides de Egipto", valor: "4.500", v: 4500, cue: "pirámides" },
  ]} />
);

// 6. Elvis, o ancião (p33)
export const S06Elvis: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Pelvis 1 · «Elvis»", titulo: "Un anciano de la sima", linhas: [
    { rotulo: "Edad al morir", valor: `más de 45${NB}años`, cue: "45", destaque: true },
    { rotulo: "Casi nadie pasaba de", valor: `30${NB}años`, cue: "30" },
  ], tint: "accent" }} />
);

// 7. o crime do Crânio 17 (p53)
export const S07Crimen: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="prueba" chave={5} linhas={[
    "SALA ET AL. · 2015 · CRÁNEO 17",
    "",
    "1. Fracturas en el momento de la muerte",
    "2. Dos golpes con el mismo objeto",
    "3. Dos ángulos: un atacante cara a cara",
    "Conclusión: alguien quería que muriera",
  ]} carimbo={{ texto: "HOMICIDIO", cue: "homicidio" }} />
);

// 8. Excalibur (p61)
export const S08Excalibur: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Sima de los Huesos · 1998", titulo: "Excalibur", linhas: [
    { rotulo: "Herramientas en la sima", valor: "una sola", cue: "bifaz" },
    { rotulo: "Largo", valor: `unos 15${NB}cm`, cue: "15" },
    { rotulo: "Peso", valor: `casi 700${NB}g`, cue: "700" },
    { rotulo: "Piedra", valor: "cuarcita rojiza", cue: "cuars", destaque: true },
  ], tint: "accent" }} />
);

// 9. MAPA: Burgos -> Leipzig (p75)
export const S09Leipzig: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="DE LA SIMA AL LABORATORIO" lugares={[
    { nome: "Sima de los Huesos · Burgos", lat: 42.35, lon: -3.52, cue: "pasó", abaixo: true },
    { nome: "Max Planck · Leipzig", lat: 51.34, lon: 12.37, cue: "leipzig", esquerda: true },
  ]} tint={colors.accent} />
);

// 10. MAPA: Denisova -> Espanha (p82)
export const S10Denisova: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="DENISOVANOS · DESCUBIERTOS EN 2010" lugares={[
    { nome: "Cueva de Denisova · Altái", lat: 51.40, lon: 84.68, cue: "denisova", esquerda: true },
    { nome: "Sima de los Huesos · España", lat: 42.35, lon: -3.52, cue: "españa", abaixo: true },
  ]} tint={colors.accent} />
);

// 11. a resposta do ADN nuclear (p91)
export const S11Nuclear: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Nature · marzo de 2016", titulo: "¿Quiénes eran?", linhas: [
    { rotulo: "ADN mitocondrial · 2013", valor: "¿denisovanos?", cue: "denisovanos" },
    { rotulo: "ADN nuclear · 2016", valor: "neandertales", cue: "neandertales", destaque: true },
    { rotulo: "La rama", valor: "neandertales primitivos", cue: "primitivos" },
  ], tint: "accent" }} />
);
