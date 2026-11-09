// 04/10/2026 (regra do usuário: "10 estilos por tema"): cartões por TEMA — o `tipo` do DOSSIE (minúsculo) -> componente.
// As props do cartão no DOSSIE vão direto para o componente (ver os tipos *Props em src/scenes/estilos_<tema>.tsx).
// Ligar/desligar no painel: guia "Cartões na tela" (painel/catalogo.py); cota em scripts/build_overlays.py (GENERO).
import React from "react";
import { FichaEditAI, LinhaEditAI, EditorialEditAI } from "../scenes/editai_cards";
import { AvisoRecall, LinhaMontagem, RaioX, TesteColisao, Velocimetro } from "../scenes/estilos_carros";
import { DatacaoCarbono, Escaneamento3D, Estratigrafia, EtiquetaMuseu, Papiro, QuadriculaEscavacao } from "../scenes/estilos_arqueologia";
import { ContratoCarimbo, CupomFiscal, PilhaDinheiro, RankingBarras, Rosca } from "../scenes/estilos_economia";
import { ComparaForcas, DossieSecreto, Periscopio, PlacaIdentificacao, Sonar } from "../scenes/estilos_militar";
import { AnuncioRevista, EtiquetaPreco, EvolucaoMarca, Polaroids, TvTubo } from "../scenes/estilos_nostalgia";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const CARTOES_TEMA: Record<string, React.FC<any>> = {
  editai_ficha: FichaEditAI, editai_linha: LinhaEditAI, editai_editorial: EditorialEditAI,
  velocimetro: Velocimetro, raiox: RaioX, testecolisao: TesteColisao, avisorecall: AvisoRecall, linhamontagem: LinhaMontagem,
  estratigrafia: Estratigrafia, papiro: Papiro, etiquetamuseu: EtiquetaMuseu, datacaocarbono: DatacaoCarbono,
  escaneamento3d: Escaneamento3D, quadriculaescavacao: QuadriculaEscavacao,
  cupomfiscal: CupomFiscal, rankingbarras: RankingBarras, rosca: Rosca, pilhadinheiro: PilhaDinheiro, contratocarimbo: ContratoCarimbo,
  dossiesecreto: DossieSecreto, sonar: Sonar, comparaforcas: ComparaForcas, periscopio: Periscopio, placaidentificacao: PlacaIdentificacao,
  tvtubo: TvTubo, anunciorevista: AnuncioRevista, polaroids: Polaroids, evolucaomarca: EvolucaoMarca, etiquetapreco: EtiquetaPreco,
};
