// As 9 animações de "A Toyota voltou em silêncio ao V8" (pt) — o motor V35A da Tundra e os três recalls.
// Mesmo filme do polonês (seu canal), texto da tela traduzido; o desenho é o mesmo.
// Regra do usuário: pouca tela cheia; o peso do filme está nos cartões em papel (src/overlays/Cartoes.tsx).
// Todo número aqui é DITO na narração; os cues (scripts/build_plan.py -> CUES) marcam o quadro exato.
import React from "react";
import { useCurrentFrame } from "remotion";
import { colors, type } from "../design/tokens";
import { Painel, PainelSpec } from "./Painel";
import { Barras, Colunas, Frame, LinhaDoTempo, Lista } from "./blocos";
import { SceneProps, cue, enter, prog } from "./shared";

const painel = (spec: PainelSpec): React.FC<SceneProps> => {
  const C: React.FC<SceneProps> = (p) => <Painel {...p} spec={spec} />;
  return C;
};

// ---------------- 1. o V8 de 5,7 litros ----------------
export const A01CincoVirgulaSete = painel({
  kicker: "O motor que a Toyota considerou ultrapassado",
  titulo: "3UR-FE",
  linhas: [
    { rotulo: "Cilindrada", valor: "5,7 litros", cue: "cinco|v.rgula", destaque: true },
    { rotulo: "Arquitetura", valor: "V8 aspirado, sem turbo", cue: "tr.s|U R F E|3UR" },
    { rotulo: "Por quanto tempo", valor: "mais de uma década sob o capô", cue: "d.cada" },
  ],
  nota: "Não o design, não a tela no painel. Apenas a certeza de que a picape ia chegar.",
  notaCue: "d.cada",
  tint: "accent",
});

// ---------------- 2. o V35A ----------------
export const A02VTrintaCinco: React.FC<SceneProps> = (p) => (
  <Colunas
    {...p}
    kicker="Terceira geração da Tundra, 2022"
    tint={colors.cool}
    cols={[
      { titulo: "3,5 L", texto: "Menos cilindrada no lugar do V8 aspirado de 5,7 litros.",
        cue: "trinta e cinco|tr.s v.rgula cinco", cor: colors.cool },
      { titulo: "2 TURBOS", texto: "Dois turbocompressores para compensar o que falta de cilindrada.",
        cue: "turbo", cor: colors.accent },
      { titulo: "V35A-FTS", texto: "Mais potência, mais torque, menor consumo. Essa era a promessa.",
        cue: "pot.ncia|torque", cor: colors.textDim },
    ]}
    nota={{ texto: "E, pela primeira vez em muito tempo, não havia nenhum V8 na linha.", cue: "pot.ncia|torque" }}
  />
);

// ---------------- 3. como quebrou ----------------
export const A03ComoQuebrou: React.FC<SceneProps> = (p) => {
  const frame = useCurrentFrame();
  const c1 = cue(p, "limalha|cavaco", 0.16);
  const c2 = cue(p, ".leo", 0.46);
  const c3 = cue(p, "mancal|bronzina", 0.76);
  const cx = [330, 960, 1590];
  const cor = [colors.textDim, colors.cool, colors.danger];
  const rot = ["LIMALHAS", "ÓLEO", "MANCAL"];
  const sub = ["ficaram da usinagem", "leva tudo para dentro", "a película de óleo some"];
  const ats = [c1, c2, c3];
  return (
    <Frame p={p} kicker="Como morre o mancal do virabrequim" tint={colors.danger} grid>
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        {[0, 1].map((i) => (
          <line key={i} x1={cx[i] + 140} y1={560} x2={cx[i] + 140 + 350 * prog(frame, ats[i] + 12, ats[i + 1])}
                y2={560} stroke={colors.line} strokeWidth={6} />
        ))}
        {[0, 1, 2].map((i) => (
          <circle key={i} cx={cx[i]} cy={560} r={125} fill="none" stroke={cor[i]} strokeWidth={7}
                  opacity={prog(frame, ats[i], ats[i] + 20)} />
        ))}
        {/* a película de óleo que desaparece */}
        <line x1={1465} y1={720} x2={1715} y2={720} stroke={colors.danger} strokeWidth={4}
              opacity={prog(frame, c3 + 14, c3 + 30)} />
      </svg>
      {[0, 1, 2].map((i) => (
        <div key={i}>
          <div style={{ position: "absolute", left: cx[i] - 150, top: 525, width: 300, textAlign: "center",
                        ...type.display, fontSize: 44, color: cor[i], ...enter(frame, ats[i], 20) }}>{rot[i]}</div>
          <div style={{ position: "absolute", left: cx[i] - 170, top: 720, width: 340, textAlign: "center",
                        ...type.bodyMedium, fontSize: 26, color: colors.textDim,
                        ...enter(frame, ats[i] + 8, 16) }}>{sub[i]}</div>
        </div>
      ))}
      <div style={{ position: "absolute", left: 150, top: 200, width: 1620, ...type.display, fontSize: 62,
                    color: colors.text, ...enter(frame, 8, 22) }}>
        Tudo depende de uma película de óleo
      </div>
      <div style={{ position: "absolute", left: 150, top: 900, width: 1620, ...type.bodyMedium, fontSize: 30,
                    color: colors.textDim, ...enter(frame, c3, 18) }}>
        Metal encosta em metal. E sempre no mesmo lugar.
      </div>
    </Frame>
  );
};

// ---------------- 4. os três recalls ----------------
export const A04TresChamadas: React.FC<SceneProps> = (p) => (
  <LinhaDoTempo
    {...p}
    kicker="Três recalls, cada vez maiores"
    tint={colors.danger}
    marcos={[
      { ano: "MAIO 2024", texto: "Primeiro recall. Troca do motor inteiro.", cue: "maio", cor: colors.accent },
      { ano: "NOVEMBRO 2025", texto: "Segundo recall. Lista de veículos ampliada.",
        cue: "novembro", cor: colors.cool },
      { ano: "MAIO 2026", texto: "Terceiro recall. Problema maior do que se admitia.",
        cue: "terceiro", cor: colors.danger },
    ]}
  />
);

// ---------------- 5. duzentos e setenta mil ----------------
export const A05DuzentosSetenta: React.FC<SceneProps> = (p) => {
  const frame = useCurrentFrame();
  const c1 = cue(p, "duzentos|setenta", 0.18);
  const c2 = cue(p, "exemplares|meia d.zia", 0.5);
  const c3 = cue(p, "modelo", 0.78);
  const t = prog(frame, c2, c2 + 40);
  const COLS = 30;
  const ROWS = 9;
  return (
    <Frame p={p} kicker="A escala do problema" tint={colors.danger} grid>
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        {Array.from({ length: ROWS * COLS }).map((_, k) => {
          const on = k / (ROWS * COLS) < t;
          return (
            <rect key={k} x={200 + (k % COLS) * 51} y={560 + Math.floor(k / COLS) * 42} width={34} height={22}
                  fill={on ? colors.danger : colors.line} opacity={on ? 0.9 : 0.25} />
          );
        })}
      </svg>
      <div style={{ position: "absolute", left: 150, top: 230, width: 1300, ...type.display, fontSize: 160,
                    color: colors.danger, ...enter(frame, c1, 26) }}>270.000</div>
      <div style={{ position: "absolute", left: 150, top: 420, width: 1300, ...type.display, fontSize: 52,
                    color: colors.text, ...enter(frame, c1 + 10, 20) }}>PICAPES</div>
      <div style={{ position: "absolute", left: 150, top: 960, width: 1620, ...type.bodyMedium, fontSize: 31,
                    color: colors.textDim, ...enter(frame, c3, 18) }}>
        Isso não é defeito de meia dúzia de exemplares. É um problema na escala de um modelo inteiro.
      </div>
    </Frame>
  );
};

// ---------------- 6. setenta mil motores ----------------
export const A06SetentaMil: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="Quantos motores já foram trocados"
    titulo="Setenta mil motores completos"
    tint={colors.accent}
    max={270}
    barras={[
      { rotulo: "No recall", valor: "270.000", v: 270, cue: "setenta", cor: colors.danger },
      { rotulo: "Já trocados", valor: "mais de 70.000", v: 70, cue: "motores", cor: colors.accent },
    ]}
    nota={{ texto: "Tirados das picapes, embalados e devolvidos. Um por um.", cue: "trocado|tirados" }}
  />
);

// ---------------- 7. do motor ao teste ----------------
export const A07DoMotorAoTeste: React.FC<SceneProps> = (p) => {
  const frame = useCurrentFrame();
  const c1 = cue(p, "junho", 0.16);
  const c2 = cue(p, "teste|software", 0.5);
  const c3 = cue(p, "troca", 0.8);
  const cai = prog(frame, c2, c2 + 30);
  return (
    <Frame p={p} kicker="Junho de 2026: mudam as regras" tint={colors.cool} grid>
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        <rect x={180} y={430} width={620} height={230} fill="none" stroke={colors.accent} strokeWidth={6}
              opacity={1 - 0.6 * cai} />
        <line x1={800} y1={545} x2={800 + 320 * cai} y2={545} stroke={colors.line} strokeWidth={6} />
        <rect x={1120} y={430} width={620} height={230} fill="none" stroke={colors.cool} strokeWidth={6}
              opacity={prog(frame, c2 + 10, c2 + 34)} />
      </svg>
      <div style={{ position: "absolute", left: 210, top: 470, width: 560, ...type.display, fontSize: 46,
                    color: colors.accent, ...enter(frame, c1, 20) }}>TROCA AUTOMÁTICA<br />DO MOTOR</div>
      <div style={{ position: "absolute", left: 1150, top: 470, width: 560, ...type.display, fontSize: 46,
                    color: colors.cool, ...enter(frame, c2, 20) }}>PRIMEIRO, O TESTE<br />POR SOFTWARE</div>
      <div style={{ position: "absolute", left: 1150, top: 700, width: 600, ...type.bodyMedium, fontSize: 27,
                    color: colors.textDim, ...enter(frame, c3, 18) }}>
        Troca só se o teste detectar o mancal danificado.
      </div>
      <div style={{ position: "absolute", left: 150, top: 200, width: 1620, ...type.display, fontSize: 64,
                    color: colors.text, ...enter(frame, 8, 22) }}>O que o dono realmente recebe</div>
      <div style={{ position: "absolute", left: 150, top: 930, width: 1620, ...type.bodyMedium, fontSize: 30,
                    color: colors.textDim, ...enter(frame, c3 + 8, 18) }}>
        Um mancal danificado muda a vibração do virabrequim. Dá para detectar antes da batida.
      </div>
    </Frame>
  );
};

// ---------------- 8. o novo V8 ----------------
export const A08NovoV8 = painel({
  kicker: "A portas fechadas",
  titulo: "O novo V8",
  linhas: [
    { rotulo: "O que estava sendo feito", valor: "um motor totalmente novo", cue: "novo|desenvolv", destaque: true },
    { rotulo: "Arquitetura", valor: "oito cilindros, de novo", cue: "oito" },
    { rotulo: "Mas não igual", valor: "também turbinado e também híbrido", cue: "h.brido" },
  ],
  nota: "Poucos anos depois de anunciar o fim do V8, a mesma empresa constrói um V8 novo para a mesma picape.",
  notaCue: "h.brido",
  tint: "accent",
});

// ---------------- 9. os cinco passos ----------------
export const A09CincoPassos: React.FC<SceneProps> = (p) => (
  <Lista
    {...p}
    kicker="O que fazer se você tem uma Tundra com o V35A"
    titulo="Cinco coisas"
    tint={colors.cool}
    itens={[
      { titulo: "Consulte o número do chassi", texto: "A lista já foi ampliada três vezes.", cue: "primeiro" },
      { titulo: "Fique atento aos sintomas", texto: "Batida, marcha lenta irregular, luz do motor.", cue: "segundo" },
      { titulo: "Documente tudo", texto: "Cada visita, cada conversa, cada diagnóstico.", cue: "terceiro" },
      { titulo: "Troque o óleo com mais frequência", texto: "Muitos donos encurtam o intervalo.", cue: "quarto",
        cor: colors.accent },
      { titulo: "Pergunte a data de fabricação do motor", texto: "Unidades feitas depois de julho de 2024.",
        cue: "quinto", cor: colors.accent },
    ]}
  />
);
