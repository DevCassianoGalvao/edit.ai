// As 10 animações de "Jak wielki może być statek?" (pl, 29,5 min). 20 % vídeo / 80 % foto.
// REGRA (25/09 + 26/09/2026): animação em JavaScript pela BIBLIOTECA e todo filme com MAPA — MapaCampanha, MapaRota,
// Painel (4), Barras (3), Lista. Todo número é DITO na narração; cues em scripts/build_plan.py -> CUES
// (grafia do Whisper: "Sea Wise Giant", "Nok Nevis", "Ormus", "MSC i RINA"; o norm() descarta "ł" — nada de cue com ł).
// Texto de tela em polonês com espaço NÃO separável antes de unidade (checklist 25/09).
import React from "react";
import { colors } from "../design/tokens";
import { Painel, PainelSpec } from "./Painel";
import { Barras, Lista } from "./blocos";
import { MapaRota } from "./biblioteca";
import { MapaCampanha } from "./arquivo2";
import { SceneProps } from "./shared";

const painel = (spec: PainelSpec): React.FC<SceneProps> => {
  const C: React.FC<SceneProps> = (p) => <Painel {...p} spec={spec} />;
  return C;
};

// ---------------- 1. wymiary Seawise Giant ----------------
export const S01Wymiary = painel({
  kicker: "Seawise Giant · 1979",
  titulo: "Trudny do ogarnięcia wyobraźnią",
  linhas: [
    { rotulo: "Długość", valor: "458 m", cue: "458" },
    { rotulo: "Szerokość", valor: "prawie 70 m", cue: "70" },
    { rotulo: "Zanurzenie", valor: "blisko 25 m — jak ośmiopiętrowy blok", cue: "25" },
    { rotulo: "Masa z ładunkiem", valor: "ponad 650 tysięcy ton", cue: "650", destaque: true },
  ],
  tint: "accent",
});

// ---------------- 2. życie giganta (MAPA) ----------------
export const S02Zycie: React.FC<SceneProps> = (p) => (
  <MapaCampanha
    {...p}
    kicker="SEAWISE GIANT · HAPPY GIANT · JAHRE VIKING · KNOCK NEVIS · MONT"
    pontos={[
      { nome: "Larak (Ormuz)", lat: 26.86, lon: 56.36, data: "1988 · TRAFIONY", cue: "larak" },
      { nome: "Singapur", lat: 1.29, lon: 103.85, data: "REMONT", cue: "singapuru" },
      { nome: "Katar", lat: 25.35, lon: 51.18, data: "PŁYWAJĄCY MAGAZYN", cue: "kataru" },
      { nome: "Alang", lat: 21.4, lon: 72.2, data: "2009 · ZŁOM", cue: "alang" },
      { nome: "Hongkong", lat: 22.3, lon: 114.17, data: "KOTWICA · 36 TON", cue: "hongkongu" },
    ]}
    setas={[
      { de: 0, para: 1, cue: "singapuru" },
      { de: 1, para: 2, cue: "kataru" },
      { de: 2, para: 3, cue: "alang" },
    ]}
  />
);

// ---------------- 3. prawo kwadratu i sześcianu ----------------
export const S03Kwadrat: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="Prawo kwadratu i sześcianu · statek powiększony dwukrotnie"
    titulo="Masa rośnie szybciej niż wytrzymałość"
    tint={colors.accent}
    max={8}
    barras={[
      { rotulo: "Każdy wymiar", valor: "×2", v: 2, cue: "dwukrotnie", cor: colors.textDim },
      { rotulo: "Objętość, masa, ładowność", valor: "×8", v: 8, cue: "osmiokrotnie", cor: colors.danger },
      { rotulo: "Przekrój konstrukcji", valor: "×4", v: 4, cue: "czterokrotnie", cor: colors.cool },
    ]}
  />
);

// ---------------- 4. hogging i sagging ----------------
export const S04Fale: React.FC<SceneProps> = (p) => (
  <Lista
    {...p}
    kicker="Kadłub to gigantyczna belka na wodzie"
    titulo="Fala próbuje złamać statek"
    tint={colors.cool}
    itens={[
      { titulo: "Spokojne morze: woda podpiera cały kadłub", cue: "spokojnym" },
      { titulo: "Grzbiet fali pod środkiem: kadłub wygina się w górę", cue: "grzbiet" },
      { titulo: "HOGGING", cue: "hogging", cor: colors.accent },
      { titulo: "Środek nad doliną: kadłub ugina się w dół — SAGGING", cue: "sagging", cor: colors.danger },
    ]}
  />
);

// ---------------- 5. Panamax ----------------
export const S05Panamax: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="Kanał Panamski · długość statku"
    titulo="Klasy nazwane od miejsc"
    tint={colors.cool}
    max={470}
    barras={[
      { rotulo: "Panamax", valor: "niecałe 300 m · 32 m szerokości", v: 294, cue: "300", cor: colors.textDim },
      { rotulo: "Nowe śluzy · 2016", valor: "366 m · 49 m · 15 m zanurzenia", v: 366, cue: "366", cor: colors.cool },
      { rotulo: "Seawise Giant", valor: "zdecydowanie więcej", v: 458, cue: "wise", cor: colors.danger },
    ]}
  />
);

// ---------------- 6. Malakka (MAPA) ----------------
export const S06Malakka: React.FC<SceneProps> = (p) => (
  <MapaRota
    {...p}
    kicker="MALACCAMAX · OK. 470 M DŁUGOŚCI · 60 M SZEROKOŚCI · PONAD 20 M ZANURZENIA"
    tint={colors.accent}
    lugares={[
      { nome: "Zatoka Perska", lat: 26.5, lon: 52.0, cue: "perskiej" },
      { nome: "Singapur · 25 m głębokości", lat: 1.29, lon: 103.85, cue: "singapuru", abaixo: true },
      { nome: "Lombok", lat: -8.6, lon: 116.1, cue: "lombok", abaixo: true },
    ]}
  />
);

// ---------------- 7. kontenerowce ----------------
export const S07Kontenerowce = painel({
  kicker: "Klasa MSC Irina",
  titulo: "Największe współczesne kontenerowce",
  linhas: [
    { rotulo: "Długość", valor: "prawie 400 m", cue: "400" },
    { rotulo: "Szerokość", valor: "ponad 60 m", cue: "60" },
    { rotulo: "Ładunek", valor: "ponad 24 tysiące TEU", cue: "24" },
    { rotulo: "W jednym rzędzie", valor: "ponad 20 kontenerów", cue: "20", destaque: true },
  ],
  tint: "cool",
});

// ---------------- 8. silnik Emmy Maersk ----------------
export const S08Silnik = painel({
  kicker: "Emma Maersk · dwusuwowy silnik wysokoprężny",
  titulo: "Silnik-rekordzista",
  linhas: [
    { rotulo: "Moc", valor: "ponad 100 tysięcy KM", cue: "100" },
    { rotulo: "Masa", valor: "około 2300 ton", cue: "2300" },
    { rotulo: "Cylindry", valor: "14", cue: "14" },
    { rotulo: "Każdy cylinder", valor: "dorosły człowiek stanie w środku", cue: "wewnatrz", destaque: true },
  ],
  tint: "accent",
});

// ---------------- 9. Prelude ----------------
export const S09Prelude = painel({
  kicker: "Shell Prelude · Samsung, Geoje",
  titulo: "Dłuższa niż Seawise Giant",
  linhas: [
    { rotulo: "Długość × szerokość", valor: "488 m × 74 m", cue: "488" },
    { rotulo: "Wyporność", valor: "około 600 tysięcy ton", cue: "600" },
    { rotulo: "Napęd", valor: "brak — przyholowana do Australii", cue: "napedu" },
    { rotulo: "Gaz schładzany do", valor: "minus 160 °C", cue: "160", destaque: true },
  ],
  tint: "cool",
});

// ---------------- 10. granica ----------------
export const S10Granica: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="Jak wielki może być statek?"
    titulo="Granica nie leży w oceanie"
    tint={colors.accent}
    max={1000}
    barras={[
      { rotulo: "Technicznie możliwe", valor: "konstrukcja długości kilometra", v: 1000, cue: "kilometra", cor: colors.textDim },
      { rotulo: "Realna granica: kanały, porty, ekonomia", valor: "400–470 m", v: 470, cue: "470", cor: colors.accent },
    ]}
  />
);
