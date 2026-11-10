// As 12 animações de "Noventa dias sem sol" (pt) — submarinos da classe Ohio. Regra do usuário:
// pouca tela cheia; o peso do filme está nos cartões em papel (src/overlays/Cartoes.tsx).
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

// ---------------- 1. o casco (p003) ----------------
export const A01CentoECinquenta = painel({
  kicker: "Um submarino da classe Ohio",
  titulo: "As medidas do casco",
  linhas: [
    { rotulo: "Comprimento", valor: "170 metros e 70 centímetros", cue: "setenta|cento", destaque: true },
    { rotulo: "Deslocamento submerso", valor: "18.700 toneladas", cue: "dezoito|toneladas" },
    { rotulo: "Diâmetro", valor: "cerca de 13 metros", cue: "metros|di.metro" },
  ],
  nota: "Mais do que um campo e meio de futebol colocado em linha reta.",
  notaCue: "metros|di.metro",
  tint: "cool",
});

// ---------------- 2. azul e ouro (p012) ----------------
export const A02DuasTripulacoes: React.FC<SceneProps> = (p) => (
  <Colunas
    {...p}
    kicker="Cada submarino tem duas tripulações"
    tint={colors.accent}
    cols={[
      { titulo: "AZUL", texto: "Está no mar. Setenta e sete dias de patrulha, às vezes noventa ou mais.",
        cue: "Azul|azul", cor: colors.cool },
      { titulo: "OURO", texto: "Está em terra. Descansa, treina e se prepara para a próxima patrulha.",
        cue: "Ouro|ouro", cor: colors.accent },
    ]}
    nota={{ texto: "Entre uma e outra, algumas semanas de manutenção. Então elas trocam de lugar.",
            cue: "setenta e sete|noventa" }}
  />
);

// ---------------- 3. a eletrólise (p025) ----------------
export const A03Eletrolise: React.FC<SceneProps> = (p) => {
  const frame = useCurrentFrame();
  const c1 = cue(p, "eletr.lise", 0.16);
  const c2 = cue(p, "hidrog.nio", 0.5);
  const c3 = cue(p, "oxig.nio", 0.76);
  const t = prog(frame, c1, c1 + 34);
  return (
    <Frame p={p} kicker="De onde vem o ar" tint={colors.cool} grid>
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        <rect x={150} y={470} width={340} height={200} fill="none" stroke={colors.cool} strokeWidth={5} />
        <line x1={490} y1={570} x2={490 + 380 * t} y2={570} stroke={colors.line} strokeWidth={6} />
        <rect x={880} y={430} width={240} height={280} fill="none" stroke={colors.accent} strokeWidth={6}
              opacity={prog(frame, c1 + 10, c1 + 34)} />
        <line x1={1120} y1={500} x2={1120 + 420 * prog(frame, c3, c3 + 26)} y2={500}
              stroke={colors.cool} strokeWidth={6} />
        <line x1={1120} y1={640} x2={1120 + 420 * prog(frame, c2, c2 + 26)} y2={640}
              stroke={colors.danger} strokeWidth={6} />
      </svg>
      <div style={{ position: "absolute", left: 170, top: 500, width: 300, ...type.display, fontSize: 44,
                    color: colors.cool, ...enter(frame, 8, 20) }}>ÁGUA DO MAR</div>
      <div style={{ position: "absolute", left: 170, top: 580, width: 320, ...type.bodyMedium, fontSize: 26,
                    color: colors.textDim, ...enter(frame, 10, 16) }}>hidrogênio e oxigênio, juntos</div>
      <div style={{ position: "absolute", left: 900, top: 520, width: 200, ...type.display, fontSize: 40,
                    color: colors.accent, textAlign: "center", ...enter(frame, c1 + 12, 20) }}>CORRENTE<br />ELÉTRICA</div>
      <div style={{ position: "absolute", left: 1560, top: 452, width: 320, ...type.display, fontSize: 52,
                    color: colors.cool, ...enter(frame, c3, 20) }}>OXIGÊNIO</div>
      <div style={{ position: "absolute", left: 1560, top: 512, width: 340, ...type.bodyMedium, fontSize: 25,
                    color: colors.textDim, ...enter(frame, c3 + 8, 16) }}>vai para a ventilação</div>
      <div style={{ position: "absolute", left: 1560, top: 592, width: 320, ...type.display, fontSize: 52,
                    color: colors.danger, ...enter(frame, c2, 20) }}>HIDROGÊNIO</div>
      <div style={{ position: "absolute", left: 1560, top: 652, width: 340, ...type.bodyMedium, fontSize: 25,
                    color: colors.textDim, ...enter(frame, c2 + 8, 16) }}>descartado no mar</div>
      <div style={{ position: "absolute", left: 150, top: 880, width: 1620, ...type.bodyMedium, fontSize: 30,
                    color: colors.textDim, ...enter(frame, c1, 18) }}>
        O submarino não carrega o ar que respira. Ele fabrica o ar, a partir da água em que está mergulhado.
      </div>
    </Frame>
  );
};

// ---------------- 4. o depurador (p028) ----------------
export const A04Depurador: React.FC<SceneProps> = (p) => {
  const frame = useCurrentFrame();
  const c1 = cue(p, "depuradores|depurador", 0.16);
  const c2 = cue(p, "monoetanolamina", 0.46);
  const c3 = cue(p, "aquecida|liberado", 0.76);
  return (
    <Frame p={p} kicker="O outro lado do problema" tint={colors.danger} grid>
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        <circle cx={420} cy={560} r={130} fill="none" stroke={colors.danger} strokeWidth={6}
                opacity={prog(frame, c1, c1 + 20)} />
        <line x1={550} y1={560} x2={550 + 240 * prog(frame, c1 + 10, c1 + 34)} y2={560}
              stroke={colors.line} strokeWidth={6} />
        <rect x={800} y={450} width={300} height={220} fill="none" stroke={colors.cool} strokeWidth={6}
              opacity={prog(frame, c2, c2 + 20)} />
        <line x1={1100} y1={560} x2={1100 + 260 * prog(frame, c3, c3 + 30)} y2={560}
              stroke={colors.line} strokeWidth={6} />
        <circle cx={1490} cy={560} r={120} fill="none" stroke={colors.accent} strokeWidth={6}
                opacity={prog(frame, c3 + 8, c3 + 28)} />
      </svg>
      <div style={{ position: "absolute", left: 300, top: 520, width: 240, textAlign: "center",
                    ...type.display, fontSize: 46, color: colors.danger, ...enter(frame, c1, 20) }}>CO₂</div>
      <div style={{ position: "absolute", left: 280, top: 720, width: 280, textAlign: "center",
                    ...type.bodyMedium, fontSize: 25, color: colors.textDim, ...enter(frame, c1 + 8, 16) }}>
        o que 150 homens expiram sem parar
      </div>
      <div style={{ position: "absolute", left: 820, top: 500, width: 260, textAlign: "center",
                    ...type.display, fontSize: 36, color: colors.cool, ...enter(frame, c2, 20) }}>
        MONOETANOLAMINA
      </div>
      <div style={{ position: "absolute", left: 800, top: 720, width: 300, textAlign: "center",
                    ...type.bodyMedium, fontSize: 25, color: colors.textDim, ...enter(frame, c2 + 8, 16) }}>
        a amina absorve o gás do ar
      </div>
      <div style={{ position: "absolute", left: 1380, top: 520, width: 220, textAlign: "center",
                    ...type.display, fontSize: 40, color: colors.accent, ...enter(frame, c3 + 8, 20) }}>O MAR</div>
      <div style={{ position: "absolute", left: 1350, top: 720, width: 280, textAlign: "center",
                    ...type.bodyMedium, fontSize: 25, color: colors.textDim, ...enter(frame, c3 + 14, 16) }}>
        aquecida, ela devolve o gás e volta ao começo
      </div>
      <div style={{ position: "absolute", left: 150, top: 890, width: 1620, ...type.bodyMedium, fontSize: 30,
                    color: colors.textDim, ...enter(frame, c1, 18) }}>
        Fabricar oxigênio é metade do trabalho. A outra metade é tirar do ar o que eles expiram.
      </div>
    </Frame>
  );
};

// ---------------- 5. o reator S8G (p038) ----------------
export const A05ReatorS8G: React.FC<SceneProps> = (p) => {
  const frame = useCurrentFrame();
  const c1 = cue(p, "reator", 0.16);
  const c2 = cue(p, "vapor", 0.48);
  const c3 = cue(p, "turbinas|h.lice", 0.76);
  const caixa = (x: number, cor: string, op: number) => (
    <rect x={x} y={440} width={260} height={220} fill="none" stroke={cor} strokeWidth={6} opacity={op} />
  );
  return (
    <Frame p={p} kicker="O coração do submarino" tint={colors.cool} grid>
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        {caixa(160, colors.danger, prog(frame, c1, c1 + 20))}
        {caixa(700, colors.cool, prog(frame, c2, c2 + 20))}
        {caixa(1240, colors.accent, prog(frame, c3, c3 + 20))}
        <line x1={420} y1={550} x2={420 + 280 * prog(frame, c1 + 14, c2)} y2={550}
              stroke={colors.line} strokeWidth={6} />
        <line x1={960} y1={550} x2={960 + 280 * prog(frame, c2 + 14, c3)} y2={550}
              stroke={colors.line} strokeWidth={6} />
        <circle cx={1660} cy={550} r={90} fill="none" stroke={colors.accent} strokeWidth={6}
                opacity={prog(frame, c3 + 12, c3 + 30)} />
      </svg>
      <div style={{ position: "absolute", left: 180, top: 500, width: 220, textAlign: "center",
                    ...type.display, fontSize: 44, color: colors.danger, ...enter(frame, c1, 20) }}>REATOR<br />S8G</div>
      <div style={{ position: "absolute", left: 720, top: 505, width: 220, textAlign: "center",
                    ...type.display, fontSize: 44, color: colors.cool, ...enter(frame, c2, 20) }}>VAPOR</div>
      <div style={{ position: "absolute", left: 1260, top: 505, width: 220, textAlign: "center",
                    ...type.display, fontSize: 44, color: colors.accent, ...enter(frame, c3, 20) }}>TURBINAS</div>
      <div style={{ position: "absolute", left: 1570, top: 690, width: 200, textAlign: "center",
                    ...type.bodyMedium, fontSize: 26, color: colors.textDim, ...enter(frame, c3 + 14, 16) }}>hélice</div>
      <div style={{ position: "absolute", left: 150, top: 880, width: 1620, ...type.bodyMedium, fontSize: 30,
                    color: colors.textDim, ...enter(frame, c1, 18) }}>
        Água sob alta pressão leva o calor do reator até um segundo circuito, que vira vapor. O vapor gira tudo.
      </div>
    </Frame>
  );
};

// ---------------- 6. o dia de dezoito horas (p044) ----------------
export const A06DiaDeDezoito: React.FC<SceneProps> = (p) => {
  const frame = useCurrentFrame();
  const c1 = cue(p, "dezoito", 0.16);
  const c2 = cue(p, "seis horas|seis", 0.46);
  const c3 = cue(p, "vinte e quatro", 0.76);
  const setor = (cx: number, r: number, i: number, n: number, t: number) => {
    const a0 = (-Math.PI / 2) + (2 * Math.PI * i) / n;
    const a1 = (-Math.PI / 2) + (2 * Math.PI * (i + t)) / n;
    const x0 = cx + r * Math.cos(a0), y0 = 560 + r * Math.sin(a0);
    const x1 = cx + r * Math.cos(a1), y1 = 560 + r * Math.sin(a1);
    return `M ${cx} 560 L ${x0} ${y0} A ${r} ${r} 0 0 1 ${x1} ${y1} Z`;
  };
  const cores = [colors.accent, colors.cool, colors.textDim];
  const rot = ["6 h DE SERVIÇO", "6 h DE ESTUDO E MANUTENÇÃO", "6 h DE SONO"];
  return (
    <Frame p={p} kicker="Durante décadas, o dia a bordo não tinha 24 horas" tint={colors.accent} grid>
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        <circle cx={620} cy={560} r={230} fill="none" stroke={colors.line} strokeWidth={4} />
        {[0, 1, 2].map((i) => (
          <path key={i} d={setor(620, 226, i, 3, prog(frame, c2 + i * 10, c2 + 26 + i * 10))}
                fill={cores[i]} opacity={0.32} stroke={cores[i]} strokeWidth={4} />
        ))}
        <circle cx={1420} cy={560} r={230} fill="none" stroke={colors.line} strokeWidth={4}
                opacity={prog(frame, c3, c3 + 20)} />
        <path d={setor(1420, 226, 0, 1, prog(frame, c3 + 6, c3 + 34))} fill={colors.textDim} opacity={0.16}
              stroke={colors.textDim} strokeWidth={4} />
      </svg>
      <div style={{ position: "absolute", left: 470, top: 505, width: 300, textAlign: "center",
                    ...type.display, fontSize: 92, color: colors.accent, ...enter(frame, c1, 24) }}>18 h</div>
      <div style={{ position: "absolute", left: 420, top: 830, width: 400, textAlign: "center",
                    ...type.bodyMedium, fontSize: 26, color: colors.textDim, ...enter(frame, c2, 16) }}>
        {rot.join(" · ")}
      </div>
      <div style={{ position: "absolute", left: 1270, top: 505, width: 300, textAlign: "center",
                    ...type.display, fontSize: 92, color: colors.textDim, ...enter(frame, c3, 24) }}>24 h</div>
      <div style={{ position: "absolute", left: 1220, top: 830, width: 400, textAlign: "center",
                    ...type.bodyMedium, fontSize: 26, color: colors.textDim, ...enter(frame, c3 + 10, 16) }}>
        o dia do corpo humano
      </div>
      <div style={{ position: "absolute", left: 150, top: 950, width: 1620, ...type.bodyMedium, fontSize: 30,
                    color: colors.text, ...enter(frame, c3 + 16, 18) }}>
        O café da manhã de um dia caía na hora do jantar de outro. O corpo nunca se sincronizava.
      </div>
    </Frame>
  );
};

// ---------------- 7. o beliche (p053) ----------------
export const A07Beliche: React.FC<SceneProps> = (p) => {
  const frame = useCurrentFrame();
  const c1 = cue(p, "comprimento", 0.18);
  const c2 = cue(p, "meio metro|altura", 0.5);
  const c3 = cue(p, "cortina", 0.78);
  const w = prog(frame, c1, c1 + 30);
  const h = prog(frame, c2, c2 + 26);
  return (
    <Frame p={p} kicker="O espaço de um homem a bordo" tint={colors.accent} grid>
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        {[0, 1, 2].map((i) => (
          <rect key={i} x={360} y={330 + i * 190} width={1100 * w} height={150} fill="none"
                stroke={i === 1 ? colors.accent : colors.line} strokeWidth={i === 1 ? 6 : 4} />
        ))}
        <line x1={360} y1={880} x2={360 + 1100 * w} y2={880} stroke={colors.cool} strokeWidth={5} />
        <line x1={1500} y1={520} x2={1500} y2={520 + 150 * h} stroke={colors.cool} strokeWidth={5} />
        <line x1={1470} y1={520} x2={1530} y2={520} stroke={colors.cool} strokeWidth={5} opacity={h} />
        <line x1={1470} y1={670} x2={1530} y2={670} stroke={colors.cool} strokeWidth={5} opacity={h} />
      </svg>
      <div style={{ position: "absolute", left: 360, top: 900, width: 1100, textAlign: "center",
                    ...type.display, fontSize: 48, color: colors.cool, ...enter(frame, c1 + 10, 20) }}>
        POUCO MAIS QUE O COMPRIMENTO DE UM HOMEM
      </div>
      <div style={{ position: "absolute", left: 1560, top: 540, width: 330, ...type.display, fontSize: 52,
                    color: colors.cool, ...enter(frame, c2, 20) }}>MENOS DE<br />MEIO METRO</div>
      <div style={{ position: "absolute", left: 1560, top: 690, width: 340, ...type.bodyMedium, fontSize: 25,
                    color: colors.textDim, ...enter(frame, c2 + 10, 16) }}>
        não dá para sentar; mal dá para virar de lado
      </div>
      <div style={{ position: "absolute", left: 150, top: 176, width: 1620, ...type.display, fontSize: 64,
                    color: colors.text, ...enter(frame, 8, 22) }}>Três beliches empilhados</div>
      <div style={{ position: "absolute", left: 150, top: 980, width: 1620, ...type.bodyMedium, fontSize: 30,
                    color: colors.textDim, ...enter(frame, c3, 18) }}>
        Uma cortina é tudo o que separa esse homem dos outros cento e quarenta e nove.
      </div>
    </Frame>
  );
};

// ---------------- 8. quatro refeições (p063) ----------------
export const A08QuatroRefeicoes: React.FC<SceneProps> = (p) => (
  <Lista
    {...p}
    kicker="A galera serve o dia inteiro"
    titulo="Quatro refeições por dia"
    tint={colors.accent}
    itens={[
      { titulo: "Café da manhã", cue: "quatro refei|quatro" },
      { titulo: "Almoço", cue: "quatro refei|quatro" },
      { titulo: "Jantar", cue: "cozinheiros|galera" },
      { titulo: "Midrats", texto: "A refeição da madrugada, para quem entra ou sai de serviço às três da manhã",
        cue: "midrats|midrat", cor: colors.cool },
    ]}
    nota={{ texto: "Uma cozinha pequena, uma equipe que praticamente não para.", cue: "cozinheiros|galera" }}
  />
);

// ---------------- 9. a familygram (p072) ----------------
export const A09Familygram: React.FC<SceneProps> = (p) => {
  const frame = useCurrentFrame();
  const c1 = cue(p, "familygrams|familygram", 0.16);
  const c2 = cue(p, "dezenas de palavras|palavras", 0.5);
  const c3 = cue(p, "marinha|aprovadas", 0.78);
  return (
    <Frame p={p} kicker="A única janela para casa" tint={colors.cool} grid>
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        <rect x={250} y={330} width={780} height={520} fill={colors.bgElevated} stroke={colors.line}
              strokeWidth={4} opacity={prog(frame, c1, c1 + 22)} />
        {[0, 1, 2, 3, 4, 5].map((i) => (
          <line key={i} x1={310} y1={430 + i * 70} x2={310 + 660 * prog(frame, c2 + i * 6, c2 + 24 + i * 6)}
                y2={430 + i * 70} stroke={colors.textDim} strokeWidth={7} opacity={0.5} />
        ))}
      </svg>
      <div style={{ position: "absolute", left: 1120, top: 350, width: 660, ...type.display, fontSize: 96,
                    color: colors.cool, ...enter(frame, c2, 24) }}>ALGUMAS DEZENAS DE PALAVRAS</div>
      <div style={{ position: "absolute", left: 1120, top: 640, width: 660, ...type.bodyMedium, fontSize: 30,
                    color: colors.text, lineHeight: 1.35, ...enter(frame, c3, 20) }}>
        A família escreve, a Marinha revisa e aprova, e só então a mensagem segue para o submarino.
      </div>
      <div style={{ position: "absolute", left: 150, top: 900, width: 1620, ...type.bodyMedium, fontSize: 30,
                    color: colors.textDim, ...enter(frame, c1, 18) }}>
        O submarino não responde. Ele só recebe.
      </div>
    </Frame>
  );
};

// ---------------- 10. a pressão (p080) ----------------
export const A10Pressao: React.FC<SceneProps> = (p) => (
  <Barras
    {...p}
    kicker="O que o mar cobra por metro"
    titulo="A pressão cresce com a profundidade"
    tint={colors.cool}
    max={25}
    barras={[
      { rotulo: "10 metros", valor: "1 atmosfera", v: 1, cue: "atmosfera|dez metros" },
      { rotulo: "100 metros", valor: "10 atmosferas", v: 10, cue: "atmosfera|dez metros" },
      { rotulo: "Mais de 240 metros", valor: "mais de 24 atmosferas", v: 25, cue: "duzentos e quarenta|duzentos",
        cor: colors.danger },
    ]}
    nota={{ texto: "A profundidade real máxima de um submarino da classe Ohio é segredo militar.",
            cue: "segredo" }}
  />
);

// ---------------- 11. Thresher e Scorpion (p081) ----------------
export const A11Thresher: React.FC<SceneProps> = (p) => (
  <LinhaDoTempo
    {...p}
    kicker="A história não deixa ninguém esquecer"
    tint={colors.danger}
    marcos={[
      { ano: "1963", texto: "O Thresher afunda durante testes no Atlântico. 129 homens.",
        cue: "Thresher|mil novecentos e sessenta e tr.s", cor: colors.danger },
      { ano: "1968", texto: "O Scorpion desaparece a caminho de casa. 99 homens.",
        cue: "Scorpion|noventa e nove", cor: colors.danger },
    ]}
  />
);

// ---------------- 12. o fecho (p093) ----------------
export const A12NoventaDias = painel({
  kicker: "Neste exato momento, em algum lugar do oceano",
  titulo: "Enquanto você assiste a isto",
  linhas: [
    { rotulo: "A bordo", valor: "cento e cinquenta homens", cue: "cento e cinquenta", destaque: true },
    { rotulo: "Há quanto tempo", valor: "semanas sem ver o sol", cue: "noventa|tr.s meses" },
    { rotulo: "Onde", valor: "um ponto do oceano que quase ninguém conhece", cue: "oceano" },
  ],
  nota: "E, em terra, outra tripulação já começou a carregar comida pelas escotilhas.",
  notaCue: "oceano",
  tint: "cool",
});
