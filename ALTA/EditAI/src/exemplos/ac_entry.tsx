// entrada só com os exemplos do ARQUIVO COLORIZADO (o bundle não depende de data/timeline.json do filme atual)
import React from "react";
import { Composition, registerRoot } from "remotion";
import { EXEMPLOS_AC } from "./ArquivoColorizadoEx";
const Raiz: React.FC = () => (<>{EXEMPLOS_AC.map(([id, C]) => (
  <Composition key={id} id={id} component={C} durationInFrames={180} fps={30} width={1920} height={1080} />))}</>);
registerRoot(Raiz);
