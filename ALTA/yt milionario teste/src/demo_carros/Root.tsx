// Prévias dos 5 cartões do tema CARROS (src/scenes/estilos_carros.tsx), 04/10/2026.
// npx remotion still src/demo_carros/index.ts ArqVelocimetro out/demo_temas/carros_Velocimetro_f70.png --frame 70
import React from "react";
import { Composition, Folder } from "remotion";
import { AvisoRecall, LinhaMontagem, RaioX, TesteColisao, Velocimetro } from "../scenes/estilos_carros";

const FPS = 30;
const WIDTH = 1920;
const HEIGHT = 1080;
const D = 180;
const E = { dur: D, t0: 0 };
const F = (n: string) => `demo_arquivo/${n}.jpg`;

export const ArqVelocimetro: React.FC = () => (
  <Velocimetro {...E} titulo="Produção diária" valor={4850} max={6000} unidade="carros/dia" rotulo="Fábrica de Camaçari · BA"
    luzes={["MOTOR", "ÓLEO", "BATERIA"]} />
);
export const ArqRaioX: React.FC = () => (
  <RaioX {...E} src={F("est_carro")} titulo="BYD Seal por dentro"
    pecas={[{ x: 0.13, y: 0.6, rotulo: "porta de carga" }, { x: 0.36, y: 0.82, rotulo: "bateria Blade" },
      { x: 0.83, y: 0.6, rotulo: "motor dianteiro" }]} />
);
export const ArqTesteColisao: React.FC = () => (
  <TesteColisao {...E} src={F("est_retro")} titulo="Latin NCAP · impacto frontal" velocidade="64 km/h"
    resultado="Coluna A deformou 18 cm" nota="Zero estrelas" marcas={[{ x: 0.27, y: 0.6 }, { x: 0.45, y: 0.4 }, { x: 0.7, y: 0.56 }]} />
);
export const ArqAvisoRecall: React.FC = () => (
  <AvisoRecall {...E} marca="BYD" modelo="Seal AWD 2024" defeito="Falha no módulo de airbag do passageiro pode impedir a abertura em colisão."
    unidades={12483} data="03/10/2026" />
);
export const ArqLinhaMontagem: React.FC = () => (
  <LinhaMontagem {...E} titulo="Ford São Bernardo · fechamento" total={2800} unidade="empregos" sub="52 anos de produção encerrados em 2019"
    descendo status="LINHA 1 · PARADA" />
);

export const RemotionRoot: React.FC = () => (
  <Folder name="Carros">
    {([["ArqVelocimetro", ArqVelocimetro], ["ArqRaioX", ArqRaioX], ["ArqTesteColisao", ArqTesteColisao],
      ["ArqAvisoRecall", ArqAvisoRecall], ["ArqLinhaMontagem", ArqLinhaMontagem]] as const).map(([id, C]) => (
      <Composition key={id} id={id} component={C} durationInFrames={D} fps={FPS} width={WIDTH} height={HEIGHT} />
    ))}
  </Folder>
);
