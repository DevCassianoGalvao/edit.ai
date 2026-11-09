"""Geração de imagem para agentes, usando a chave e os limites do Estúdio."""
import argparse,base64,sys
from pathlib import Path
root=Path(__file__).resolve().parent.parent
painel=(root.parent.parent/'yt milionario teste'/'painel') if root.parent.name=='baias' else root/'painel'
sys.path.insert(0,str(painel))
import editai
p=argparse.ArgumentParser();p.add_argument('--prompt',required=True);p.add_argument('--estilo',default='');p.add_argument('--canal',default='');p.add_argument('--referencia');a=p.parse_args()
ref=base64.b64encode(Path(a.referencia).read_bytes()).decode() if a.referencia else ''
channel=next((x['id'] for x in editai.profiles() if x['id']==a.canal or x['name']==a.canal),'')
if a.canal and not channel:raise SystemExit('Canal não encontrado.')
r=editai.generate({'prompt':a.prompt,'style':a.estilo,'channel_id':channel,'reference':ref})
print('Imagem salva:',editai.thumb_path(r['id']))
