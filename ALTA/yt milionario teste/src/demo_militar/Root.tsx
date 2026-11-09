// Prévias dos 5 cartões do tema MILITAR / NAVAL / GUERRA (src/scenes/estilos_militar.tsx), 04/10/2026.
// Render de um quadro: npx remotion still src/demo_militar/index.ts ArqSonar out/demo_temas/mil_Sonar_f70.png --frame 70
import React from "react";
import { Composition, Folder } from "remotion";
import { ComparaForcas, DossieSecreto, Periscopio, PlacaIdentificacao, Sonar } from "../scenes/estilos_militar";

const FPS = 30;
const WIDTH = 1920;
const HEIGHT = 1080;
const D = 180;
const E = { dur: D, t0: 0 };
const F = (n: string) => `demo_arquivo/${n}.jpg`;

export const ArqDossieSecreto: React.FC = () => (
  <DossieSecreto {...E} titulo="Operação MI · Midway" classificacao="Ultrassecreto" data="28 MAIO 1942" origem="CINCPAC · PEARL HARBOR"
    linhas={["Código JN-25 decifrado: o alvo [[AF]] é Midway.", "Força inimiga: [[4 porta-aviões]] de esquadra.",
      "Ataque previsto para [[4 de junho]] ao amanhecer.", "TF-16 e TF-17 aguardam a [[nordeste da ilha]]."]} />
);
export const ArqSonar: React.FC = () => (
  <Sonar {...E} titulo="TK-208 Tajfun · Mar de Barents" profundidade="−180 m"
    contatos={[{ ang: 42, dist: 0.62, rotulo: "SSN LOS ANGELES", distancia: "14 km" },
      { ang: 205, dist: 0.4, rotulo: "QUEBRA-GELO", distancia: "8 km" },
      { ang: 300, dist: 0.82, rotulo: "BALEIA", distancia: "19 km" }]} />
);
export const ArqComparaForcas: React.FC = () => (
  <ComparaForcas {...E} titulo="Midway · 4 de junho de 1942" lados={[
    { nome: "Japão", itens: [{ rotulo: "Porta-aviões", n: 4, icone: "navio" }, { rotulo: "Aviões", n: 248, icone: "aviao" },
      { rotulo: "Encouraçados", n: 11, icone: "navio" }, { rotulo: "Submarinos", n: 16, icone: "submarino" }] },
    { nome: "Estados Unidos", itens: [{ rotulo: "Porta-aviões", n: 3, icone: "navio" }, { rotulo: "Aviões", n: 360, icone: "aviao" },
      { rotulo: "Encouraçados", n: 0, icone: "navio" }, { rotulo: "Submarinos", n: 19, icone: "submarino" }] },
  ]} />
);
export const ArqPeriscopio: React.FC = () => (
  <Periscopio {...E} src={F("est_navio")} titulo="USS Gerald R. Ford · Mediterrâneo" distancia="4.800 m" rumo="072°" />
);
export const ArqPeriscopioBinoculo: React.FC = () => (
  <Periscopio {...E} src={F("est_navio")} titulo="USS Gerald R. Ford · Mediterrâneo" distancia="4.800 m" rumo="072°" modo="binoculo" />
);
export const ArqPlacaIdentificacao: React.FC = () => (
  <PlacaIdentificacao {...E} linhas={["Silva, João B.", "1G-217.458", "Tipo O  ·  T44", "FEB  ·  Brasil"]}
    legenda="Placa de um pracinha da FEB, Monte Castello, fevereiro de 1945" />
);

export const RemotionRoot: React.FC = () => {
  return (
    <Folder name="Militar">
      {([["ArqDossieSecreto", ArqDossieSecreto], ["ArqSonar", ArqSonar], ["ArqComparaForcas", ArqComparaForcas],
        ["ArqPeriscopio", ArqPeriscopio], ["ArqPeriscopioBinoculo", ArqPeriscopioBinoculo],
        ["ArqPlacaIdentificacao", ArqPlacaIdentificacao]] as const).map(([id, C]) => (
        <Composition key={id} id={id} component={C} durationInFrames={D} fps={FPS} width={WIDTH} height={HEIGHT} />
      ))}
    </Folder>
  );
};
