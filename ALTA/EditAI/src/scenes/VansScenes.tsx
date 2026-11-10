// As 6 animações de "The nine vans that reach 300,000 miles" (en). Regra do usuário: pouca tela cheia;
// o peso do filme está nos cartões em papel (src/overlays/Cartoes.tsx) — aqui, na ficha de cada van.
// Todo número é DITO na narração; os cues (scripts/build_plan.py -> CUES) marcam o quadro exato.
import React from "react";
import { useCurrentFrame } from "remotion";
import { colors, type } from "../design/tokens";
import { Painel, PainelSpec } from "./Painel";
import { Colunas, Frame, LinhaDoTempo, Lista } from "./blocos";
import { SceneProps, cue, enter, prog } from "./shared";

const painel = (spec: PainelSpec): React.FC<SceneProps> => {
  const C: React.FC<SceneProps> = (p) => <Painel {...p} spec={spec} />;
  return C;
};

// ---------------- 1. trezentas mil milhas (p000) ----------------
export const A01TrezentasMil: React.FC<SceneProps> = (p) => {
  const frame = useCurrentFrame();
  const c1 = cue(p, "miles|thousand", 0.14);
  const c2 = cue(p, "trips|planet", 0.46);
  const c3 = cue(p, "scrapped|rain", 0.76);
  const t = prog(frame, c2, c2 + 40);
  const R = 190;
  return (
    <Frame p={p} kicker="What the number actually means" tint={colors.accent} grid>
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        <circle cx={1420} cy={560} r={R} fill="none" stroke={colors.line} strokeWidth={5} />
        <circle cx={1420} cy={560} r={R} fill="none" stroke={colors.accent} strokeWidth={14}
                strokeDasharray={2 * Math.PI * R} strokeDashoffset={2 * Math.PI * R * (1 - t)}
                transform={`rotate(-90 1420 560)`} />
        <circle cx={1420 + R * Math.cos(2 * Math.PI * t - Math.PI / 2)}
                cy={560 + R * Math.sin(2 * Math.PI * t - Math.PI / 2)} r={16} fill={colors.accent} />
      </svg>
      <div style={{ position: "absolute", left: 150, top: 230, width: 1000, ...type.display, fontSize: 150,
                    color: colors.accent, ...enter(frame, c1, 26) }}>300,000</div>
      <div style={{ position: "absolute", left: 150, top: 400, width: 980, ...type.display, fontSize: 62,
                    color: colors.text, ...enter(frame, c1 + 10, 22) }}>MILES</div>
      <div style={{ position: "absolute", left: 150, top: 520, width: 980, ...type.bodyMedium, fontSize: 32,
                    color: colors.text, lineHeight: 1.4, ...enter(frame, c2, 20) }}>
        Roughly twelve trips around the entire planet.
      </div>
      <div style={{ position: "absolute", left: 150, top: 900, width: 1620, ...type.bodyMedium, fontSize: 30,
                    color: colors.textDim, ...enter(frame, c3, 18) }}>
        Most vans are scrapped long before they get anywhere near it.
      </div>
      <div style={{ position: "absolute", left: 1270, top: 790, width: 300, textAlign: "center",
                    ...type.display, fontSize: 44, color: colors.cool, ...enter(frame, c2 + 20, 18) }}>12×</div>
    </Frame>
  );
};

// ---------------- 2. três marcas, uma van (p013) ----------------
export const A02TresMarcasUmaVan: React.FC<SceneProps> = (p) => (
  <Colunas
    {...p}
    kicker="Three badges, one van"
    tint={colors.cool}
    cols={[
      { titulo: "RENAULT", texto: "Trafic. The original badge, and the one that names the family.",
        cue: "Trafic|badges", cor: colors.accent },
      { titulo: "VAUXHALL", texto: "Vivaro. Assembled in Britain, at the Luton plant.",
        cue: "Vivaro|Vauxhall", cor: colors.cool },
      { titulo: "NISSAN", texto: "Primastar. The same van again, under a third badge.",
        cue: "Primastar|Nissan", cor: colors.textDim },
    ]}
    nota={{ texto: "Three brands sold the same vehicle — which is exactly why the parts are cheap.",
            cue: "Primastar|Nissan" }}
  />
);

// ---------------- 3. chassi de caminhão (p030) ----------------
export const A03ChassiDeCaminhao: React.FC<SceneProps> = (p) => {
  const frame = useCurrentFrame();
  const c1 = cue(p, "chassis|frame", 0.18);
  const c2 = cue(p, "lorry|truck", 0.5);
  const c3 = cue(p, "body|steel", 0.78);
  const w = prog(frame, c1, c1 + 34);
  return (
    <Frame p={p} kicker="Why the Daily is different" tint={colors.accent} grid>
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        {/* o corpo, que se apoia em cima */}
        <rect x={340} y={430} width={1100 * prog(frame, c3, c3 + 26)} height={150} fill="none"
              stroke={colors.textDim} strokeWidth={5} />
        {/* as duas longarinas do chassi */}
        <rect x={340} y={640} width={1180 * w} height={34} fill={colors.accent} />
        <rect x={340} y={706} width={1180 * w} height={34} fill={colors.accent} />
        {[0, 1, 2, 3, 4].map((i) => (
          <rect key={i} x={420 + i * 260} y={640} width={26} height={100} fill={colors.accentDim}
                opacity={prog(frame, c2 + i * 5, c2 + 22 + i * 5)} />
        ))}
        <circle cx={520} cy={820} r={62} fill="none" stroke={colors.line} strokeWidth={9} opacity={w} />
        <circle cx={1340} cy={820} r={62} fill="none" stroke={colors.line} strokeWidth={9} opacity={w} />
      </svg>
      <div style={{ position: "absolute", left: 150, top: 200, width: 1620, ...type.display, fontSize: 70,
                    color: colors.text, ...enter(frame, 8, 24) }}>A separate ladder frame chassis</div>
      <div style={{ position: "absolute", left: 1560, top: 420, width: 330, ...type.bodyMedium, fontSize: 27,
                    color: colors.textDim, ...enter(frame, c3, 18) }}>the body simply sits on top</div>
      <div style={{ position: "absolute", left: 1560, top: 650, width: 330, ...type.display, fontSize: 40,
                    color: colors.accent, ...enter(frame, c1, 20) }}>HEAVY<br />STEEL<br />FRAME</div>
      <div style={{ position: "absolute", left: 150, top: 930, width: 1300, ...type.bodyMedium, fontSize: 31,
                    color: colors.text, ...enter(frame, c2, 20) }}>
        Exactly like a lorry — and almost every rival abandoned it.
      </div>
    </Frame>
  );
};

// ---------------- 4. fabricado aqui (p041) ----------------
export const A04FabricadoAqui: React.FC<SceneProps> = (p) => (
  <LinhaDoTempo
    {...p}
    kicker="The Transit was built in Britain"
    tint={colors.cool}
    marcos={[
      { ano: "1965", texto: "The first Transit appears.", cue: "Langley", cor: colors.accent },
      { ano: "LANGLEY", texto: "Where British production began.", cue: "Langley", cor: colors.cool },
      { ano: "SOUTHAMPTON", texto: "The plant that kept building Transits for decades.",
        cue: "Southampton", cor: colors.cool },
      { ano: "2013", texto: "The last British-built Transit leaves the line.",
        cue: "Transits|building", cor: colors.danger },
    ]}
  />
);

// ---------------- 5. os dois motores do Sprinter (p048) ----------------
export const A05DoisMotores: React.FC<SceneProps> = (p) => (
  <Lista
    {...p}
    kicker="Which Sprinter to look for"
    titulo="Two generations, two engines"
    tint={colors.accent}
    itens={[
      { titulo: "2.7 CDI five-cylinder",
        texto: "First generation, the 2000 to 2006 build. Where the legend was born.",
        cue: "CDI|cylinder" },
      { titulo: "2.1 CDI and 3.0 V6",
        texto: "Second generation, 2006 to 2018. Better rust protection, better comfort.",
        cue: "generation|second", cor: colors.cool },
      { titulo: "The one enemy",
        texto: "Rust. Arches, sills, door bottoms and floor, winter after winter.",
        cue: "rust|salt", cor: colors.danger },
    ]}
  />
);

// ---------------- 6. o que todas têm (p052) ----------------
export const A06OQueTodasTem = painel({
  kicker: "What all nine have in common",
  titulo: "None of them rely on luck",
  linhas: [
    { rotulo: "The engines", valor: "understressed", cue: "engines|understressed", destaque: true },
    { rotulo: "The designs", valor: "proven, not experimental", cue: "common|share" },
    { rotulo: "The parts", valor: "easy to find, and cheap", cue: "common|share" },
  ],
  nota: "But even the toughest van in the world will fail if it is neglected.",
  notaCue: "neglected|neglect",
  tint: "accent",
});
