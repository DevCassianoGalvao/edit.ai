// Animacje filmu "Icon of the Seas — pływające miasto" (pl, arquivo dark) — painel 20261004-153813 (baia 1).
// REGRA (25/09 + 03/10/2026): biblioteca + MAPA; motion CURTO (cues ditos em <= ~12 s); todo número é dito.
// Polonês: espaço duro (NB) depois de palavra de uma letra (w, z, i, o, a) e entre número e unidade.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Odometro, MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. MAPA: stocznia w Turku, kilkaset km od polskiego wybrzeża (p05)
export const C01Turku: React.FC<SceneProps> = (p) => (
  <MapaRota
    {...p}
    kicker="STOCZNIA MEYER TURKU · FINLANDIA"
    lugares={[
      { nome: "Turku", lat: 60.45, lon: 22.27, cue: "turku" },
      { nome: `Polskie wybrzeże`, lat: 54.52, lon: 18.53, cue: "polskiego", abaixo: true },
    ]}
    tint={colors.accent}
  />
);

// 2. dzień zmiany pasażerów (p10)
export const C02Zmiana: React.FC<SceneProps> = (p) => (
  <Odometro
    {...p}
    kicker="DZIEŃ ZMIANY PASAŻERÓW"
    valor={7500}
    cue="7"
    sep=" "
    prefixo={`prawie${NB}`}
    sufixo={`${NB}osób schodzi`}
    nota={{ texto: `od rana do${NB}wczesnego popołudnia`, cue: "popo" }}
  />
);

// 3. Chill Island (p16)
export const C03Baseny: React.FC<SceneProps> = (p) => (
  <Painel
    {...p}
    spec={{
      kicker: "Chill Island · Wyspa Relaksu",
      titulo: "Woda na całym statku",
      linhas: [
        { rotulo: "Baseny", valor: "7", cue: "7", destaque: true },
        { rotulo: "Jacuzzi", valor: "9", cue: "9" },
      ],
      tint: "accent",
    }}
  />
);

// 4. ponad 40 miejsc z jedzeniem (p22)
export const C04Restauracje: React.FC<SceneProps> = (p) => (
  <Odometro
    {...p}
    kicker="MIASTO, KTÓRE PRZYPADKIEM PŁYWA"
    valor={40}
    cue="40"
    prefixo={`ponad${NB}`}
    sufixo={`${NB}miejsc`}
    nota={{ texto: `gdzie można coś zjeść lub wypić`, cue: "zjesc" }}
  />
);

// 5. praca załogi (p31)
export const C05Zaloga: React.FC<SceneProps> = (p) => (
  <Painel
    {...p}
    spec={{
      kicker: "Kontrakty załogi",
      titulo: "Bez wolnego dnia",
      linhas: [
        { rotulo: "Godziny pracy dziennie", valor: `10–11`, cue: "10", destaque: true },
        { rotulo: "Dni w${NB}tygodniu", valor: "7", cue: "siedem" },
      ],
      tint: "accent",
    }}
  />
);

// 6. pędniki (p47)
export const C06Pedniki: React.FC<SceneProps> = (p) => (
  <Painel
    {...p}
    spec={{
      kicker: "Napęd elektryczny",
      titulo: "Obrotowe gondole pod rufą",
      linhas: [
        { rotulo: "Pędniki", valor: "3", cue: "trzy" },
        { rotulo: "Obrót", valor: "360°", cue: "360", destaque: true },
        { rotulo: "Moc każdego", valor: `ok.${NB}20${NB}MW`, cue: "20" },
      ],
      tint: "accent",
    }}
  />
);

// 7. koszt (p73)
export const C07Koszt: React.FC<SceneProps> = (p) => (
  <Odometro
    {...p}
    kicker="BUDOWA JEDNEGO STATKU KLASY ICON"
    valor={2}
    cue="2"
    prefixo={`około${NB}`}
    sufixo={`${NB}mld dolarów`}
    nota={{ texto: `jedna z${NB}najdroższych konstrukcji cywilnych`, cue: "najdrozsz" }}
  />
);
