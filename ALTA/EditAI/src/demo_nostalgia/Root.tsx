// Amostras dos 5 cartões do canal TV Nostalgia (marcas brasileiras que sumiram, propaganda antiga, preços de outra moeda).
import React from "react";
import { Composition, Folder } from "remotion";
import { AnuncioRevista, EtiquetaPreco, EvolucaoMarca, Polaroids, TvTubo } from "../scenes/estilos_nostalgia";

const FPS = 30;
const WIDTH = 1920;
const HEIGHT = 1080;
const D = 180;
const base = { dur: D, t0: 0 };
const F = (n: string) => `demo_arquivo/${n}.jpg`;

export const ArqTvTubo: React.FC = () => (
  <TvTubo {...base} src={F("est_retro")} canal="CANAL 4" legenda="Intervalo da novela, 1987: o sedã que toda família queria" />
);

export const ArqAnuncioRevista: React.FC = () => (
  <AnuncioRevista {...base} src={F("est_retro")} chamada="Seu carro novo sai daqui hoje mesmo." marca="Mesbla"
    preco="Cr$ 89.500" ano="1979" rodape="Financiamento em até 24 meses. Consulte as condições na loja." />
);

export const ArqPolaroids: React.FC = () => (
  <Polaroids {...base} titulo="Lembranças do Mappin"
    fotos={[
      { src: F("est_egito"), legenda: "Seu Antônio no balcão, 1972" },
      { src: F("est_retro"), legenda: "O carro novo, 1987" },
      { src: F("est_navio"), legenda: "Porto de Santos" },
      { src: F("est_carro"), legenda: "Salão do Automóvel, 1990" },
    ]} />
);

export const ArqEvolucaoMarca: React.FC = () => (
  <EvolucaoMarca {...base} titulo="Mappin: da vitrine à falência"
    itens={[
      { ano: "1913", rotulo: "Mappin Stores" },
      { ano: "1939", rotulo: "Casa Mappin", src: F("est_egito") },
      { ano: "1962", rotulo: "Mappin" },
      { ano: "1975", rotulo: "Mappin" },
      { ano: "1986", rotulo: "Mappin", src: F("est_retro") },
      { ano: "1999", rotulo: "Mappin", fim: true },
    ]} />
);

export const ArqEtiquetaPreco: React.FC = () => (
  <EtiquetaPreco {...base} produto="Arroz tipo 1 · pacote de 5 kg" antigo="Cr$ 1.890" novo="Cz$ 98,50" ano_antigo="1984" ano_novo="1987"
    multiplicador="×52" />
);

export const RemotionRoot: React.FC = () => (
  <Folder name="Nostalgia">
    {([["ArqTvTubo", ArqTvTubo], ["ArqAnuncioRevista", ArqAnuncioRevista], ["ArqPolaroids", ArqPolaroids],
      ["ArqEvolucaoMarca", ArqEvolucaoMarca], ["ArqEtiquetaPreco", ArqEtiquetaPreco]] as const).map(([id, C]) => (
      <Composition key={id} id={id} component={C} durationInFrames={D} fps={FPS} width={WIDTH} height={HEIGHT} />
    ))}
  </Folder>
);
