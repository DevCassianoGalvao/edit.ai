// As 12 animações de "The People Who Still Work Inside Chernobyl" (en, 44 min). 20 % vídeo / 80 % foto.
// REGRA (25/09/2026): animação em JavaScript pela BIBLIOTECA — Odometro, Barras (2), Colunas (2), Lista, Documento (2),
// MapaRota (2), LinhaDoTempo, Painel. Todo número é DITO na narração; cues em scripts/build_plan.py -> CUES
// (na grafia do Whisper: "3 ,000", "cesium", "Slavutich", "Semikoti").
import React from "react";
import { colors } from "../design/tokens";
import { Painel, PainelSpec } from "./Painel";
import { Barras, Colunas, LinhaDoTempo, Lista } from "./blocos";
import { Documento, MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const painel = (spec: PainelSpec): React.FC<SceneProps> => {
  const C: React.FC<SceneProps> = (p) => <Painel {...p} spec={spec} />;
  return C;
};

// ---------------- 1. quantos ainda vão ----------------
export const A01Pessoas: React.FC<SceneProps> = (p) => (
  <Odometro
    {...p}
    kicker="PEOPLE WORKING INSIDE THE ZONE · ANY ROTATION"
    valor={3000}
    cue="hovers"
    prefixo="~"
    nota={{ texto: "Engineers, electricians, chemists, dosimetrists, firefighters, police, cooks, rangers, biologists.", cue: "engineers" }}
  />
);

// ---------------- 2. o que sobrou da explosão ----------------
export const A02Isotopos: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="Half-life of what the explosion released"
    titulo="What remains after forty years"
    tint={colors.danger}
    max={100}
    barras={[
      { rotulo: "Iodine-131", valor: "decayed within weeks", v: 2, cue: "iodine", cor: colors.textDim },
      { rotulo: "Caesium-137", valor: "about 30 years", v: 30, cue: "cesium", cor: colors.accent },
      { rotulo: "Strontium-90", valor: "about 30 years", v: 30, cue: "strontium", cor: colors.accent },
      { rotulo: "Plutonium and americium", valor: "thousands of years", v: 100, cue: "plutonium", cor: colors.danger },
    ]}
    nota={{ texto: "A day in much of the zone today: less exposure than a long-haul flight.", cue: "flight" }}
  />
);

// ---------------- 3. tempo controlado ----------------
export const A03Rotacao: React.FC<SceneProps> = (p) => (
  <Colunas
    {...p}
    kicker="Controlled time — how the shifts work"
    tint={colors.cool}
    cols={[
      { titulo: "15 / 15", texto: "15 days inside the zone, 15 days outside.", cue: "famous", cor: colors.accent },
      { titulo: "4 on, 3 off", texto: "Commuting daily, or other patterns set by the dose rate.", cue: "others" },
      { titulo: "Daytime shifts", texto: "At the plant: home every evening.", cue: "daytime" },
    ]}
  />
);

// ---------------- 4. a dose ----------------
export const A04Dose: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="Annual radiation dose, in millisieverts"
    titulo="Every worker has a limit"
    tint={colors.cool}
    max={20}
    barras={[
      { rotulo: "Legal limit, nuclear industry personnel", valor: "20 mSv", v: 20, cue: "annual", cor: colors.danger },
      { rotulo: "Natural background, anywhere on Earth", valor: "2 to 3 mSv", v: 3, cue: "comparison", cor: colors.textDim },
      { rotulo: "Many zone workers today", valor: "only a few mSv", v: 4, cue: "few", cor: colors.cool },
    ]}
    nota={{ texto: "Enforced — it decides which road a crew takes and how long a welder stays.", cue: "enforced" }}
  />
);

// ---------------- 5. a travessia ----------------
export const A05Travessia: React.FC<SceneProps> = (p) => (
  <Lista
    {...p}
    kicker="Leaving the zone"
    titulo="The ritual of crossing"
    tint={colors.accent}
    itens={[
      { titulo: "Vehicles", texto: "Sensors scan the tires and the chassis.", cue: "vehicles" },
      { titulo: "Portal monitors", texto: "Hands and feet on the sensor plates.", cue: "portal" },
      { titulo: "Green light: pass. Red light: contaminated.", texto: "Clothes or shoes may never leave the zone.", cue: "green", cor: colors.danger },
      { titulo: "Sanitary checkpoint", texto: "Personal clothes off, uniform on — shower and change back at the end.", cue: "sanitary" },
    ]}
    nota={{ texto: "The line between clean and dirty is a corridor with a painted floor.", cue: "corridor" }}
  />
);

// ---------------- 6. os oito quarteirões ----------------
export const A06Quarteiroes: React.FC<SceneProps> = (p) => (
  <Documento
    {...p}
    cue="construction"
    chave={6}
    linhas={[
      "SLAVUTYCH — A CITY BUILT BY EIGHT SOVIET REPUBLICS",
      "Kyiv Quarter        Tbilisi Quarter",
      "Yerevan Quarter     Riga Quarter",
      "Vilnius Quarter     Baku Quarter",
      "Tallinn Quarter     Moscow Quarter",
      "",
      "Each brigade built its own neighbourhood.",
    ]}
    carimbo={{ texto: "8 REPUBLICS", cue: "moscow" }}
  />
);

// ---------------- 7. o trem que atravessava a Bielorrússia ----------------
export const A07Trem: React.FC<SceneProps> = (p) => (
  <MapaRota
    {...p}
    kicker="SLAVUTYCH → SEMYKHODY · THE WORKERS' TRAIN"
    unidade="km"
    tint={colors.accent}
    lugares={[
      { nome: "Slavutych", lat: 51.522, lon: 30.757, valor: 0, cue: "morning" },
      { nome: "Belarus", lat: 51.56, lon: 30.45, valor: 25, cue: "belarus" },
      { nome: "Semykhody · the plant", lat: 51.405, lon: 30.085, valor: 50, cue: "pulled", abaixo: true },
    ]}
    linhas={[{ pontos: [[51.78, 30.52], [51.62, 30.57], [51.48, 30.58], [51.32, 30.55]], cor: colors.cool }]}
  />
);

// ---------------- 8. a cidade que deu o nome ----------------
export const A08Cidade: React.FC<SceneProps> = (p) => (
  <MapaRota
    {...p}
    kicker="CHERNOBYL TOWN IS NOT PRIPYAT"
    unidade="km"
    tint={colors.cool}
    lugares={[
      { nome: "Reactor 4", lat: 51.389, lon: 30.099, valor: 0, cue: "named" },
      { nome: "Chernobyl town", lat: 51.276, lon: 30.222, valor: 15, cue: "southeast", abaixo: true },
    ]}
    marca={{ nome: "Pripyat", lat: 51.405, lon: 30.057, nota: "where the workers lived", cue: "pripyat" }}
  />
);

// ---------------- 9. os reatores que continuaram ----------------
export const A09Reatores: React.FC<SceneProps> = (p) => (
  <LinhaDoTempo
    {...p}
    kicker="The plant did not die in 1986"
    tint={colors.accent}
    marcos={[
      { ano: "1986", texto: "Reactor 4 destroyed — 1, 2 and 3 restarted", cue: "destroyed", cor: colors.danger },
      { ano: "1991", texto: "Reactor 2 shut down after a turbine hall fire", cue: "turbine" },
      { ano: "1996", texto: "Reactor 1 closed", cue: "closed" },
      { ano: "2000", texto: "15 December — Reactor 3, the last unit, switched off", cue: "december", cor: colors.accent },
    ]}
  />
);

// ---------------- 10. o arco ----------------
export const A10Arco = painel({
  kicker: "The New Safe Confinement",
  titulo: "A gigantic steel arch",
  linhas: [
    { rotulo: "Funded by", valor: "more than 40 countries", cue: "funded" },
    { rotulo: "Height", valor: "about 108 m", cue: "tall" },
    { rotulo: "Length", valor: "162 m", cue: "long" },
    { rotulo: "Span", valor: "about 257 m", cue: "span" },
    { rotulo: "Weight", valor: "more than 36,000 tonnes", cue: "weighs", destaque: true },
  ],
  tint: "cool",
});

// ---------------- 11. o turno que não pôde voltar ----------------
export const A11Ocupacao: React.FC<SceneProps> = (p) => (
  <Colunas
    {...p}
    kicker="Chernobyl plant under occupation, 2022"
    tint={colors.danger}
    cols={[
      { titulo: "12-hour shift", texto: "They arrived for a normal day.", cue: "normal" },
      { titulo: "No relief crew", texto: "No one could get in.", cue: "relief" },
      { titulo: "Nearly 4 weeks", texto: "Fuel storage, arch sensors, power, cooling.", cue: "weeks", cor: colors.accent },
      { titulo: "Armed soldiers", texto: "In the corridors, with food and medicine running low.", cue: "soldiers", cor: colors.danger },
    ]}
  />
);

// ---------------- 12. o laudo da AIEA ----------------
export const A12IAEA: React.FC<SceneProps> = (p) => (
  <Documento
    {...p}
    cue="inspectors"
    chave={3}
    linhas={[
      "INTERNATIONAL ATOMIC ENERGY AGENCY",
      "New Safe Confinement — inspection, late 2025",
      "",
      "Primary confinement function: LOST",
      "Load-bearing structure: not compromised",
      "Protective shell: no longer sealed as designed",
    ]}
    carimbo={{ texto: "WOUNDED", cue: "decade" }}
  />
);
