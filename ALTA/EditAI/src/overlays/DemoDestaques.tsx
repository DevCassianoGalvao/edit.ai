// PRÉVIA dos destaques sobrepostos (não entra em filme nenhum): quadro real do filme entregue + um destaque
// por cima, para escolher o estilo antes de ligar no próximo filme. Renderizada por scripts/demo_destaques.mjs.
import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import { Comparativo, Destaque, Estilo, EstiloCtx, Etiqueta, Faixa, NumeroSobreposto } from "./Destaques";
import { CartaoFoto, Comparacao, Fichas, PalavraCheia } from "./Cartoes";

export type DemoProps = { fundo: string; estilo: Estilo; variante: string };

const Peca: React.FC<{ variante: string }> = ({ variante }) => {
  switch (variante) {
    case "etiqueta":
      return <Etiqueta texto="Mojave National Preserve · California" canto="alto-dir" entra={0} fica={600} />;
    case "numero":
      return <NumeroSobreposto valor="118 °F" rotulo="Inside the cab" canto="baixo-dir" entra={0} fica={600} />;
    case "faixa":
      return <Faixa texto="The nearest town is forty miles away — no store around the corner." entra={0} fica={600} />;
    case "comparativo":
      return (
        <Comparativo
          titulo="Cab temperature"
          a={{ rotulo: "Outside, noon", valor: "104 °F", v: 104 }}
          b={{ rotulo: "Inside the cab", valor: "118 °F", v: 118 }}
          canto="baixo-esq"
          entra={0}
          fica={600}
        />
      );
    case "cartao":
      return <CartaoFoto src="demo/c1.jpg" legenda="Kelso Depot · opened 1924" etiqueta="Stop 3 of 7" lado="centro" entra={0} fica={600} />;
    case "comparacao":
      return (
        <Comparacao
          titulo="Same desert, a century apart"
          a={{ src: "demo/c2.jpg", legenda: "Steam era · 1905", rotulo: "Then" }}
          b={{ src: "demo/c3.jpg", legenda: "Union Pacific · today", rotulo: "Now" }}
          entra={0}
          fica={600}
        />
      );
    case "fichas":
      return (
        <Fichas
          itens={[
            { rotulo: "Exhibit A", texto: "Union Pacific heat order" },
            { rotulo: "Exhibit B", texto: "NWS Mojave records" },
            { rotulo: "Exhibit C", texto: "Crew hours of service log" },
          ]}
          entra={0}
          fica={600}
        />
      );
    case "palavra":
      return <PalavraCheia palavra="NOBODY" sub="Forty miles to the nearest town" entra={0} fica={600} />;
    default:
      return <Destaque titulo="KELSO DEPOT" sub="Mojave Desert · 1924" canto="baixo-esq" entra={0} fica={600} />;
  }
};

export const DemoDestaques: React.FC<DemoProps> = ({ fundo, estilo, variante }) => (
  <AbsoluteFill style={{ backgroundColor: "#000" }}>
    <Img src={staticFile(`demo/${fundo}`)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
    <EstiloCtx.Provider value={estilo}>
      <Peca variante={variante} />
    </EstiloCtx.Provider>
  </AbsoluteFill>
);
