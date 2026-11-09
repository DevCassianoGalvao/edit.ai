import React from "react";
import { Composition, Folder } from "remotion";
import { Main } from "./Main";
import sourceMeta from "../data/source_meta.json";
import { SCENES } from "./scenes";
import { DemoDestaques } from "./overlays/DemoDestaques";
import { ExDocumento, ExMapaRota, ExOdometro, ExTermometro } from "./exemplos/Exemplos";
import { EXEMPLOS_AC } from "./exemplos/ArquivoColorizadoEx";
import { ArqAntesDepois, ArqCapitulo, ArqChecklist, ArqChecklistX, ArqFicha, ArqFichaRevela, ArqLupa, ArqManchete, ArqMapa, ArqParalaxe,
  ArqQuadro, ArqQuadroFio, ArqRevela, ArqRolo, ArqTelex, ArqPlanta, ArqCaderno, ArqMercado, ArqRadar, ArqVhs } from "./exemplos/ArquivoDemo";

const FPS = 30;
const WIDTH = 1920;
const HEIGHT = 1080;

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="Main"
        component={Main}
        durationInFrames={sourceMeta.durationInFrames}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
      <Composition
        id="DemoDestaques"
        component={DemoDestaques}
        durationInFrames={90}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
        defaultProps={{ fundo: "f002100.jpg", estilo: "documentario" as const, variante: "destaque" }}
      />
      <Folder name="Exemplos">
        <Composition id="ExMapaRota" component={ExMapaRota} durationInFrames={200} fps={FPS} width={WIDTH} height={HEIGHT} />
        <Composition id="ExOdometro" component={ExOdometro} durationInFrames={170} fps={FPS} width={WIDTH} height={HEIGHT} />
        <Composition id="ExDocumento" component={ExDocumento} durationInFrames={180} fps={FPS} width={WIDTH} height={HEIGHT} />
        <Composition id="ExTermometro" component={ExTermometro} durationInFrames={170} fps={FPS} width={WIDTH} height={HEIGHT} />
      </Folder>
      <Folder name="ArquivoColorizado">
        {EXEMPLOS_AC.map(([id, C]) => (
          <Composition key={id} id={id} component={C} durationInFrames={180} fps={FPS} width={WIDTH} height={HEIGHT} />
        ))}
      </Folder>
      <Folder name="Arquivo">
        {([["ArqQuadro", ArqQuadro], ["ArqQuadroFio", ArqQuadroFio], ["ArqChecklist", ArqChecklist],
          ["ArqChecklistX", ArqChecklistX], ["ArqFicha", ArqFicha], ["ArqFichaRevela", ArqFichaRevela]] as const).map(([id, C]) => (
          <Composition key={id} id={id} component={C} durationInFrames={210} fps={FPS} width={WIDTH} height={HEIGHT} />
        ))}
        {([["ArqManchete", ArqManchete, 150], ["ArqTelex", ArqTelex, 150], ["ArqLupa", ArqLupa, 150], ["ArqAntesDepois", ArqAntesDepois, 150],
          ["ArqRolo", ArqRolo, 150], ["ArqRevela", ArqRevela, 150], ["ArqParalaxe", ArqParalaxe, 150], ["ArqMapa", ArqMapa, 180],
          ["ArqCapitulo", ArqCapitulo, 110], ["ArqPlanta", ArqPlanta, 180], ["ArqCaderno", ArqCaderno, 180],
          ["ArqMercado", ArqMercado, 180], ["ArqRadar", ArqRadar, 180], ["ArqVhs", ArqVhs, 180]] as const).map(([id, C, d]) => (
          <Composition key={id} id={id} component={C} durationInFrames={d} fps={FPS} width={WIDTH} height={HEIGHT} />
        ))}
      </Folder>
      <Folder name="Scenes">
        {Object.entries(SCENES).map(([id, s]) => (
          <Composition
            key={id}
            id={id}
            component={s.C}
            durationInFrames={s.preview}
            fps={FPS}
            width={WIDTH}
            height={HEIGHT}
            defaultProps={{ dur: s.preview, t0: 0 }}
          />
        ))}
      </Folder>
    </>
  );
};
