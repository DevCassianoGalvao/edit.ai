import React from "react";
import type { SceneProps } from "./shared";
import { L01Rota, L04Ovos, L05Queda, L06Portaria, L14Marambaias, L07Prof, L15Regras, L09Casos, L10Natal, L13Preco } from "./LagScenes";

export type SceneEntry = { C: React.FC<SceneProps>; preview: number };

// Registro das animações (id da Composition sem underscore). Tema: pescadores de lagosta do Ceará (pt, 06/11).
export const SCENES: Record<string, SceneEntry> = {
  "L01-Rota": { C: L01Rota, preview: 600 },
  "L04-Ovos": { C: L04Ovos, preview: 600 },
  "L05-Queda": { C: L05Queda, preview: 600 },
  "L06-Portaria": { C: L06Portaria, preview: 600 },
  "L14-Marambaias": { C: L14Marambaias, preview: 600 },
  "L07-Prof": { C: L07Prof, preview: 600 },
  "L15-Regras": { C: L15Regras, preview: 600 },
  "L09-Casos": { C: L09Casos, preview: 600 },
  "L10-Natal": { C: L10Natal, preview: 600 },
  "L13-Preco": { C: L13Preco, preview: 600 },
};
