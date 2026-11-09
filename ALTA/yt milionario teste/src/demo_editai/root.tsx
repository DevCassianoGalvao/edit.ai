import React from "react";
import {Composition, AbsoluteFill} from "remotion";
import {Destaque, EstiloCtx} from "../overlays/Destaques";
import {FichaEditAI, LinhaEditAI, EditorialEditAI} from "../scenes/editai_cards";
const Ficha: React.FC = () => <FichaEditAI titulo="DADO EM DESTAQUE" valor="73%" detalhe="Um dado de exemplo para ilustrar o cartão." fonte="EXEMPLO"/>;
const Linha: React.FC = () => <LinhaEditAI titulo="Uma história em quatro marcos" eventos={[{data:"1969",texto:"Primeiro marco"},{data:"1981",texto:"Uma nova etapa"},{data:"2000",texto:"Expansão"},{data:"2026",texto:"O presente"}]}/>;
const DestaqueEditorial: React.FC = () => <AbsoluteFill style={{background:"#29364a"}}><EstiloCtx.Provider value="editorial"><Destaque titulo="UMA NOVA PERSPECTIVA" sub="DOCUMENTÁRIO" entra={0} fica={110}/></EstiloCtx.Provider></AbsoluteFill>;
const Editorial: React.FC = () => <EditorialEditAI titulo="Por que isso aconteceu?" texto="Uma explicação visual com contexto e fonte." fonte="EXEMPLO"/>;
export const Root: React.FC = () => <><Composition id="DestaqueEditorial" component={DestaqueEditorial} durationInFrames={120} fps={30} width={1920} height={1080}/><Composition id="Editorial" component={Editorial} durationInFrames={120} fps={30} width={1920} height={1080}/><Composition id="Ficha" component={Ficha} durationInFrames={120} fps={30} width={1920} height={1080}/><Composition id="Linha" component={Linha} durationInFrames={120} fps={30} width={1920} height={1080}/></>;
