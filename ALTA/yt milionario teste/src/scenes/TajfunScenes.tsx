// As 9 animações de "Tajfun — największy okręt podwodny w historii" (pl, padrão). Pedido do painel (automático, baia 1).
// REGRA (25/09 + 26/09/2026): biblioteca + MAPA — MapaCampanha, Painel, Odometro, Barras, Colunas, Lista.
// Todo número é DITO na narração; cues na grafia do Whisper ("8300", "-650." -> "650", "2 ,5" -> "2").
// Polonês: milhar com espaço inquebrável (sep " ").
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Barras, Colunas, Lista } from "./blocos";
import { Odometro } from "./biblioteca";
import { MapaCampanha } from "./arquivo2";
import { SceneProps } from "./shared";

// Península de Kola e Mar Branco simplificados (lat, lon)
const KOLA: [number, number][] = [
  [70.4, 25.5], [70.1, 28.0], [69.8, 30.8], [69.4, 33.0], [69.2, 35.5], [68.6, 38.5], [68.2, 40.5], [67.0, 41.3],
  [66.2, 40.0], [66.4, 37.0], [66.8, 34.5], [66.5, 33.0], [65.0, 34.8], [64.5, 36.5], [64.6, 39.8], [65.2, 40.5],
  [66.0, 42.5], [66.5, 44.0],
];

// ---------------- 1. R-39 x Trident (p03) ----------------
export const T01Rakieta: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="ER-39 · 16 METRÓW DŁUGOŚCI"
    titulo="Masa rakiety z systemem startowym"
    tint={colors.danger}
    max={100}
    barras={[
      { rotulo: "Radziecka R-39", valor: "ok. 90 ton", v: 90, cue: "90", cor: colors.danger },
      { rotulo: "Amerykański Trident I", valor: "ok. 33 tony", v: 33, cue: "33", cor: colors.cool },
    ]}
    nota={{ texto: "niemal trzy razy cięższa", cue: "trzy" }}
  />
);

// ---------------- 2. as medidas (p05) ----------------
export const T02Wymiary: React.FC<SceneProps> = (p) => (
  <Painel
    {...p}
    spec={{
      kicker: "Projekt 941 · Tajfun",
      titulo: "Olbrzym w liczbach",
      linhas: [
        { rotulo: "Długość", valor: "ok. 175 metrów", cue: "175", destaque: true },
        { rotulo: "Szerokość kadłuba", valor: "ok. 23 metry", cue: "23" },
        { rotulo: "Zanurzenie na powierzchni", valor: "ok. 12 metrów", cue: "12" },
      ],
      tint: "cool",
    }}
  />
);

// ---------------- 3. a deslocação x Ohio (p06) ----------------
export const T03Wypornosc: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="WYPORNOŚĆ · TYSIĄCE TON"
    titulo="Najcięższy okręt podwodny w historii"
    tint={colors.accent}
    max={50}
    barras={[
      { rotulo: "Tajfun na powierzchni", valor: "23–24 tys. ton", v: 24, cue: "23", cor: colors.cool },
      { rotulo: "Tajfun w zanurzeniu", valor: "ok. 48 tys. ton", v: 48, cue: "48", cor: colors.danger },
      { rotulo: "Ohio w zanurzeniu", valor: "niecałe 19 tys. ton", v: 19, cue: "19" },
    ]}
  />
);

// ---------------- 4. os cascos de pressão (p11) ----------------
export const T04Kadluby: React.FC<SceneProps> = (p) => (
  <Colunas
    {...p}
    kicker="KADŁUBY CIŚNIENIOWE · MIĘDZY DWOMA GŁÓWNYMI"
    tint={colors.cool}
    cols={[
      { titulo: "Trzeci", texto: "z przodu: przedział torpedowy", cue: "trzeci", cor: colors.cool },
      { titulo: "Czwarty", texto: "pod kioskiem: centrum dowodzenia", cue: "czwart", cor: colors.accent },
      { titulo: "Piąty", texto: "na rufie: mechanizmy sterów", cue: "piat", cor: colors.danger },
    ]}
  />
);

// ---------------- 5. o alcance (p16) ----------------
export const T05Zasieg: React.FC<SceneProps> = (p) => (
  <Odometro
    {...p}
    kicker="ZASIĘG POCISKU ER-39"
    valor={8300}
    sep={" "}
    cue="8300"
    sufixo=" km"
    nota={{ texto: "jeden Tajfun: nawet 200 głowic jądrowych", cue: "200" }}
  />
);

// ---------------- 6. os reatores (p20) ----------------
export const T06Reaktory: React.FC<SceneProps> = (p) => (
  <Painel
    {...p}
    spec={{
      kicker: "Serce maszyny",
      titulo: "Dwa reaktory jądrowe",
      linhas: [
        { rotulo: "Typ reaktora", valor: "OK-650", cue: "650" },
        { rotulo: "Moc cieplna każdego", valor: "ok. 190 MW", cue: "190", destaque: true },
        { rotulo: "Obieg pierwotny", valor: "znacznie ponad 100 °C", cue: "100" },
      ],
      tint: "accent",
    }}
  />
);

// ---------------- 7. atravessar o gelo (p27) ----------------
export const T07Lod: React.FC<SceneProps> = (p) => (
  <Lista
    {...p}
    kicker="WYNURZENIE POD LODEM"
    titulo="Procedura"
    tint={colors.cool}
    itens={[
      { titulo: "Sonar szuka najcieńszego lodu", cue: "najciensz" },
      { titulo: "Okręt unosi się niemal pionowo", cue: "pionowo" },
      { titulo: "Załoga wydmuchuje balast", cue: "wydmuch" },
      { titulo: "Lód do ok. 2,5 metra — przebity", cue: "2", cor: colors.danger },
    ]}
  />
);

// ---------------- 8. a tripulação (p31) ----------------
export const T08Zaloga: React.FC<SceneProps> = (p) => (
  <Painel
    {...p}
    spec={{
      kicker: "Życie na pokładzie",
      titulo: "Miesiące bez słońca",
      linhas: [
        { rotulo: "Załoga", valor: "ok. 160 ludzi", cue: "160" },
        { rotulo: "Oficerowie i chorążowie", valor: "mniej więcej jedna trzecia", cue: "jedna" },
        { rotulo: "Autonomia", valor: "ok. 120 dni", cue: "120", destaque: true },
        { rotulo: "Bez słońca i rodziny", valor: "4 miesiące", cue: "4" },
      ],
      tint: "cool",
    }}
  />
);

// ---------------- 9. MAPA: Siewierodwińsk -> Zapadnaja Lica (p38) ----------------
export const T09Baza: React.FC<SceneProps> = (p) => (
  <MapaCampanha
    {...p}
    kicker="SZEŚĆ TAJFUNÓW · OSTATNI W SŁUŻBIE OD 1989"
    pontos={[
      { nome: "Siewierodwińsk", lat: 64.56, lon: 39.83, data: "STOCZNIA SIEWMASZ", cue: "piec" },
      { nome: "Zapadnaja Lica", lat: 69.42, lon: 32.45, data: "BAZA TAJFUNÓW", cue: "zapadnaja", lado: "esq" },
      { nome: "Norwegia", lat: 69.9, lon: 28.4, data: "GRANICA", cue: "norweg", lado: "esq" },
    ]}
    setas={[{ de: 0, para: 1, cue: "zapadnaja", cor: "#b3161b" }]}
    costa={[KOLA]}
  />
);
