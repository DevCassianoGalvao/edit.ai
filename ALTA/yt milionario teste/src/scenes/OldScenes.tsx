// Animações de "7 Old-House Features Worth Keeping Before You Start Remodeling" (en, enxuto) — painel 20261101-222207 (b1).
// REGRA: biblioteca (Painel/Odometro/Lista/MapaRota); motion CURTO; todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { Lista } from "./blocos";
import { Odometro, MapaRota } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = "\u00a0";

// 1. quantas vezes cada piso pode ser lixado (p03)
export const A01Floors: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Floors · how many refinishes are left", titulo: "Sand and refinish", linhas: [
    { rotulo: "Solid hardwood", valor: `4 to 6 times`, cue: "four", destaque: true },
    { rotulo: "Engineered, thick top layer", valor: `once or twice`, cue: "once" },
    { rotulo: "Engineered, thin top layer", valor: `maybe never`, cue: "thin" },
  ], tint: "accent" }} />
);

// 3. janelas de madeira bem cuidadas duram 150 anos (p20)
export const A03Windows: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="A PROPERLY MAINTAINED WOOD WINDOW CAN LAST" valor={150} cue="150" sufixo={`${NB}years or more`}
    nota={{ texto: "A wooden sash can be taken apart and fixed with simple tools", cue: "years" }} />
);

// 4. a mesma sala com pé-direito de 10 pés ou 8 pés (p45)
export const A04Ceilings: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "High ceilings · same room, different feel", titulo: "Height you cannot buy back", linhas: [
    { rotulo: "The room", valor: `12${NB}x${NB}12${NB}ft`, cue: "12x12" },
    { rotulo: "With a 10 ft ceiling", valor: `feels generous`, cue: "10", destaque: true },
    { rotulo: "With 8 ft overhead", valor: `a very different space`, cue: "8" },
  ], tint: "cool" }} />
);

// 5. recapitulação dos sete (p54)
export const A05Seven: React.FC<SceneProps> = (p) => (
  <Lista {...p} kicker="Worth keeping" titulo="All seven" tint={colors.accent} itens={[
    { titulo: "Solid wood floors", cue: "floors" },
    { titulo: "Original moldings", cue: "moldings" },
    { titulo: "Wood windows", cue: "windows" },
    { titulo: "Fireplace and chimney", cue: "fireplace" },
    { titulo: "Panel doors", cue: "doors" },
    { titulo: "High ceilings", cue: "ceilings" },
    { titulo: "Built-ins", cue: "built" },
  ]} />
);

// 2. chumbo: mapa dos EUA, casas anteriores a 1978
export const A02Lead: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="OLDER HOMES · UNITED STATES · BUILT BEFORE 1978" lugares={[
    { nome: "Lead paint banned for homes", lat: 39.8, lon: -98.6, cue: "1978|nineteen|seventy" },
  ]} linhas={[
    { pontos: [[48.4,-124.7],[46.2,-124.0],[43.0,-124.4],[40.4,-124.4],[37.8,-122.5],[34.5,-120.5],[32.5,-117.1],[32.7,-114.7],[31.3,-108.2],[29.8,-101.4],[26.0,-97.2],[29.4,-94.7],[29.0,-89.4],[30.4,-88.0],[29.1,-83.0],[25.2,-80.4],[30.5,-81.4],[35.2,-75.5],[38.9,-74.9],[40.5,-74.0],[41.6,-70.0],[44.8,-66.9],[47.4,-68.3],[45.0,-74.7],[43.3,-79.0],[42.0,-83.0],[46.5,-84.5],[48.0,-89.5],[49.0,-95.2],[49.0,-123.0],[48.4,-124.7]] },
  ]} tint={colors.accent} />
);
