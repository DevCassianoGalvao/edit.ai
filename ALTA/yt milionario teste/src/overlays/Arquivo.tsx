// Cartões de ARQUIVO sobre o corte (26/09/2026, regra do usuário para TODO filme): as peças de src/scenes/arquivo*.tsx
// entram como cartão em papel do DOSSIE — tomam o quadro inteiro durante `fica` quadros e o plano segue por baixo.
// Contam no piso de cartões (1 a cada 1,5 min) e NÃO no teto de animações de tela cheia.
import React from "react";
import { AbsoluteFill, Sequence, interpolate, useCurrentFrame } from "remotion";
import { Checklist, FichaCirculo, QuadroProvas, type Campo, type ItemCheck, type Prova } from "../scenes/arquivo";
import { AntesDepois, Lupa, Manchete, Paralaxe, Revela, RoloFilme, Teletipo } from "../scenes/arquivo2";
import { CARTOES_TEMA } from "./temas";
import { CadernoCampo, PainelMercado, PlantaTecnica, RadarTatico, VhsRetro, type Alvo, type Chamada, type Cota } from "../scenes/estilos5";

export type OvArquivo =
  | { tipo: "quadro"; titulo: string; provas: Omit<Prova, "cue">[]; fio?: boolean; tom?: "sepia" | "frio" | "pb"; entra?: number; fica?: number }
  | { tipo: "checklist"; fundo: string; titulo: string; itens: Omit<ItemCheck, "cue">[]; cor?: string; lado?: "direita" | "esquerda"; entra?: number; fica?: number }
  | { tipo: "ficha"; nome: string; orgao: string; campos: Campo[]; relatorio?: number; foto?: string; carimbo?: string;
      modo?: "censurar" | "revelar"; entra?: number; fica?: number }
  | { tipo: "manchete"; jornal: string; data: string; titulo: string; sub?: string; foto?: string; entra?: number; fica?: number }
  | { tipo: "teletipo"; cabecalho: string; data: string; linhas: string[]; entra?: number; fica?: number }
  | { tipo: "lupa"; src: string; x: number; y: number; r?: number; rotulo: string; t?: "sepia" | "frio" | "pb" | "cor"; entra?: number; fica?: number }
  | { tipo: "antesdepois"; a: { src: string; rotulo: string }; b: { src: string; rotulo: string }; sepiaA?: boolean; entra?: number; fica?: number }
  | { tipo: "rolo"; fotos: string[]; titulo?: string; entra?: number; fica?: number }
  | { tipo: "revela"; src: string; legenda?: string; entra?: number; fica?: number }
  | { tipo: "paralaxe"; src: string; fg: string; dir?: 1 | -1; entra?: number; fica?: number }
  // 04/10/2026: 5 estilos por gênero (src/scenes/estilos5.tsx)
  | { tipo: "planta"; src: string; titulo: string; cotas?: Cota[]; chamadas?: Chamada[]; folha?: string; entra?: number; fica?: number }
  | { tipo: "caderno"; src: string; titulo: string; local: string; data: string; notas?: string[]; achado?: string;
      circulo?: { x: number; y: number; r?: number }; escala?: string; entra?: number; fica?: number }
  | { tipo: "mercado"; titulo: string; serie: number[]; rotulos?: string[]; valor: string; variacao?: string; sobe?: boolean;
      ticker?: string[]; unidade?: string; entra?: number; fica?: number }
  | { tipo: "radar"; src?: string; titulo: string; coord?: string; hora?: string; alvos?: Alvo[]; entra?: number; fica?: number }
  | { tipo: "vhs"; src: string; data: string; slogan: string; marca?: string; hora?: string; entra?: number; fica?: number }
  // 04/10/2026: cartões por TEMA (src/overlays/temas.ts) — props livres, iguais às do componente
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  | ({ tipo: "tema"; entra?: number; fica?: number } & Record<string, any>);

export const TIPOS_ARQUIVO = ["quadro", "checklist", "ficha", "manchete", "teletipo", "lupa", "antesdepois", "rolo", "revela", "paralaxe",
  "planta", "caderno", "mercado", "radar", "vhs", ...Object.keys(CARTOES_TEMA)];

const Entrada: React.FC<{ children: React.ReactNode; fade: boolean }> = ({ children, fade }) => {
  const f = useCurrentFrame();
  return <AbsoluteFill style={{ opacity: fade ? interpolate(f, [0, 8], [0, 1], { extrapolateRight: "clamp" }) : 1 }}>{children}</AbsoluteFill>;
};

export const CartaoArquivo: React.FC<{ ov: OvArquivo }> = ({ ov }) => {
  const entra = ov.entra ?? 6;
  const dur = ov.fica ?? 150;
  const base = { dur, t0: 0 };
  const c = (i: number) => `c${i}`;   // sem cue: cada peça entra pela fração da duração
  let el: React.ReactNode = null;
  switch (ov.tipo) {
    case "quadro":
      el = <QuadroProvas {...base} titulo={ov.titulo} tituloCue="-" fio={ov.fio} tom={ov.tom}
        provas={ov.provas.map((p, i) => ({ ...p, cue: c(i) }))} />; break;
    case "checklist":
      el = <Checklist {...base} fundo={ov.fundo} titulo={ov.titulo} cor={ov.cor} lado={ov.lado}
        itens={ov.itens.map((it, i) => ({ ...it, cue: c(i) }))} />; break;
    case "ficha":
      el = <FichaCirculo {...base} nome={ov.nome} nomeCue="-" orgao={ov.orgao} campos={ov.campos} relatorio={ov.relatorio}
        foto={ov.foto} carimbo={ov.carimbo} modo={ov.modo} />; break;
    case "manchete":
      el = <Manchete {...base} jornal={ov.jornal} data={ov.data} titulo={ov.titulo} sub={ov.sub} foto={ov.foto} />; break;
    case "teletipo":
      el = <Teletipo {...base} cabecalho={ov.cabecalho} data={ov.data} linhas={ov.linhas} />; break;
    case "lupa":
      el = <Lupa {...base} src={ov.src} x={ov.x} y={ov.y} r={ov.r} rotulo={ov.rotulo} t={ov.t} />; break;
    case "antesdepois":
      el = <AntesDepois {...base} a={ov.a} b={ov.b} sepiaA={ov.sepiaA} />; break;
    case "rolo":
      el = <RoloFilme {...base} fotos={ov.fotos} titulo={ov.titulo} />; break;
    case "revela":
      el = <Revela {...base} src={ov.src} legenda={ov.legenda} />; break;
    case "paralaxe":
      el = <Paralaxe {...base} src={ov.src} fg={ov.fg} dir={ov.dir} />; break;
    case "planta":
      el = <PlantaTecnica {...base} src={ov.src} titulo={ov.titulo} cotas={ov.cotas} chamadas={ov.chamadas} folha={ov.folha} />; break;
    case "caderno":
      el = <CadernoCampo {...base} src={ov.src} titulo={ov.titulo} local={ov.local} data={ov.data} notas={ov.notas} achado={ov.achado}
        circulo={ov.circulo} escala={ov.escala} />; break;
    case "mercado":
      el = <PainelMercado {...base} titulo={ov.titulo} serie={ov.serie} rotulos={ov.rotulos} valor={ov.valor} variacao={ov.variacao}
        sobe={ov.sobe} ticker={ov.ticker} unidade={ov.unidade} />; break;
    case "radar":
      el = <RadarTatico {...base} src={ov.src} titulo={ov.titulo} coord={ov.coord} hora={ov.hora} alvos={ov.alvos} />; break;
    case "vhs":
      el = <VhsRetro {...base} src={ov.src} data={ov.data} slogan={ov.slogan} marca={ov.marca} hora={ov.hora} />; break;
    default: {
      const C = CARTOES_TEMA[ov.tipo as string];
      if (C) el = <C {...ov} {...base} />;
    }
  }
  return (
    <Sequence from={entra} durationInFrames={dur} layout="none">
      <Entrada fade={ov.tipo !== "paralaxe"}>{el}</Entrada>
    </Sequence>
  );
};
