import React from "react";
import { AbsoluteFill, Audio, Sequence, staticFile } from "remotion";
import timeline from "../data/timeline.json";
import config from "../data/pipeline_config.json";
import { Cut, FadeIn, PhotoCut, VideoCut } from "./stock/StockClip";
import { SCENES } from "./scenes";
import { Sobreposto, type OvSpec } from "./overlays/Sobreposto";

// "music": false no pipeline_config.json = filme SEM trilha (pedido do usuário no filme das 15 máquinas)
const WITH_MUSIC = (config as { music?: boolean }).music !== false;

export type Item =
  | (Cut & { type: "cut"; id: string; fadeIn: number; tail: number; ov?: OvSpec })
  | { type: "animation"; id: string; scene: string; from: number; dur: number; fadeIn: number; tail: number; cues?: Record<string, number> };

// O JSON é gerado para cada produção; a estrutura é validada pelo pipeline antes da montagem.
const items = (timeline as unknown as { items: Item[] }).items;

// Cada item ocupa [from, from+dur). `tail` = quadros extras em que ele continua
// montado por BAIXO do próximo item enquanto este faz fade-in (sem buraco preto).
export const Main: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <Audio src={staticFile("audio.mp3")} />
      {/* trilha já mixada com volume guiado pela fala (scripts/music_mix.py) — só quando o filme tem trilha */}
      {WITH_MUSIC ? <Audio src={staticFile("music.m4a")} /> : null}
      {items.map((it) => {
        const seqDur = it.dur + it.tail;
        if (it.type === "animation") {
          const S = SCENES[it.scene];
          return (
            <Sequence key={it.id} from={it.from} durationInFrames={seqDur} name={it.id}>
              <FadeIn frames={it.fadeIn}>
                <S.C dur={it.dur} t0={it.from} cues={it.cues} />
              </FadeIn>
            </Sequence>
          );
        }
        return (
          <Sequence key={it.id} from={it.from} durationInFrames={seqDur} name={it.id}>
            <FadeIn frames={it.fadeIn}>
              {it.kind === "video" ? <VideoCut cut={{ ...it, dur: seqDur }} /> : <PhotoCut cut={{ ...it, dur: seqDur }} />}
            </FadeIn>
            {/* motion graphic POR CIMA do corte: fica fora do FadeIn para não piscar junto com a imagem */}
            {it.ov ? <Sobreposto ov={it.ov} dur={it.dur} /> : null}
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
