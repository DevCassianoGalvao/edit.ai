// As 10 animações de "Dlaczego samoloty lecą nad Atlantykiem w nocy" (pl, 38 min). 20 % vídeo / 80 % foto.
// REGRA (25/09/2026): animação em JavaScript pela BIBLIOTECA — Colunas, MapaRota (2), LinhaDoTempo (2), Odometro,
// Barras (2), Painel, Lista. Todo número é DITO na narração; cues em scripts/build_plan.py -> CUES
// (grafia do Whisper: "24", "400", "1200", "100", "40", "1958", "707").
import React from "react";
import { colors } from "../design/tokens";
import { Painel, PainelSpec } from "./Painel";
import { Barras, Colunas, LinhaDoTempo, Lista } from "./blocos";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const painel = (spec: PainelSpec): React.FC<SceneProps> => {
  const C: React.FC<SceneProps> = (p) => <Painel {...p} spec={spec} />;
  return C;
};

// ---------------- 1. zegar ----------------
export const A01Strefy: React.FC<SceneProps> = (p) => (
  <Colunas
    {...p}
    kicker="Ta sama chwila, trzy zegary"
    tint={colors.cool}
    cols={[
      { titulo: "Nowy Jork", texto: "19:00 — wieczór.", cue: "jorku" },
      { titulo: "Londyn", texto: "Północ. 5 stref czasowych dalej.", cue: "londynie" },
      { titulo: "Warszawa", texto: "1:00 w nocy. 6 stref dalej.", cue: "warszawie" },
      { titulo: "7 godzin lotu", texto: "Start 19:00 → lądowanie 7:00 rano w Londynie.", cue: "siedem", cor: colors.accent },
    ]}
  />
);

// ---------------- 2. poranny szczyt ----------------
export const A02Szczyt: React.FC<SceneProps> = (p) => (
  <MapaRota
    {...p}
    kicker="PORANNY SZCZYT TRANSATLANTYCKI · 5:00–10:00"
    tint={colors.accent}
    lugares={[
      { nome: "Dublin", lat: 53.35, lon: -6.26, cue: "irlandie" },
      { nome: "Londyn", lat: 51.47, lon: -0.45, cue: "londynie" },
      { nome: "Amsterdam", lat: 52.31, lon: 4.76, cue: "amsterdamie" },
      { nome: "Frankfurt", lat: 50.03, lon: 8.57, cue: "frankfurcie", abaixo: true },
      { nome: "Zurych", lat: 47.46, lon: 8.55, cue: "zurychu", abaixo: true },
    ]}
    marca={{ nome: "Paryż", lat: 49.0, lon: 2.55, nota: "fala setek samolotów", cue: "paryzu" }}
  />
);

// ---------------- 3. obrót samolotu ----------------
export const A03Obrot: React.FC<SceneProps> = (p) => (
  <LinhaDoTempo
    {...p}
    kicker="Jeden samolot, jedna doba"
    tint={colors.accent}
    marcos={[
      { ano: "Wieczór", texto: "Start z Nowego Jorku", cue: "wieczorem" },
      { ano: "Rano", texto: "Lądowanie w Londynie — sprzątanie, tankowanie, catering, załoga", cue: "rano" },
      { ano: "Przed południem", texto: "Start z powrotem", cue: "poudniem" },
      { ano: "24 h", texto: "Dwa przeloty, niemal zero straconego czasu", cue: "24", cor: colors.accent },
    ]}
  />
);

// ---------------- 4. prąd strumieniowy ----------------
export const A04Strumien = painel({
  kicker: "Prąd strumieniowy nad północnym Atlantykiem",
  titulo: "Rzeka powietrza z zachodu na wschód",
  linhas: [
    { rotulo: "Wysokość", valor: "9–12 km", cue: "9" },
    { rotulo: "Zwykle", valor: "od stu kilkudziesięciu do ponad 300 km/h", cue: "trzystu" },
    { rotulo: "Zimą", valor: "ponad 400 km/h", cue: "400", destaque: true },
  ],
  tint: "cool",
});

// ---------------- 5. rekord Ciary ----------------
export const A05Rekord: React.FC<SceneProps> = (p) => (
  <Odometro
    {...p}
    kicker="BURZA CIARA · LUTY 2020 · BRITISH AIRWAYS 747 · NOWY JORK → LONDYN"
    valor={1200}
    cue="1200"
    sep=" "
    prefixo="> "
    sufixo=" km/h"
    nota={{ texto: "4 godziny 56 minut zamiast prawie 7.", cue: "zwykle" }}
  />
);

// ---------------- 6. trasy atlantyckie ----------------
export const A06Tracki: React.FC<SceneProps> = (p) => (
  <MapaRota
    {...p}
    kicker="ZORGANIZOWANY SYSTEM TRAS PÓŁNOCNOATLANTYCKICH"
    tint={colors.cool}
    lugares={[
      { nome: "Gander · trasy na wschód, nocą", lat: 48.95, lon: -54.6, cue: "gander" },
      { nome: "Shanwick · trasy na zachód, w dzień", lat: 55.5, lon: -4.6, cue: "shanwick" },
    ]}
  />
);

// ---------------- 7. odstępy ----------------
export const A07Odstepy: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="Odstęp boczny między samolotami nad oceanem, km"
    titulo="Satelity zbliżyły samoloty"
    tint={colors.accent}
    max={110}
    barras={[
      { rotulo: "Kiedyś, bez radaru", valor: "ponad 100 km", v: 110, cue: "100", cor: colors.textDim },
      { rotulo: "Dziś, z ADS-B z kosmosu", valor: "niewiele ponad 40 km", v: 42, cue: "40", cor: colors.accent },
    ]}
    nota={{ texto: "Odstępy wzdłużne: z kilkunastu minut do kilku.", cue: "wzduzne" }}
  />
);

// ---------------- 8. epoki ----------------
export const A08Epoki: React.FC<SceneProps> = (p) => (
  <LinhaDoTempo
    {...p}
    kicker="Jak skracał się ocean"
    tint={colors.accent}
    marcos={[
      { ano: "1958", texto: "Najpierw brytyjski Comet", cue: "1958" },
      { ano: "1958", texto: "Kilka tygodni później Boeing 707", cue: "707" },
      { ano: "7–8 h", texto: "Wieczorny start = poranny przylot", cue: "wieczorny", cor: colors.accent },
      { ano: "Lata 60.", texto: "Pierwsze zorganizowane trasy atlantyckie", cue: "60" },
    ]}
  />
);

// ---------------- 9. jet lag ----------------
export const A09JetLag: React.FC<SceneProps> = (p) => (
  <Lista
    {...p}
    kicker="Jet lag"
    titulo="Dlaczego lot na wschód jest trudniejszy"
    tint={colors.danger}
    itens={[
      { titulo: "Na zachód: dzień się wydłuża", texto: "Kładziemy się spać później — to łatwe.", cue: "wyduza" },
      { titulo: "Na wschód: dzień się skraca", texto: "Trzeba zasnąć wcześniej, niż chce zegar biologiczny.", cue: "skraca", cor: colors.danger },
      { titulo: "Po przylocie", texto: "Jest 9 rano, a organizm mówi: 3 w nocy.", cue: "dziewiata" },
    ]}
  />
);

// ---------------- 10. jedna noc ----------------
export const A10Noc: React.FC<SceneProps> = (p) => (
  <MapaRota
    {...p}
    kicker="JEDNA NOC NAD ATLANTYKIEM"
    tint={colors.accent}
    lugares={[
      { nome: "Nowa Fundlandia", lat: 47.6, lon: -52.7, cue: "fundlandia" },
      { nome: "30°W · Gander → Shanwick", lat: 52.0, lon: -30.0, cue: "30", abaixo: true },
      { nome: "Irlandia", lat: 52.7, lon: -8.9, cue: "cicho" },
    ]}
  />
);
