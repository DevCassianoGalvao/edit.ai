// As 11 animações de "Alang — największy cmentarz statków" (pl, 38 min). 20 % vídeo / 80 % foto.
// REGRA (25/09/2026): animação em JavaScript pela BIBLIOTECA — Painel, MapaRota, Barras, Lista (2), Colunas,
// Documento, Odometro (2), LinhaDoTempo (2). Todo número é DITO na narração; cues em scripts/build_plan.py -> CUES
// (grafia do Whisper: "1983", "100", "200", "2018", "26", "16", "2006", "2009", "2025").
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

// ---------------- 1. plaża ----------------
export const A01Plaza = painel({
  kicker: "Alang, Gudźarat",
  titulo: "Cmentarz i fabryka jednocześnie",
  linhas: [
    { rotulo: "Wybrzeże", valor: "ok. 10 km", cue: "kilometrow" },
    { rotulo: "Działki stoczniowe", valor: "ponad 150", cue: "piecdziesiat", destaque: true },
    { rotulo: "Na każdej", valor: "jeden, dwa, czasem więcej statków", cue: "kazdej" },
  ],
  tint: "danger",
});

// ---------------- 2. trzy plaże ----------------
export const A02Trojka: React.FC<SceneProps> = (p) => (
  <MapaRota
    {...p}
    kicker="TRZY PLAŻE AZJI POŁUDNIOWEJ · NAWET 4/5 ŚWIATOWEGO TONAŻU"
    tint={colors.danger}
    lugares={[
      { nome: "Alang · od 1983", lat: 21.4, lon: 72.2, cue: "1983" },
      { nome: "Czittagong", lat: 22.45, lon: 91.73, cue: "chittagong|czittagong" },
      { nome: "Gadani", lat: 25.1, lon: 66.7, cue: "gadani", abaixo: true },
    ]}
  />
);

// ---------------- 3. cena ----------------
export const A03Cena: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="Ile płacą stocznie za tonę starego statku"
    titulo="Najbiedniejsze płacą najwięcej"
    tint={colors.accent}
    max={100}
    barras={[
      { rotulo: "Turcja, Chiny, Europa", valor: "wyraźnie mniej", v: 55, cue: "turcji", cor: colors.textDim },
      { rotulo: "Azja Południowa", valor: "+100, +200, a nawet kilkaset $ za tonę", v: 100, cue: "poudniowej", cor: colors.danger },
    ]}
    nota={{ texto: "Przy dużym tankowcu: kilka milionów dolarów różnicy.", cue: "milionow" }}
  />
);

// ---------------- 4. bandery ----------------
export const A04Bandery: React.FC<SceneProps> = (p) => (
  <Lista
    {...p}
    kicker="Pranie tożsamości"
    titulo="Ostatnia podróż pod obcą flagą"
    tint={colors.accent}
    itens={[
      { titulo: "Nowa nazwa", cue: "nazwe" },
      { titulo: "Nowa bandera", texto: "Komory, Saint Kitts i Nevis, Palau, Tuvalu", cue: "bandere", cor: colors.danger },
      { titulo: "Rejestracja na jedną podróż", texto: "Tania i szybka — wyłącznie na ostatni rejs.", cue: "rejestracje" },
    ]}
  />
);

// ---------------- 5. łańcuch ----------------
export const A05Lancuch: React.FC<SceneProps> = (p) => (
  <Colunas
    {...p}
    kicker="Kto co dostaje"
    tint={colors.danger}
    cols={[
      { titulo: "Pośrednik", texto: "Ryzyko prawne i marżę.", cue: "posrednicy" },
      { titulo: "Armator", texto: "Wysoką cenę i czyste ręce.", cue: "armator", cor: colors.accent },
      { titulo: "Stocznia", texto: "Stal.", cue: "stocznia" },
      { titulo: "Robotnik", texto: "Palnik.", cue: "robotnik", cor: colors.danger },
    ]}
  />
);

// ---------------- 6. Seatrade ----------------
export const A06Seatrade: React.FC<SceneProps> = (p) => (
  <Documento
    {...p}
    cue="2018"
    chave={4}
    linhas={[
      "SĄD W HOLANDII — 2018",
      "Sprawa: Seatrade",
      "",
      "4 statki wysłane na plaże w Indiach i Bangladeszu.",
      "Nielegalny eksport odpadów niebezpiecznych.",
      "Grzywna. Zakaz działalności dla dyrektorów.",
    ]}
    carimbo={{ texto: "WINNA", cue: "winna" }}
  />
);

// ---------------- 7. Gadani ----------------
export const A07Gadani: React.FC<SceneProps> = (p) => (
  <Odometro
    {...p}
    kicker="GADANI, PAKISTAN · 1 LISTOPADA 2016 · EKSPLOZJE NA TANKOWCU"
    valor={26}
    cue="26"
    prefixo="≥ "
    sufixo=" zabitych"
    nota={{ texto: "Dziesiątki rannych. Części ciał nigdy nie odnaleziono.", cue: "odnalezion" }}
  />
);

// ---------------- 8. azbest ----------------
export const A08Azbest: React.FC<SceneProps> = (p) => (
  <Odometro
    {...p}
    kicker="KOMISJA SĄDU NAJWYŻSZEGO INDII · 2006 · ROBOTNICY Z ALANG"
    valor={16}
    cue="16"
    prefixo="~"
    sufixo=" %"
    nota={{ texto: "Objawy pylicy azbestowej — mniej więcej co szósty.", cue: "szosty" }}
  />
);

// ---------------- 9. Clemenceau ----------------
export const A09Clemenceau: React.FC<SceneProps> = (p) => (
  <LinhaDoTempo
    {...p}
    kicker="Lotniskowiec Clemenceau — ostatnia podróż"
    tint={colors.cool}
    marcos={[
      { ano: "2006", texto: "Wyrusza do Alang z setkami ton azbestu", cue: "2006" },
      { ano: "Protest", texto: "Greenpeace, sądy we Francji i Indiach", cue: "greenpeace" },
      { ano: "Suez", texto: "Egipt nie chce przepuścić okrętu", cue: "egipt" },
      { ano: "Powrót", texto: "Rozebrany w Wielkiej Brytanii, według norm UE", cue: "zawroci", cor: colors.accent },
    ]}
  />
);

// ---------------- 10. konwencja ----------------
export const A10Konwencja: React.FC<SceneProps> = (p) => (
  <LinhaDoTempo
    {...p}
    kicker="Konwencja z Hongkongu"
    tint={colors.accent}
    marcos={[
      { ano: "2009", texto: "Przyjęta w Hongkongu", cue: "2009" },
      { ano: "16 lat", texto: "Czekanie na ratyfikacje", cue: "16" },
      { ano: "26.06.2025", texto: "Wchodzi w życie", cue: "2025", cor: colors.accent },
    ]}
  />
);

// ---------------- 11. beneficjent nr 1 ----------------
export const A11Armator: React.FC<SceneProps> = (p) => (
  <Lista
    {...p}
    kicker="Kto na tym zarabia"
    titulo="Beneficjent nr 1: armator"
    tint={colors.accent}
    itens={[
      { titulo: "Plaża zamiast stoczni z listy UE", cue: "sprzedajac" },
      { titulo: "Miliony dolarów więcej na jednym statku", cue: "miliony", cor: colors.danger },
      { titulo: "Dziesiątki statków we flocie", cue: "flocie" },
      { titulo: "Akcjonariusze, fundusze — i nasze emerytury", cue: "akcjonariuszy" },
    ]}
  />
);
