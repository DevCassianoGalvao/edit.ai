// Animações de "30 horas dentro de un B-52" (es, enxuto) — painel 20261016-213824-b-52 (baia b1).
// REGRA: biblioteca + MAPA; motion curto (cues <= ~14 s); todo número é dito.
import React from "react";
import { colors } from "../design/tokens";
import { Painel } from "./Painel";
import { MapaRota, Documento, Odometro, FotoMedidor } from "./biblioteca";
import { SceneProps } from "./shared";

const NB = " ";
export const FOTO_FRIO = "stock/pb28bf270.jpg";

// 1. o gigante (p04)
export const B01Gigante: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Boeing B-52H Stratofortress", titulo: "Un gigante", linhas: [
    { rotulo: "Largo", valor: `casi 49${NB}metros`, cue: "49" },
    { rotulo: "Envergadura", valor: `más de 56${NB}metros`, cue: "56" },
    { rotulo: "Peso al despegar", valor: `cerca de 220${NB}toneladas`, cue: "220", destaque: true },
  ], tint: "accent" }} />
);

// 2. dois níveis, cinco postos (p07)
export const B02Niveles: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "La tripulación · dos niveles", titulo: "Cinco puestos", linhas: [
    { rotulo: "Arriba", valor: "piloto y copiloto", cue: "abajo" },
    { rotulo: "Abajo", valor: "navegante y navegante de radar", cue: "navegante" },
    { rotulo: "Guerra electrónica", valor: "un oficial", cue: "oficial", destaque: true },
  ], tint: "cool" }} />
);

// 3. a caixa de almoço (p12)
export const B03Caja: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="mano" chave={2} linhas={[
    "CAJA DE ALMUERZO · UNA POR TRIPULANTE",
    "",
    "Sándwiches de pollo, jamón, pavo",
    "Manzanas · naranjas · plátanos",
    "Barras de cereal · frutos secos",
    "Galletas · chocolates",
    "Café en termos grandes",
  ]} carimbo={{ texto: "PARA UNA SOLA MANO", cue: "galletas" }} />
);

// 4. o frio lá fora (p20)
export const B04Frio: React.FC<SceneProps> = (p) => (
  <FotoMedidor {...p} foto={FOTO_FRIO} de={0} ate={-50} unidade={`${NB}°C`} cue="50" efeito="gelo"
    legenda="Fuera del avión · a gran altura · 50 grados bajo cero" />
);

// 5. os aviões-tanque (p30)
export const B05Cisterna: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Reabastecimiento en vuelo", titulo: "Beber en pleno aire", linhas: [
    { rotulo: "Cisterna", valor: "KC-135", cue: "135" },
    { rotulo: "Cada vez más", valor: "KC-46", cue: "46" },
    { rotulo: "La pértiga", valor: "un largo tubo rígido", cue: "tubo", destaque: true },
  ], tint: "accent" }} />
);

// 6. fadiga (p41)
export const B06Fatiga: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Estudios sobre fatiga", titulo: "Horas sin dormir", linhas: [
    { rotulo: `17 o 18${NB}horas`, valor: "como haber bebido alcohol", cue: "17" },
    { rotulo: `24${NB}horas`, valor: "legalmente ebrio", cue: "24", destaque: true },
  ], tint: "danger" }} />
);

// 7. as pílulas (p49)
export const B07Pastillas: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="pastillas" chave={2} linhas={[
    "FUERZA AÉREA DE ESTADOS UNIDOS · MISIONES MUY LARGAS",
    "",
    "Pastillas estimulantes: «pastillas de ir»",
    "Pastillas para dormir: al volver a la base",
    "Solo bajo supervisión de un médico",
  ]} carimbo={{ texto: "MUY REGULADO", cue: "dormir" }} />
);

// 8. Power Flite (p52)
export const B08PowerFlite: React.FC<SceneProps> = (p) => (
  <Odometro {...p} kicker="ENERO DE 1957 · LA VUELTA AL MUNDO SIN ATERRIZAR" valor={39000} cue="39" prefixo="más de "
    sufixo={`${NB}km`} sep="." nota={{ texto: "en 45 horas y 19 minutos", cue: "minutos" }} />
);

// 9. os dois acidentes (p55) — 16/10: o MapaRota Palomares->Thule deixava Thule fora do quadro
export const B09Accidentes: React.FC<SceneProps> = (p) => (
  <Painel {...p} spec={{ kicker: "Dos accidentes con armas nucleares", titulo: "La vida en el límite", linhas: [
    { rotulo: "1966 · España", valor: "Palomares", cue: "palomares" },
    { rotulo: "1968 · Groenlandia", valor: "Thule", cue: "groenlandia", destaque: true },
  ], tint: "danger" }} />
);

// 10. MAPA Secret Squirrel (p58)
export const B10Squirrel: React.FC<SceneProps> = (p) => (
  <MapaRota {...p} kicker="16 DE ENERO DE 1991 · SECRET SQUIRREL" lugares={[
    { nome: "Barksdale · Luisiana", lat: 32.5, lon: -93.66, cue: "squirrel", abaixo: true },
    { nome: "Irak", lat: 33.3, lon: 44.4, cue: "irak" },
  ]} tint={colors.cool} />
);

// 11. o Congresso (p61)
export const B11Congreso: React.FC<SceneProps> = (p) => (
  <Documento {...p} cue="pidió" chave={4} linhas={[
    "CONGRESO DE ESTADOS UNIDOS · 2024",
    "",
    "Mejores asientos",
    "Zonas de descanso más dignas",
    "Baños con mayor intimidad",
  ]} carimbo={{ texto: "EL DESCANSO NO ES UN LUJO", cue: "lujo" }} />
);
