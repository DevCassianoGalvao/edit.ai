import React from "react";
import {Composition} from "remotion";
import {FichaEditAI, LinhaEditAI} from "../scenes/editai_cards";
const Ficha: React.FC = () => <FichaEditAI titulo="DADO EM DESTAQUE" valor="73%" detalhe="Um dado de exemplo para ilustrar o cartão." fonte="EXEMPLO"/>;
const Linha: React.FC = () => <LinhaEditAI titulo="Uma história em quatro marcos" eventos={[{data:"1969",texto:"Primeiro marco"},{data:"1981",texto:"Uma nova etapa"},{data:"2000",texto:"Expansão"},{data:"2026",texto:"O presente"}]}/>;
export const Root: React.FC = () => <><Composition id="Ficha" component={Ficha} durationInFrames={120} fps={30} width={1920} height={1080}/><Composition id="Linha" component={Linha} durationInFrames={120} fps={30} width={1920} height={1080}/></>;
