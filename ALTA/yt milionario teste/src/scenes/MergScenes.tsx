// As 12 animações de "Os mergulhadores pagos para tirar corpos de navios naufragados" (pt, 46 min). 20 % vídeo / 80 % foto.
// REGRA (25/09 + 26/09/2026): animação em JavaScript pela BIBLIOTECA e todo filme com MAPA — Lista (2), Colunas, Painel (3),
// Odometro, MapaCampanha (2), Documento (2), Barras. Todo número é DITO na narração; cues em scripts/build_plan.py -> CUES
// (grafia do Whisper: "Biford Dolphin", "Russell Rebello", "Dmitry"; o "476 a bordo" do Sewol NÃO saiu no Whisper — fora da tela).
import React from "react";
import { colors } from "../design/tokens";
import { Painel, PainelSpec } from "./Painel";
import { Barras, Colunas, Lista } from "./blocos";
import { Documento, Odometro } from "./biblioteca";
import { MapaCampanha } from "./arquivo2";
import { SceneProps } from "./shared";

const painel = (spec: PainelSpec): React.FC<SceneProps> => {
  const C: React.FC<SceneProps> = (p) => <Painel {...p} spec={spec} />;
  return C;
};

// ---------------- 1. o pânico ----------------
export const M01Panico: React.FC<SceneProps> = (p) => (
  <Lista
    {...p}
    kicker="Dentro de um navio naufragado"
    titulo="O que mata não é o tubarão"
    tint={colors.cool}
    itens={[
      { titulo: "O maior inimigo é o pânico", cue: "panico" },
      { titulo: "Respira e gasta o gás mais rápido", cue: "gasta" },
      { titulo: "Se movimenta sem pensar", cue: "movimenta" },
      { titulo: "Se perde em segundos num corredor que já conhecia", cue: "perder", cor: colors.danger },
    ]}
  />
);

// ---------------- 2. o umbilical ----------------
export const M02Umbilical: React.FC<SceneProps> = (p) => (
  <Colunas
    {...p}
    kicker="O umbilical · literalmente a vida dele"
    tint={colors.cool}
    cols={[
      { titulo: "Gás", texto: "O que o mergulhador respira.", cue: "gas", cor: colors.accent },
      { titulo: "Voz", texto: "Comunicação com a superfície.", cue: "comunicacao" },
      { titulo: "Água quente", texto: "Para aquecer a roupa.", cue: "quente" },
      { titulo: "Energia", texto: "Câmera e lanterna.", cue: "energia" },
    ]}
  />
);

// ---------------- 3. a equipe na superfície ----------------
export const M03Equipe = painel({
  kicker: "Na superfície",
  titulo: "A sala que acompanha cada mergulho",
  linhas: [
    { rotulo: "Supervisor", valor: "no rádio o tempo inteiro", cue: "supervisor" },
    { rotulo: "Mergulhador de reserva", valor: "equipado, pronto em segundos", cue: "reserva" },
    { rotulo: "Técnicos", valor: "painel de gases, profundidade, tempo", cue: "tecnicos" },
    { rotulo: "Robôs submarinos", valor: "descem antes dos humanos", cue: "robos", destaque: true },
  ],
  tint: "cool",
});

// ---------------- 4. o Kursk ----------------
export const M04Kursk: React.FC<SceneProps> = (p) => (
  <Odometro
    {...p}
    kicker="SUBMARINO NUCLEAR KURSK · MAR DE BARENTS"
    valor={118}
    cue="118"
    sufixo=" homens a bordo"
    nota={{ texto: "Parou a pouco mais de 100 metros de profundidade", cue: "100" }}
  />
);

// ---------------- 5. os noruegueses (MAPA) ----------------
export const M05Noruegueses: React.FC<SceneProps> = (p) => (
  <MapaCampanha
    {...p}
    kicker="DO PETRÓLEO DO MAR DO NORTE ATÉ O KURSK"
    pontos={[
      { nome: "Kursk", lat: 69.6, lon: 37.6, data: "MAR DE BARENTS · RÚSSIA", cue: "russia" },
      { nome: "Mar do Norte", lat: 60.5, lon: 2.8, data: "MERGULHADORES NORUEGUESES", cue: "noruegueses" },
    ]}
    setas={[{ de: 1, para: 0, cue: "saturacao" }]}
  />
);

// ---------------- 6. o bilhete (paráfrase, não o texto original) ----------------
export const M06Bilhete: React.FC<SceneProps> = (p) => (
  <Documento
    {...p}
    cue="bilhete"
    chave={3}
    linhas={[
      "KURSK — COMPARTIMENTO DE POPA",
      "Tenente-capitão Dmitri Kolesnikov",
      "",
      "Uma lista com os nomes dos homens vivos",
      "Escrita no escuro",
      "Ninguém ali conseguiria sair",
      "",
      "Retirado do fundo do mar por um mergulhador",
    ]}
    carimbo={{ texto: "HOUVE SOBREVIVENTES", cue: "sobreviventes" }}
  />
);

// ---------------- 7. saturação ----------------
export const M07Saturacao = painel({
  kicker: "Mergulho de saturação",
  titulo: "Viver sob pressão",
  linhas: [
    { rotulo: "Câmara hiperbárica", valor: "tubos de aço dentro do navio de apoio", cue: "hiperbarica" },
    { rotulo: "Pressão", valor: "a mesma da profundidade de trabalho", cue: "pressurizada" },
    { rotulo: "Tempo lá dentro", valor: "até 28 dias", cue: "28" },
    { rotulo: "Descompressão", valor: "praticamente a mesma no final", cue: "descompressao", destaque: true },
  ],
  tint: "cool",
});

// ---------------- 8. Byford Dolphin ----------------
export const M08Byford: React.FC<SceneProps> = (p) => (
  <Documento
    {...p}
    cue="1983"
    chave={5}
    linhas={[
      "RELATÓRIO DE ACIDENTE — MAR DO NORTE",
      "Plataforma Byford Dolphin · 1983",
      "",
      "Falha na ligação entre câmaras",
      "",
      "Descompressão explosiva",
      "Quatro mergulhadores dentro do sistema",
      "Um técnico do lado de fora",
    ]}
    carimbo={{ texto: "FATAL", cue: "vida", cor: colors.danger }}
  />
);

// ---------------- 9. Russel Rebello (MAPA) ----------------
export const M09Concordia: React.FC<SceneProps> = (p) => (
  <MapaCampanha
    {...p}
    kicker="COSTA CONCORDIA · RUSSEL REBELLO"
    pontos={[
      { nome: "Ilha de Giglio", lat: 42.36, lon: 10.92, data: "DESAPARECEU NAQUELA NOITE", cue: "desapareceu" },
      { nome: "Gênova", lat: 44.41, lon: 8.93, data: "ENCONTRADO · NOVEMBRO DE 2014", cue: "genova" },
    ]}
    setas={[{ de: 0, para: 1, cue: "rebocado" }]}
  />
);

// ---------------- 10. Sewol ----------------
export const M10Sewol: React.FC<SceneProps> = (p) => (
  <Lista
    {...p}
    kicker="Balsa Sewol · 16 de abril de 2014"
    titulo="A instrução"
    tint={colors.cool}
    itens={[
      { titulo: "A maioria: estudantes do ensino médio", cue: "estudantes" },
      { titulo: "\"Permaneçam nas cabines\"", cue: "permanecer" },
      { titulo: "Eles obedeceram", cue: "obedeceram" },
      { titulo: "304 mortos — quase todos adolescentes", cue: "304", cor: colors.danger },
    ]}
  />
);

// ---------------- 11. Estonia ----------------
export const M11Estonia = painel({
  kicker: "Balsa Estonia · Mar Báltico",
  titulo: "28 de setembro de 1994",
  linhas: [
    { rotulo: "Mortos", valor: "852", cue: "852" },
    { rotulo: "Profundidade", valor: "cerca de 80 metros", cue: "80" },
    { rotulo: "Decisão dos governos", valor: "não recuperar as vítimas", cue: "recuperar" },
    { rotulo: "O local", valor: "túmulo oficial · mergulho proibido", cue: "tumulo", destaque: true },
  ],
  tint: "danger",
});

// ---------------- 12. o salário ----------------
export const M12Salario: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="Mergulhador comercial · por dia de trabalho"
    titulo="Quanto se ganha"
    tint={colors.accent}
    max={1200}
    barras={[
      { rotulo: "Águas rasas", valor: "algumas centenas de dólares", v: 350, cue: "centenas", cor: colors.textDim },
      { rotulo: "Saturação · Mar do Norte", valor: "mais de mil dólares", v: 1100, cue: "mil", cor: colors.accent },
    ]}
    nota={{ texto: "Só enquanto está em saturação.", cue: "enquanto" }}
  />
);
