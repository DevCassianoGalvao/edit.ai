// As 9 animações de "Challenger and Appendix F" (en), modo ULTRA. Regra do usuário: pouca tela cheia;
// o peso do filme está nos cartões em papel (src/overlays/Cartoes.tsx).
// Todo número aqui é DITO na narração; os cues (scripts/build_plan.py -> CUES) marcam o quadro exato.
import React from "react";
import { useCurrentFrame } from "remotion";
import { colors, type } from "../design/tokens";
import { Painel, PainelSpec } from "./Painel";
import { Barras, Frame, Lista } from "./blocos";
import { SceneProps, cue, enter, prog } from "./shared";

const painel = (spec: PainelSpec): React.FC<SceneProps> => {
  const C: React.FC<SceneProps> = (p) => <Painel {...p} spec={spec} />;
  return C;
};

// ---------------- 1. setenta e três segundos (p005) ----------------
export const A01SetentaETres: React.FC<SceneProps> = (p) => {
  const frame = useCurrentFrame();
  const c1 = cue(p, "minute", 0.14);
  const c2 = cue(p, "seventy|73", 0.44);
  const c3 = cue(p, "thousand|48", 0.7);
  const t = prog(frame, c1, c2 + 30);
  return (
    <Frame p={p} kicker="28 January 1986 · 11:38 Eastern" tint={colors.danger} grid>
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        <line x1={200} y1={820} x2={1720} y2={820} stroke={colors.line} strokeWidth={4} />
        <path d={`M 200 820 C 700 ${820 - 420 * t} 1100 ${820 - 520 * t} ${200 + 1220 * t} ${820 - 560 * t}`}
              stroke={colors.accent} strokeWidth={8} fill="none" />
        <circle cx={200 + 1220 * t} cy={820 - 560 * t} r={16} fill={colors.accent} />
        {t > 0.98 ? (
          <g opacity={prog(frame, c2 + 20, c2 + 40)}>
            <circle cx={1420} cy={260} r={70} fill="none" stroke={colors.danger} strokeWidth={9} />
            <line x1={1372} y1={212} x2={1468} y2={308} stroke={colors.danger} strokeWidth={9} />
            <line x1={1468} y1={212} x2={1372} y2={308} stroke={colors.danger} strokeWidth={9} />
          </g>
        ) : null}
      </svg>
      <div style={{ position: "absolute", left: 150, top: 190, width: 900, ...type.display, fontSize: 140,
                    color: colors.danger, ...enter(frame, c2, 26) }}>73 SECONDS</div>
      <div style={{ position: "absolute", left: 150, top: 370, width: 880, ...type.bodyMedium, fontSize: 32,
                    color: colors.text, ...enter(frame, c3, 20) }}>
        At an altitude of about 48,000 feet, the vehicle vanished inside a rolling cloud.
      </div>
      <div style={{ position: "absolute", left: 150, top: 900, width: 1620, ...type.bodyMedium, fontSize: 30,
                    color: colors.textDim, ...enter(frame, c1, 18) }}>
        For just over a minute, everything appeared normal.
      </div>
    </Frame>
  );
};

// ---------------- 2. um quarto de polegada (p017) ----------------
export const A02UmQuartoDePolegada: React.FC<SceneProps> = (p) => {
  const frame = useCurrentFrame();
  const c1 = cue(p, "quarter", 0.2);
  const c2 = cue(p, "circumference", 0.5);
  const c3 = cue(p, "secondary", 0.78);
  const r = 250;
  return (
    <Frame p={p} kicker="What sealed the joint" tint={colors.accent} grid>
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        <circle cx={1380} cy={580} r={r} fill="none" stroke={colors.coolDim} strokeWidth={34}
                opacity={prog(frame, c2, c2 + 20)} />
        <circle cx={1380} cy={580} r={r} fill="none" stroke={colors.accent} strokeWidth={12}
                strokeDasharray={2 * Math.PI * r}
                strokeDashoffset={2 * Math.PI * r * (1 - prog(frame, c2, c2 + 40))} />
        <circle cx={1380} cy={580} r={r - 58} fill="none" stroke={colors.cool} strokeWidth={9}
                opacity={prog(frame, c3, c3 + 20)} />
      </svg>
      <div style={{ position: "absolute", left: 150, top: 240, width: 820, ...type.display, fontSize: 104,
                    color: colors.accent, ...enter(frame, c1, 24) }}>A QUARTER OF AN INCH</div>
      <div style={{ position: "absolute", left: 150, top: 420, width: 800, ...type.bodyMedium, fontSize: 31,
                    color: colors.text, ...enter(frame, c2, 20) }}>
        That is the thickness of the rubber ring that had to run around the entire circumference of the booster.
      </div>
      <div style={{ position: "absolute", left: 150, top: 900, width: 1620, ...type.display, fontSize: 48,
                    color: colors.cool, ...enter(frame, c3, 20) }}>
        PRIMARY O-RING · SECONDARY O-RING
      </div>
    </Frame>
  );
};

// ---------------- 3. mil libras por polegada quadrada (p018) ----------------
export const A03MilPSI: React.FC<SceneProps> = (p) => {
  const frame = useCurrentFrame();
  const c1 = cue(p, "thousand|1000", 0.18);
  const c2 = cue(p, "bulge", 0.48);
  const c3 = cue(p, "rotation", 0.78);
  const abre = 26 * prog(frame, c2, c2 + 30);
  return (
    <Frame p={p} kicker="A fraction of a second after ignition" tint={colors.danger} grid>
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        {/* duas paredes de aço que se abrem */}
        <rect x={700 - abre} y={360} width={200} height={440} fill={colors.coolDim} />
        <rect x={1020 + abre} y={360} width={200} height={440} fill={colors.coolDim} />
        {/* o anel espremido no meio */}
        <circle cx={960} cy={580} r={26} fill={colors.accent} opacity={prog(frame, c1, c1 + 16)} />
        {/* a fresta */}
        <rect x={900 - abre + 0} y={560} width={120 + 2 * abre} height={40} fill={colors.danger}
              opacity={0.35 * prog(frame, c3, c3 + 20)} />
      </svg>
      <div style={{ position: "absolute", left: 150, top: 200, width: 520, ...type.display, fontSize: 92,
                    color: colors.danger, ...enter(frame, c1, 24) }}>1,000 PSI</div>
      <div style={{ position: "absolute", left: 150, top: 340, width: 520, ...type.bodyMedium, fontSize: 29,
                    color: colors.textDim, ...enter(frame, c1 + 10, 18) }}>
        The pressure inside the booster, in a fraction of a second.
      </div>
      <div style={{ position: "absolute", left: 1330, top: 340, width: 440, ...type.display, fontSize: 52,
                    color: colors.accent, ...enter(frame, c2, 20) }}>THE STEEL BULGES</div>
      <div style={{ position: "absolute", left: 150, top: 900, width: 1620, ...type.display, fontSize: 56,
                    color: colors.text, ...enter(frame, c3, 22) }}>
        THE JOINT OPENS FASTER THAN THE RUBBER CAN FOLLOW
      </div>
    </Frame>
  );
};

// ---------------- 4. trinta e dois graus (p029) ----------------
export const A04TrintaEDois: React.FC<SceneProps> = (p) => {
  const frame = useCurrentFrame();
  const c1 = cue(p, "thirty|32", 0.24);
  const c2 = cue(p, "resilience", 0.56);
  const c3 = cue(p, "significance", 0.84);
  return (
    <Frame p={p} kicker="Feynman, at the witness table" tint={colors.cool} grid>
      <div style={{ position: "absolute", left: 150, top: 240, width: 760, ...type.display, fontSize: 150,
                    color: colors.cool, ...enter(frame, c1, 26) }}>32 °F</div>
      <div style={{ position: "absolute", left: 150, top: 430, width: 740, ...type.bodyMedium, fontSize: 31,
                    color: colors.textDim, ...enter(frame, c1 + 10, 18) }}>
        The temperature of ice water. Colder than any launch in the program's history.
      </div>
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        {/* o anel espremido que não volta */}
        <circle cx={1370} cy={520} r={110} fill="none" stroke={colors.accentDim} strokeWidth={26}
                opacity={prog(frame, c2, c2 + 16)} />
        <ellipse cx={1370} cy={520} rx={110} ry={110 - 62 * prog(frame, c2, c2 + 34)} fill="none"
                 stroke={colors.accent} strokeWidth={26} />
      </svg>
      <div style={{ position: "absolute", left: 1180, top: 690, width: 420, textAlign: "center",
                    ...type.display, fontSize: 46, color: colors.accent, ...enter(frame, c2, 20) }}>
        NO RESILIENCE
      </div>
      <div style={{ position: "absolute", left: 150, top: 920, width: 1620, ...type.bodyMedium, fontSize: 34,
                    color: colors.text, ...enter(frame, c3, 20) }}>
        "For at least a few seconds, the material has no resilience at thirty-two degrees."
      </div>
    </Frame>
  );
};

// ---------------- 5. a sequência da falha (p031) ----------------
export const A05SetentaETresSegundos: React.FC<SceneProps> = (p) => {
  const frame = useCurrentFrame();
  const marcos = [
    { t: "0.678 s", s: "Dark grey smoke from the right joint", cue: "half" },
    { t: "37 s", s: "The strongest wind shears of the program", cue: "thirty" },
    { t: "58 s", s: "A flame appears on the booster", cue: "fifty" },
    { t: "73 s", s: "The vehicle breaks apart", cue: "seventy" },
  ];
  const ats = marcos.map((m, i) => cue(p, m.cue, 0.14 + i * 0.22));
  const x0 = 220, x1 = 1700;
  return (
    <Frame p={p} kicker="What the launch films showed" tint={colors.danger} grid>
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        <line x1={x0} y1={580} x2={x0 + (x1 - x0) * prog(frame, 6, 44)} y2={580} stroke={colors.line}
              strokeWidth={6} />
        {ats.map((a, i) => (
          <circle key={i} cx={x0 + ((x1 - x0) * i) / 3} cy={580} r={18}
                  fill={i === 3 ? colors.danger : colors.accent} opacity={prog(frame, a, a + 12)} />
        ))}
      </svg>
      {marcos.map((m, i) => (
        <div key={i} style={{ position: "absolute", left: x0 + ((x1 - x0) * i) / 3 - 180, width: 360,
                              top: i % 2 ? 630 : 350, textAlign: "center", ...enter(frame, ats[i], 24) }}>
          <div style={{ ...type.display, fontSize: 56, color: i === 3 ? colors.danger : colors.accent,
                        lineHeight: 1 }}>{m.t}</div>
          <div style={{ ...type.bodyMedium, fontSize: 25, color: colors.text, marginTop: 12,
                        lineHeight: 1.3 }}>{m.s}</div>
        </div>
      ))}
    </Frame>
  );
};

// ---------------- 6. um em cem contra um em cem mil (p038) ----------------
export const A06UmEmCem: React.FC<SceneProps> = (p) => (
  <Barras {...p} kicker="The same vehicle, two numbers" tint={colors.danger} max={1000}
          titulo="The odds of losing a shuttle" barras={[
    { rotulo: "Working engineers", valor: "about 1 in 100", v: 1000, cue: "hundred", cor: colors.accent },
    { rotulo: "Management's official figure", valor: "1 in 100,000", v: 1, cue: "thousand",
      cor: colors.cool },
  ]} nota={{ texto: "A gap of a thousand times, inside the same agency.", cue: "gap" }} />
);

// ---------------- 7. trezentos anos (p039) ----------------
export const A07TrezentosAnos: React.FC<SceneProps> = (p) => {
  const frame = useCurrentFrame();
  const c1 = cue(p, "hundred|300", 0.3);
  const c2 = cue(p, "thinking|wishful", 0.74);
  const n = Math.round(300 * prog(frame, c1, c1 + 44));
  return (
    <Frame p={p} kicker="What one in a hundred thousand means" tint={colors.cool} grid>
      <div style={{ position: "absolute", left: 150, top: 260, width: 1620, ...type.display, fontSize: 130,
                    color: colors.cool, ...enter(frame, c1, 26) }}>{n} YEARS</div>
      <div style={{ position: "absolute", left: 150, top: 440, width: 1500, ...type.bodyMedium, fontSize: 36,
                    color: colors.text, ...enter(frame, c1 + 12, 20) }}>
        You could launch a shuttle every single day for three centuries and expect to lose only one.
      </div>
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        {Array.from({ length: 60 }).map((_, i) => (
          <rect key={i} x={160 + (i % 20) * 82} y={640 + Math.floor(i / 20) * 70} width={58} height={44}
                fill={i < Math.round(60 * prog(frame, c1, c1 + 44)) ? colors.coolDim : "none"}
                stroke={colors.line} strokeWidth={2} />
        ))}
      </svg>
      <div style={{ position: "absolute", left: 150, top: 900, width: 1620, ...type.display, fontSize: 54,
                    color: colors.accent, ...enter(frame, c2, 22) }}>
        THAT IS NOT ENGINEERING. IT IS WISHFUL THINKING.
      </div>
    </Frame>
  );
};

// ---------------- 8. o fator de segurança (p042) ----------------
export const A08FatorDeSeguranca: React.FC<SceneProps> = (p) => (
  <Lista {...p} kicker="What a safety factor actually is" titulo="The bridge and the O-ring"
         tint={colors.accent} itens={[
    { titulo: "A BRIDGE BUILT FOR THREE TIMES THE LOAD", texto: "That margin is there so nothing is damaged at all.",
      cue: "bridge" },
    { titulo: "AN O-RING EATEN AWAY BY A THIRD", texto: "NASA called the remaining two thirds a safety factor of three.",
      cue: "third", cor: colors.danger },
    { titulo: "BUT THE SEAL WAS NEVER MEANT TO ERODE", texto: "Once it is damaged, there is no margin left to spend.",
      cue: "damaged", cor: colors.danger },
  ]} nota={{ texto: "A margin you have already spent is not a margin.", cue: "factor" }} />
);

// ---------------- 9. as nove recomendações (p057) ----------------
export const A09NoveRecomendacoes = painel({
  kicker: "The Rogers Commission report, June 1986",
  titulo: "Nine recommendations",
  linhas: [
    { rotulo: "The joints", valor: "a complete redesign, reviewed independently", cue: "redesign",
      destaque: true },
    { rotulo: "The organisation", valor: "shuttle management reorganised", cue: "reorganization" },
    { rotulo: "The decision", valor: "engineers' objections must reach the top", cue: "recommendations" },
  ],
  nota: "The shuttle did not fly again for more than two and a half years.",
  notaCue: "years",
  tint: "cool",
});
