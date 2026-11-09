// Prévias dos 5 cartões de ECONOMIA / CRISE / AGRO (src/scenes/estilos_economia.tsx), 04/10/2026.
// Render de um quadro: npx remotion still src/demo_economia/index.ts ArqCupomFiscal out/demo_temas/eco_CupomFiscal_f70.png --frame 70
import React from "react";
import { Composition } from "remotion";
import { ContratoCarimbo, CupomFiscal, PilhaDinheiro, RankingBarras, Rosca } from "../scenes/estilos_economia";

const FPS = 30;
const WIDTH = 1920;
const HEIGHT = 1080;
const DUR = 180;
const E = { dur: DUR, t0: 0 };

const ArqCupomFiscal: React.FC = () => (
  <CupomFiscal {...E} titulo="Custo de 1 hectare de soja"
    linhas={[
      { rotulo: "Sementes", valor: "R$ 780,00" },
      { rotulo: "Fertilizantes", valor: "R$ 1.450,00" },
      { rotulo: "Defensivos", valor: "R$ 1.120,00" },
      { rotulo: "Máquinas e diesel", valor: "R$ 690,00" },
      { rotulo: "Arrendamento", valor: "R$ 1.300,00" },
      { rotulo: "Juros do custeio", valor: "R$ 540,00" },
    ]}
    total="R$ 5.880,00" rodape="*** SAFRA 2024/25 · MT ***" />
);
const ArqRankingBarras: React.FC = () => (
  <RankingBarras {...E} titulo="Recuperação judicial no campo"
    unidade="Pedidos de produtores rurais em 2024, por estado"
    itens={[
      { rotulo: "Mato Grosso", valor: 142 },
      { rotulo: "Goiás", valor: 98 },
      { rotulo: "Mato Grosso do Sul", valor: 76 },
      { rotulo: "Rio Grande do Sul", valor: 64, destaque: true },
      { rotulo: "Paraná", valor: 61 },
      { rotulo: "Minas Gerais", valor: 55 },
      { rotulo: "Bahia", valor: 40 },
    ]}
    fonte="Fonte: dados de exemplo para a prévia" />
);
const ArqRosca: React.FC = () => (
  <Rosca {...E} titulo="Crédito rural" pct={38.5}
    rotulo="das cooperativas do Sul renegociaram dívidas em 2025"
    sub="Parcelas de custeio venceram depois de duas quebras de safra seguidas" />
);
const ArqPilhaDinheiro: React.FC = () => (
  <PilhaDinheiro {...E} valor="4,7 bilhões" moeda="R$" rotulo="Dívida das cooperativas em recuperação judicial"
    sub="mais do que o lucro somado de três safras" pilhas={5} />
);
const ArqContratoCarimbo: React.FC = () => (
  <ContratoCarimbo {...E} titulo="Cédula de Crédito Rural"
    partes={["Credor: Banco de fomento agrícola S.A.", "Devedor: Cooperativa Agroindustrial do Oeste"]}
    valor="R$ 412.000.000,00" carimbo="Inadimplente" data="Chapecó, 14 de março de 2024"
    clausula="Cláusula 7ª — O atraso de qualquer parcela implica o vencimento antecipado de toda a dívida, com juros de mora de 1% ao mês e multa de 2% sobre o saldo devedor." />
);

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition id="ArqCupomFiscal" component={ArqCupomFiscal} durationInFrames={DUR} fps={FPS} width={WIDTH} height={HEIGHT} />
      <Composition id="ArqRankingBarras" component={ArqRankingBarras} durationInFrames={DUR} fps={FPS} width={WIDTH} height={HEIGHT} />
      <Composition id="ArqRosca" component={ArqRosca} durationInFrames={DUR} fps={FPS} width={WIDTH} height={HEIGHT} />
      <Composition id="ArqPilhaDinheiro" component={ArqPilhaDinheiro} durationInFrames={DUR} fps={FPS} width={WIDTH} height={HEIGHT} />
      <Composition id="ArqContratoCarimbo" component={ArqContratoCarimbo} durationInFrames={DUR} fps={FPS} width={WIDTH} height={HEIGHT} />
    </>
  );
};
