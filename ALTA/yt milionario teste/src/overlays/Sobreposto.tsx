// Despacha o gráfico sobreposto descrito em data/timeline.json (campo `ov`, escrito por scripts/build_overlays.py).
// Modo ULTRA: slate de lugar/data, cartela de capítulo, cartão de citação e lower third (src/overlays/Ultra.tsx)
// entram pelo mesmo caminho dos selos e contadores.
import React from "react";
import { Apontamento, Contador, RotuloLugar, SeloDado } from "./Overlays";
import { CartelaCapitulo, LowerThird, QuoteCard, Slate } from "./Ultra";
import { Canto, Comparativo, Destaque, Etiqueta, Faixa, NumeroSobreposto } from "./Destaques";
import { CartaoFoto, Comparacao, Fichas, PalavraCheia } from "./Cartoes";
import { CartaoArquivo, TIPOS_ARQUIVO, type OvArquivo } from "./Arquivo";

export type OvSpec =
  | { tipo: "selo"; rotulo: string; valor: string; nota?: string; entra?: number; lado?: "esquerda" | "direita" }
  | { tipo: "contador"; rotulo: string; ate: number; sufixo?: string; casas?: number; entra?: number }
  | { tipo: "lugar"; lugar: string; detalhe?: string; entra?: number }
  | { tipo: "apontamento"; x: number; y: number; raio?: number; texto: string; ladoTexto?: "esquerda" | "direita"; entra?: number }
  | { tipo: "slate"; linha1: string; linha2: string; entra?: number; fica?: number }
  | { tipo: "capitulo"; nome: string; lugar?: string; entra?: number; fica?: number }
  | { tipo: "citacao"; frase: string; autor: string; entra?: number; fica: number }
  | { tipo: "lower"; nome: string; detalhe?: string; entra?: number; fica?: number }
  // 21/09/2026 — destaques SOBREPOSTOS (não tomam a tela): ver src/overlays/Destaques.tsx
  | { tipo: "destaque"; titulo: string; sub?: string; canto?: Canto; entra?: number; fica?: number; cor?: string }
  | { tipo: "etiqueta"; texto: string; canto?: Canto; entra?: number; fica?: number; cor?: string }
  | { tipo: "numero"; valor: string; rotulo?: string; canto?: Canto; entra?: number; fica?: number; cor?: string }
  | { tipo: "faixa"; texto: string; entra?: number; fica?: number; cor?: string }
  | { tipo: "comparativo"; titulo?: string; a: { rotulo: string; valor: string; v: number };
      b: { rotulo: string; valor: string; v: number }; canto?: Canto; entra?: number; fica?: number }
  // cartões em papel, tipografia de máquina de escrever: ver src/overlays/Cartoes.tsx
  | { tipo: "cartao"; src: string; legenda: string; etiqueta?: string; lado?: "centro" | "esq" | "dir";
      pb?: boolean; largura?: number; entra?: number; fica?: number }
  | { tipo: "comparacao"; a: { src: string; legenda: string; rotulo?: string };
      b: { src: string; legenda: string; rotulo?: string }; titulo?: string; pb?: boolean; entra?: number; fica?: number }
  | { tipo: "fichas"; itens: { rotulo: string; texto: string }[]; entra?: number; fica?: number }
  | { tipo: "palavra"; palavra: string; sub?: string; entra?: number; fica?: number }
  // 26/09/2026 — cartões de ARQUIVO (quadro de provas, checklist, ficha, manchete, telex, lupa, antes/depois, rolo, revela, paralaxe)
  | OvArquivo;

export const Sobreposto: React.FC<{ ov: OvSpec; dur: number }> = ({ ov, dur }) => {
  if (TIPOS_ARQUIVO.includes(ov.tipo)) return <CartaoArquivo ov={ov as OvArquivo} />;
  switch (ov.tipo) {
    case "selo":
      return <SeloDado rotulo={ov.rotulo} valor={ov.valor} nota={ov.nota} entra={ov.entra} lado={ov.lado} dur={dur} />;
    case "contador":
      return <Contador rotulo={ov.rotulo} ate={ov.ate} sufixo={ov.sufixo} casas={ov.casas} entra={ov.entra} dur={dur} />;
    case "lugar":
      return <RotuloLugar lugar={ov.lugar} detalhe={ov.detalhe} entra={ov.entra} dur={dur} />;
    case "slate":
      return <Slate linha1={ov.linha1} linha2={ov.linha2} entra={ov.entra} fica={ov.fica} />;
    case "capitulo":
      return <CartelaCapitulo nome={ov.nome} lugar={ov.lugar} entra={ov.entra} fica={ov.fica} />;
    case "citacao":
      return <QuoteCard frase={ov.frase} autor={ov.autor} entra={ov.entra} fica={ov.fica} />;
    case "lower":
      return <LowerThird nome={ov.nome} detalhe={ov.detalhe} entra={ov.entra} fica={ov.fica} />;
    case "destaque":
      return <Destaque titulo={ov.titulo} sub={ov.sub} canto={ov.canto} entra={ov.entra} fica={ov.fica} cor={ov.cor} />;
    case "etiqueta":
      return <Etiqueta texto={ov.texto} canto={ov.canto} entra={ov.entra} fica={ov.fica} cor={ov.cor} />;
    case "numero":
      return <NumeroSobreposto valor={ov.valor} rotulo={ov.rotulo} canto={ov.canto} entra={ov.entra} fica={ov.fica} cor={ov.cor} />;
    case "faixa":
      return <Faixa texto={ov.texto} entra={ov.entra} fica={ov.fica} cor={ov.cor} />;
    case "cartao":
      return <CartaoFoto src={ov.src} legenda={ov.legenda} etiqueta={ov.etiqueta} lado={ov.lado} pb={ov.pb}
                         largura={ov.largura} entra={ov.entra} fica={ov.fica} />;
    case "comparacao":
      return <Comparacao a={ov.a} b={ov.b} titulo={ov.titulo} pb={ov.pb} entra={ov.entra} fica={ov.fica} />;
    case "fichas":
      return <Fichas itens={ov.itens} entra={ov.entra} fica={ov.fica} />;
    case "palavra":
      return <PalavraCheia palavra={ov.palavra} sub={ov.sub} entra={ov.entra} fica={ov.fica} />;
    case "comparativo":
      return <Comparativo titulo={ov.titulo} a={ov.a} b={ov.b} canto={ov.canto} entra={ov.entra} fica={ov.fica} />;
    case "apontamento":
      return (
        <Apontamento x={ov.x} y={ov.y} raio={ov.raio} texto={ov.texto} ladoTexto={ov.ladoTexto} entra={ov.entra} dur={dur} />
      );
    default:
      return <CartaoArquivo ov={ov as OvArquivo} />;
  }
};
