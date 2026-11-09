import React from "react";
import {AbsoluteFill, interpolate, useCurrentFrame} from "remotion";

type FichaProps = {titulo?: string; valor?: string; detalhe?: string; fonte?: string};
export const FichaEditAI: React.FC<FichaProps> = ({titulo="DADO EM DESTAQUE", valor="", detalhe="", fonte=""}) => {
  const frame = useCurrentFrame();
  const entrada = interpolate(frame, [0, 18], [0, 1], {extrapolateLeft:"clamp", extrapolateRight:"clamp"});
  return <AbsoluteFill style={{background:"linear-gradient(135deg,#0d0b18,#22163e)", color:"#f8f5ff", fontFamily:"Arial, sans-serif", justifyContent:"center", padding:"130px 160px", opacity:entrada}}>
    <div style={{color:"#55e0ce", fontSize:28, letterSpacing:6, fontWeight:700}}>{titulo}</div>
    <div style={{fontSize:148, fontWeight:800, lineHeight:1.05, marginTop:24, overflowWrap:"anywhere"}}>{valor}</div>
    <div style={{width:180, height:7, background:"#a879ff", margin:"36px 0"}} />
    <div style={{fontSize:38, maxWidth:1250, lineHeight:1.3}}>{detalhe}</div>
    {fonte && <div style={{fontSize:22, color:"#bbb0cd", marginTop:55}}>FONTE: {fonte}</div>}
  </AbsoluteFill>;
};
type Evento = {data: string; texto: string};
export const LinhaEditAI: React.FC<{titulo?: string; eventos?: Evento[]}> = ({titulo="LINHA DO TEMPO", eventos=[]}) => {
  const frame=useCurrentFrame();
  return <AbsoluteFill style={{background:"linear-gradient(145deg,#0b1019,#211632)", color:"#f8f5ff", fontFamily:"Arial, sans-serif", padding:"130px 150px"}}>
    <div style={{color:"#64e3d0", letterSpacing:5, fontSize:28, fontWeight:700}}>EDIT.AI • CRONOLOGIA</div>
    <div style={{fontSize:70, fontWeight:800, marginTop:25}}>{titulo}</div>
    <div style={{display:"flex", gap:32, marginTop:100, borderTop:"4px solid #9f75ff"}}>{eventos.slice(0,4).map((e,i)=><div key={i} style={{flex:1, opacity:interpolate(frame,[i*12,i*12+15],[0,1],{extrapolateLeft:"clamp",extrapolateRight:"clamp"}), paddingTop:30}}><div style={{color:"#64e3d0",fontSize:40,fontWeight:700}}>{e.data}</div><div style={{fontSize:32,lineHeight:1.3,marginTop:18}}>{e.texto}</div></div>)}</div>
  </AbsoluteFill>;
};

// Cartão editorial original inspirado em vídeos explicativos, sem marcas de terceiros.
export const EditorialEditAI: React.FC<{titulo?:string; texto?:string; fonte?:string}> = ({titulo="UMA IDEIA EM FOCO",texto="",fonte=""}) => {
  const frame=useCurrentFrame();
  const revelar=interpolate(frame,[0,18],[0,1],{extrapolateLeft:"clamp",extrapolateRight:"clamp"});
  return <AbsoluteFill style={{background:"#f4efdf",color:"#201f24",fontFamily:"Arial, sans-serif",padding:"140px 170px",justifyContent:"center"}}>
    <div style={{position:"absolute",left:0,top:0,bottom:0,width:30,background:"#e6b93c"}} />
    <div style={{fontSize:27,fontWeight:700,letterSpacing:5,color:"#805d00"}}>EXPLICAÇÃO VISUAL</div>
    <div style={{fontSize:86,fontWeight:800,lineHeight:1.08,maxWidth:1500,margin:"28px 0",opacity:revelar}}>{titulo}</div>
    <div style={{width:240*revelar,height:9,background:"#e6b93c",marginBottom:36}} />
    <div style={{fontSize:42,lineHeight:1.35,maxWidth:1320}}>{texto}</div>
    {fonte && <div style={{fontSize:21,color:"#625d50",marginTop:50}}>FONTE: {fonte}</div>}
  </AbsoluteFill>;
};
