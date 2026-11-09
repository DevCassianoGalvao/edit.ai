// Amostras dos 6 cartões de ARQUEOLOGIA (src/scenes/estilos_arqueologia.tsx), com dados realistas em pt-BR.
// Render de um quadro: npx remotion still src/demo_arqueologia/index.ts ArqEstratigrafia out/demo_temas/arq_Estratigrafia_f70.png --frame 70
import React from "react";
import { Composition } from "remotion";
import { DatacaoCarbono, Escaneamento3D, EtiquetaMuseu, Estratigrafia, Papiro, QuadriculaEscavacao } from "../scenes/estilos_arqueologia";

const FPS = 30;
const WIDTH = 1920;
const HEIGHT = 1080;
const D = 180;
const E = { dur: D, t0: 0 };
const F = (n: string) => `demo_arquivo/${n}.jpg`;

const ArqEstratigrafia: React.FC = () => (
  <Estratigrafia {...E} titulo="Vale dos Reis · corte diante da KV62"
    camadas={[
      { rotulo: "Entulho das escavações modernas", data: "séc. XIX–XX" },
      { rotulo: "Cabanas dos operários de Ramsés VI", data: "c. 1150 a.C." },
      { rotulo: "Lascas de calcário da obra da KV9", data: "c. 1145 a.C." },
      { rotulo: "Entrada selada da tumba", data: "c. 1323 a.C." },
      { rotulo: "Rocha-mãe de calcário", data: "Eoceno" },
    ]}
    achado="Primeiro degrau da tumba de Tutancâmon, 4 de novembro de 1922" nivel={3} />
);

const ArqPapiro: React.FC = () => (
  <Papiro {...E} original="𓇋𓏠𓈖 𓏏𓅱𓏏 𓋹 𓋾𓊹 𓍑𓂋 𓇓𓏏"
    traducao="Imagem viva de Amon, governante da Heliópolis do Sul"
    fonte="Cartucho de Tutancâmon · KV62 · 1922" />
);

const ArqEtiquetaMuseu: React.FC = () => (
  <EtiquetaMuseu {...E} src={F("est_egito")} nome="Registro da abertura da tumba de Tutancâmon"
    material="Negativo em placa de vidro" data="Luxor, 1922–1923" inventario="Inv. GI-1922-0427" museu="Griffith Institute · Oxford" />
);

const ArqDatacaoCarbono: React.FC = () => (
  <DatacaoCarbono {...E} titulo="Ötzi, o Homem do Gelo · fragmento de osso da costela" anos={5300} margem={70}
    amostra="AMOSTRA ÖTZ-1991-07" laboratorio="Laboratório de Radiocarbono" />
);

const ArqEscaneamento3D: React.FC = () => (
  <Escaneamento3D {...E} src={F("est_egito")} titulo="Arquivo Carter · fotogrametria"
    pontos={[
      { x: 0.23, y: 0.45, rotulo: "Arthur Mace" },
      { x: 0.67, y: 0.16, rotulo: "Howard Carter" },
      { x: 0.75, y: 0.8, rotulo: "Objeto examinado" },
    ]} />
);

const ArqQuadriculaEscavacao: React.FC = () => (
  <QuadriculaEscavacao {...E} src={F("est_egito")} titulo="Quadrícula da antecâmara" sitio="KV62 · Vale dos Reis · 1922"
    achados={[
      { celula: "B2", rotulo: "Selo de argila da necrópole" },
      { celula: "D3", rotulo: "Fragmento de cerâmica" },
      { celula: "E5", rotulo: "Contas de faiança azul" },
      { celula: "C6", rotulo: "Amuleto de bronze" },
    ]} escala="0 — 1 m" />
);

export const RemotionRoot: React.FC = () => (
  <>
    {([["ArqEstratigrafia", ArqEstratigrafia], ["ArqPapiro", ArqPapiro], ["ArqEtiquetaMuseu", ArqEtiquetaMuseu],
      ["ArqDatacaoCarbono", ArqDatacaoCarbono], ["ArqEscaneamento3D", ArqEscaneamento3D],
      ["ArqQuadriculaEscavacao", ArqQuadriculaEscavacao]] as const).map(([id, C]) => (
      <Composition key={id} id={id} component={C} durationInFrames={D} fps={FPS} width={WIDTH} height={HEIGHT} />
    ))}
  </>
);
