// Animações de "Como Vive a Tripulação do Avião de US$ 445 Milhões em 16 Horas Sem Pousar" (pt, arquivo dark) —
// painel 20261011-000110 (baia 1). Emirates A380, voo EK448 Dubai -> Auckland. REGRA: biblioteca + MAPA; todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Odometro } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";

// 1. a rota EK448 (p01)
export const E01Rota: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="VOO EK448 · SEM ESCALA" unidade="km" sep="." lugares={[
    { nome: "Dubai", lat: 25.25, lon: 55.36, valor: 0, cue: "448", abaixo: true },
    { nome: "Auckland · Nova Zelândia", lat: -37.0, lon: 174.79, valor: 14200, cue: "14", abaixo: true },
  ]} tint={colors.cool} />
);

// 2. o exército por trás de cada avião (p06)
export const E02Exercito: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Emirates · para cada A380 na frota", titulo: "Um avião, um exército", linhas: [
    { rotulo: "Pilotos", valor: "20", cue: "20" },
    { rotulo: "Comissários", valor: "133", cue: "133", destaque: true },
  ], tint: "cool" }} />
);

// 3. o tamanho (p10)
export const E03Tamanho: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Ficha técnica · Airbus A380", titulo: "O tamanho do gigante", linhas: [
    { rotulo: "Comprimento", valor: `72,7${NB}m`, cue: "72" },
    { rotulo: "Altura", valor: `24,1${NB}m · um prédio de 8 andares`, cue: "24" },
    { rotulo: "Envergadura", valor: `79,8${NB}m`, cue: "79", destaque: true },
  ], tint: "accent" }} />
);

// 4. a cozinha de Dubai (p15)
export const E04Refeicoes: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="EMIRATES FLIGHT CATERING · DUBAI · MAIS DE" valor={225000} cue="225" sep="."
    sufixo={`${NB}por${NB}dia`}
    nota={{ texto: `refeições · e 120 milhões servidas no A380 em 10 anos`, cue: "120" }} />
);

// 5. a cabine (p22)
export const E05Cabine: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Cabine do A380", titulo: "Uma pequena cidade", linhas: [
    { rotulo: "Janelas", valor: "220", cue: "220" },
    { rotulo: "Portas", valor: "16", cue: "16" },
    { rotulo: "Zonas de temperatura", valor: "15", cue: "15", destaque: true },
    { rotulo: "Temperatura de cada zona", valor: `18 a 30${NB}°C`, cue: "18" },
  ], tint: "cool" }} />
);

// 6. o chuveiro (p46)
export const E06Chuveiro: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Shower Spa · primeira classe", titulo: "Água é peso", linhas: [
    { rotulo: "Água a mais a bordo", valor: `500${NB}kg`, cue: "500" },
    { rotulo: "Aumento", valor: `≈${NB}25${NB}%`, cue: "25" },
    { rotulo: "Água quente por passageiro", valor: `5${NB}minutos`, cue: "5", destaque: true },
  ], tint: "accent" }} />
);

// 7. o porão (p56)
export const E07Volume: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="OS TRÊS NÍVEIS DO A380 · AIRBUS" valor={1570} cue="1" sep="."
    sufixo={`${NB}m³`}
    nota={{ texto: `35 milhões de bolinhas de pingue-pongue`, cue: "35" }} />
);

// 8. a travessia final (p63)
export const E08Travessia: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="AUSTRÁLIA E MAR DA TASMÂNIA" lugares={[
    { nome: "Austrália", lat: -25.0, lon: 133.0, cue: "australia" },
    { nome: "Mar da Tasmânia", lat: -38.5, lon: 160.0, cue: "tasmania", abaixo: true },
    { nome: "Auckland", lat: -37.0, lon: 174.79, cue: "zelandia" },
  ]} tint={colors.cool} />
);

// 9. a volta entre dois voos (p74)
export const E09Virada: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="ENTRE UM VOO E OUTRO · DUBAI" valor={105} cue="105"
    sufixo={`${NB}minutos`} barras={[
      { rotulo: "Padrão da Airbus", v: 90, cue: "90" },
      { rotulo: "Emirates · A380", v: 105, cue: "105", destaque: true },
      { rotulo: "Emirates · Boeing 777", v: 90, cue: "virar" },
    ]} />
);

// 10. a produção (p82)
export const E10Producao: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="A380 ENTREGUES · AIRBUS" valor={251} cue="251"
    sufixo={`${NB}aviões`}
    nota={{ texto: `14 clientes · a Emirates ficou com quase metade`, cue: "14" }} />
);

// 11. a conta final (p89)
export const E11Conta: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Emirates A380 · EK448", titulo: "A conta do gigante", linhas: [
    { rotulo: "Preço de tabela", valor: `US$${NB}445${NB}milhões`, cue: "445" },
    { rotulo: "Peso máximo", valor: `575${NB}t`, cue: "575" },
    { rotulo: "Sem pousar", valor: `14.200${NB}km`, cue: "14" },
    { rotulo: "Na ida", valor: `quase 16${NB}horas`, cue: "16", destaque: true },
  ], tint: "accent" }} />
);
