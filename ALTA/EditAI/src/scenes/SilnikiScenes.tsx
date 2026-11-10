// As 12 animações de "Trzy firmy, które budują największe silniki odrzutowe" (pl, 40 min). 20 % vídeo / 80 % foto.
// REGRA (25/09/2026): animação em JavaScript pela BIBLIOTECA — MapaRota, Odometro (2), Barras, LinhaDoTempo,
// Lista (2), Documento (2), Colunas, Painel (2). Todo número é DITO na narração; cues em scripts/build_plan.py -> CUES
// (grafia do Whisper: "61", "10 tysięcy", "A 350", "3 ,5", "87 tysięcy").
import React from "react";
import { colors } from "../design/tokens";
import { Painel, PainelSpec } from "./Painel";
import { Colunas, LinhaDoTempo, Lista, Barras } from "./blocos";
import { Documento, MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const painel = (spec: PainelSpec): React.FC<SceneProps> => {
  const C: React.FC<SceneProps> = (p) => <Painel {...p} spec={spec} />;
  return C;
};

// ---------------- 1. trzy firmy, trzy miejsca ----------------
export const A01Trojka: React.FC<SceneProps> = (p) => (
  <MapaRota
    {...p}
    kicker="TRZY FIRMY · TRZY FABRYKI"
    tint={colors.accent}
    lugares={[
      { nome: "GE Aerospace · Ohio", lat: 39.26, lon: -84.42, cue: "ohio" },
      { nome: "Rolls-Royce · Derby", lat: 52.92, lon: -1.48, cue: "derby" },
      { nome: "Pratt & Whitney · Connecticut", lat: 41.76, lon: -72.64, cue: "connecticut", abaixo: true },
    ]}
  />
);

// ---------------- 2. rekord ciągu ----------------
export const A02Ciag: React.FC<SceneProps> = (p) => (
  <Odometro
    {...p}
    kicker="GE9X · TESTY W OHIO · 2017 · REKORD GUINNESSA"
    valor={61}
    cue="61"
    prefixo="~"
    sufixo=" t ciągu"
    nota={{ texto: "Tyle ważą mniej więcej dwa pełne autobusy przegubowe — z jednej maszyny pod skrzydłem.", cue: "autobusy" }}
  />
);

// ---------------- 3. paradoks temperatury ----------------
export const A03Temperatura: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="Temperatura w sercu silnika, °C"
    titulo="Gorętsze niż punkt topnienia"
    tint={colors.danger}
    max={1600}
    barras={[
      { rotulo: "Stop niklu łopatki zaczyna się topić", valor: "ok. 1300 °C", v: 1300, cue: "1300", cor: colors.textDim },
      { rotulo: "Gazy za komorą spalania", valor: "ponad 1500 °C", v: 1600, cue: "gazy", cor: colors.danger },
    ]}
    nota={{ texto: "Łopatka pracuje w płomieniu, który powinien ją stopić w kilka sekund.", cue: "topnienia" }}
  />
);

// ---------------- 4. jeden kryształ ----------------
export const A04Krysztal: React.FC<SceneProps> = (p) => (
  <LinhaDoTempo
    {...p}
    kicker="Pratt & Whitney — jak pokonać pełzanie"
    tint={colors.accent}
    marcos={[
      { ano: "Lata 60.", texto: "Ziarna ułożone w jednym kierunku, wzdłuż łopatki", cue: "60" },
      { ano: "Potem", texto: "Cała łopatka to jeden kryształ — bez granic ziaren", cue: "opracowali", cor: colors.accent },
      { ano: "Lata 80.", texto: "Łopatki monokrystaliczne w lotnictwie cywilnym", cue: "80" },
    ]}
  />
);

// ---------------- 5. obroty ----------------
export const A05Obroty: React.FC<SceneProps> = (p) => (
  <Odometro
    {...p}
    kicker="WAŁ TURBINY WYSOKIEGO CIŚNIENIA"
    valor={10000}
    cue="10"
    sep=" "
    prefixo="> "
    sufixo=" obr./min"
    nota={{ texto: "Jedna łopatka, niewiele większa od palca — moc porównywalna z bolidem Formuły 1.", cue: "formu" }}
  />
);

// ---------------- 6. moduły silnika ----------------
export const A06Moduly: React.FC<SceneProps> = (p) => (
  <Lista
    {...p}
    kicker="Wszystko musi współpracować"
    titulo="Sześć modułów jednego silnika"
    tint={colors.cool}
    itens={[
      { titulo: "Wentylator", cue: "wentylator" },
      { titulo: "Sprężarka niskiego ciśnienia", cue: "sprezarka" },
      { titulo: "Sprężarka wysokiego ciśnienia", cue: "sprezarka" },
      { titulo: "Komora spalania", cue: "komora", cor: colors.danger },
      { titulo: "Turbina wysokiego ciśnienia", cue: "turbina", cor: colors.danger },
      { titulo: "Turbina niskiego ciśnienia", cue: "turbina" },
    ]}
    nota={{ texto: "Jak tryby zegarka: zmiana w jednym miejscu zmienia wszystkie pozostałe.", cue: "zegarka" }}
  />
);

// ---------------- 7. upadłość Rolls-Royce'a ----------------
export const A07Upadlosc: React.FC<SceneProps> = (p) => (
  <Documento
    {...p}
    cue="lutym"
    chave={6}
    linhas={[
      "ROLLS-ROYCE LIMITED — LUTY 1971",
      "Program RB211 dla Lockheeda TriStar",
      "",
      "Łopatki wentylatora z włókna węglowego Hyfil",
      "nie przeszły testu zderzenia z ptakiem.",
      "Kontrakt ze stałą ceną.",
      "Rząd Wielkiej Brytanii nacjonalizuje firmę.",
    ]}
    carimbo={{ texto: "UPADŁOŚĆ", cue: "upadosc" }}
  />
);

// ---------------- 8. testy certyfikacyjne ----------------
export const A08Testy: React.FC<SceneProps> = (p) => (
  <Lista
    {...p}
    kicker="Certyfikacja"
    titulo="Zanim silnik przewiezie pierwszego pasażera"
    tint={colors.accent}
    itens={[
      { titulo: "Połykanie wody", texto: "Ulewa gęstsza, niż zobaczy większość pilotów.", cue: "wody" },
      { titulo: "Grad", texto: "Bryły lodu wrzucane do silnika.", cue: "gradu" },
      { titulo: "Wytrzymałość", texto: "Setki godzin bez przerwy, na maksymalnych temperaturach.", cue: "wytrzyma" },
      { titulo: "Oblodzenie i komory wysokościowe", cue: "oblodzenia" },
      { titulo: "Latające laboratorium", texto: "GE9X pod skrzydłem Boeinga 747.", cue: "747", cor: colors.accent },
    ]}
  />
);

// ---------------- 9. pieniądze z serwisu ----------------
export const A09Serwis: React.FC<SceneProps> = (p) => (
  <Colunas
    {...p}
    kicker="Skąd biorą się pieniądze"
    tint={colors.accent}
    cols={[
      { titulo: "Serwis", texto: "Silnik żyje 20–30 lat.", cue: "serwisu", cor: colors.accent },
      { titulo: "Przeglądy", texto: "Wymiana łopatek, remonty generalne.", cue: "przeglady" },
      { titulo: "Jedna wizyta", texto: "Kilka, a nawet kilkanaście milionów dolarów.", cue: "milionow" },
      { titulo: "Części zamienne", texto: "Tylko od jednego wytwórcy — z wysoką marżą.", cue: "zamienne" },
    ]}
  />
);

// ---------------- 10. kto napędza jakie samoloty ----------------
export const A10Samoloty = painel({
  kicker: "Kto napędza największe samoloty",
  titulo: "Każdy duży samolot — ta sama trójka",
  linhas: [
    { rotulo: "Boeing 777X", valor: "tylko GE9X", cue: "777x", destaque: true },
    { rotulo: "Airbus A350", valor: "tylko Trent XWB · ok. 44 t", cue: "350" },
    { rotulo: "Boeing 787 Dreamliner", valor: "GEnx albo Trent 1000", cue: "787" },
    { rotulo: "Nowe wąskokadłubowe Airbusy", valor: "LEAP albo Pratt & Whitney GTF", cue: "waskokad" },
  ],
  tint: "cool",
});

// ---------------- 11. kryzys metalu proszkowego ----------------
export const A11Proszek: React.FC<SceneProps> = (p) => (
  <Documento
    {...p}
    cue="lipcu"
    chave={6}
    linhas={[
      "RTX — KOMUNIKAT, LIPIEC 2023",
      "Pratt & Whitney, silnik z przekładnią",
      "",
      "Tarcze turbiny z metalu proszkowego:",
      "możliwe mikroskopijne zanieczyszczenia.",
      "Setki silników zdjętych ze skrzydeł.",
      "Koszt: 6–7 miliardów dolarów.",
    ]}
    carimbo={{ texto: "UZIEMIONE", cue: "miesiacami" }}
  />
);

// ---------------- 12. UltraFan ----------------
export const A12UltraFan = painel({
  kicker: "Rolls-Royce UltraFan — Derby, 2023",
  titulo: "Następna generacja",
  linhas: [
    { rotulo: "Średnica wentylatora", valor: "ok. 3,5 m — więcej niż GE9X", cue: "3" },
    { rotulo: "Moc przez przekładnię", valor: "ok. 87 000 KM", cue: "87" },
    { rotulo: "Rekord", valor: "dla przekładni lotniczej", cue: "rekord" },
    { rotulo: "Zużycie paliwa", valor: "ok. 10 % mniej", cue: "10", destaque: true },
  ],
  tint: "accent",
});
