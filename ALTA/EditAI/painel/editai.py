"""Edit.AI: perfis, preferências, miniaturas e consulta de acervos."""
import base64, io, json, os, re, threading, time, uuid
from pathlib import Path
import requests

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
ALTA=ROOT.parent
DATA=Path(os.environ.get('EDITAI_DATA_DIR') or HERE/'editai_data')
LOCK=threading.RLock()

def read(name, default):
    p=DATA/name
    return json.loads(p.read_text('utf-8')) if p.exists() else default

def write(name,value):
    DATA.mkdir(parents=True,exist_ok=True); p=DATA/name; t=p.with_suffix('.tmp')
    t.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8');os.replace(t,p)

def profiles():return read('canais.json',[])
def presets():return read('presets.json',[])
def settings():
    return {**{'codex_model':'','claude_model':'','codex_effort':'','image_model':'gpt-image-1.5','image_quality':'medium','estimate_usd':0,'budget_usd':0},**read('settings.json',{})}

def save_profile(b):
    name=str(b.get('name','')).strip()[:100]
    if not name:raise ValueError('Informe o nome do canal.')
    pid=str(b.get('id') or uuid.uuid4().hex[:12])
    if not re.fullmatch('[a-f0-9]{12}',pid):raise ValueError('Identificador de canal inválido.')
    with LOCK:
        a=profiles(); old=next((x for x in a if x['id']==pid),{})
        if any(x['id']!=pid and x['name'].casefold()==name.casefold() for x in a):raise ValueError('Já existe um canal com esse nome.')
        obj={'id':pid,'name':name,'language':str(b.get('language','pt'))[:8], 'memory':str(b.get('memory',''))[:12000], 'thumbnail_style':str(b.get('thumbnail_style',''))[:4000], 'default_preset':str(b.get('default_preset',''))[:100]}
        ref = b.get('reference')
        obj['thumb_config'] = b.get('thumb_config') if isinstance(b.get('thumb_config'),dict) else old.get('thumb_config',{})
        if ref:
            from PIL import Image
            raw=base64.b64decode(ref,validate=True)
            if len(raw)>8_000_000:raise ValueError('Referência maior que 8 MB.')
            im=Image.open(io.BytesIO(raw)); im.verify()
            if im.format not in ('PNG','JPEG','WEBP'):raise ValueError('Use PNG, JPG ou WebP.')
            folder=DATA/'referencias';folder.mkdir(parents=True,exist_ok=True)
            Image.open(io.BytesIO(raw)).convert('RGB').save(folder/(pid+'.png'))
            obj['has_reference']=True
        else: obj['has_reference']=bool(old.get('has_reference') and (DATA/'referencias'/(pid+'.png')).is_file())
        if old:a[a.index(old)]=obj
        else:a.append(obj)
        write('canais.json',a)
    return obj

def save_preset(b):
    name=str(b.get('name','')).strip()[:100]
    if not name:raise ValueError('Informe o nome do preset.')
    channel=str(b.get('channel_id','')); 
    if channel and not any(x['id']==channel for x in profiles()):raise ValueError('Canal não encontrado.')
    payload=b.get('production') or {}
    if not isinstance(payload,dict):raise ValueError('Configuração inválida.')
    pid=str(b.get('id') or uuid.uuid4().hex[:12])
    if not re.fullmatch('[a-f0-9]{12}',pid):raise ValueError('Identificador inválido.')
    obj={'id':pid,'name':name,'channel_id':channel,'production':{k:payload[k] for k in ('idioma','photo_share','modo','formato','estilo','escolhas','liga') if k in payload},'thumbnail_style':str(b.get('thumbnail_style',''))[:4000]}
    with LOCK:
        a=presets();old=next((x for x in a if x['id']==pid),None)
        if old:a[a.index(old)]=obj
        else:a.append(obj)
        write('presets.json',a)
    return obj

def save_settings(b):
    d=settings()
    for k in ('codex_model','claude_model'):
        if k in b:
            v=str(b[k]).strip()
            if v and not re.fullmatch(r'[a-zA-Z0-9._-]{1,80}',v):raise ValueError('Nome de modelo inválido.')
            d[k]=v
    if 'codex_effort' in b:
        if b['codex_effort'] not in ('','low','medium','high','xhigh'):raise ValueError('Esforço inválido.')
        d['codex_effort']=b['codex_effort']
    if 'image_model' in b:
        if b['image_model'] not in ('gpt-image-1.5','gpt-image-1-mini','gpt-image-2'):raise ValueError('Modelo de imagem inválido.')
        d['image_model']=b['image_model']
    if 'image_quality' in b:
        if b['image_quality'] not in ('low','medium','high'):raise ValueError('Qualidade inválida.')
        d['image_quality']=b['image_quality']
    for k in ('estimate_usd','budget_usd'):
        if k in b:
            x=float(b[k]);
            if not 0<=x<=10000:raise ValueError('Valor inválido.')
            d[k]=x
    with LOCK:write('settings.json',d)
    return d

def key():
    p=ALTA/'chaves'/'openai.txt'
    return os.environ.get('OPENAI_API_KEY','').strip() or (p.read_text('utf-8-sig').strip() if p.exists() else '')

def ledger():return read('uso.json',[])

def generate(b):
    import PIL.Image
    secret=key()
    if not secret:raise ValueError('Cadastre a chave OpenAI em Configurações → Chaves.')
    prompt=str(b.get('prompt','')).strip()[:6000]
    if not prompt:raise ValueError('Descreva a imagem.')
    channel=str(b.get('channel_id','')); prof=next((x for x in profiles() if x['id']==channel),None)
    style=str(b.get('style','')).strip()[:3000]
    prompt += '\nEstilo visual: '+style if style else ''
    if prof and prof.get('thumbnail_style'):prompt+='\nIdentidade do canal: '+prof['thumbnail_style']
    prompt+='\nComposição horizontal 16:9 para thumbnail do YouTube. Sem texto, sem letras e sem marcas d’água; deixe espaço para texto editável.'
    ref=b.get('reference') or ''
    if not ref and prof and prof.get('has_reference'):
        ref=base64.b64encode((DATA/'referencias'/(prof['id']+'.png')).read_bytes()).decode()
    if len(ref)>12_000_000:raise ValueError('Referência muito grande (máximo aproximado de 8 MB).')
    data={'model':settings()['image_model'],'prompt':prompt,'size':'1536x1024','quality':settings()['image_quality'],'output_format':'png'}
    headers={'Authorization':'Bearer '+secret}
    with LOCK:
        cfg=settings();events=ledger(); today=time.strftime('%Y-%m-%d'); estimate=float(cfg['estimate_usd']);limit=float(cfg['budget_usd'])
        spent=sum(float(x.get('estimate_usd',0)) for x in events if x.get('date')==today)
        if limit and not estimate:raise ValueError('Defina uma estimativa por imagem para usar o teto diário.')
        if limit and spent+estimate>limit+1e-9:raise ValueError('O teto diário estimado seria ultrapassado.')
        eid=uuid.uuid4().hex; events.append({'id':eid,'date':today,'time':time.strftime('%H:%M:%S'),'kind':'thumbnail','channel_id':channel,'model':data['model'],'estimate_usd':estimate,'status':'iniciada','actual_usd':None});write('uso.json',events)
    try:
        if ref:
            raw=base64.b64decode(ref,validate=True)
            if len(raw)>8_000_000:raise ValueError('Referência maior que 8 MB.')
            im=PIL.Image.open(io.BytesIO(raw));im.verify()
            mime=PIL.Image.MIME.get(im.format)
            if mime not in ('image/png','image/jpeg','image/webp'):raise ValueError('Use PNG, JPG ou WebP.')
            resp=requests.post('https://api.openai.com/v1/images/edits',headers=headers,data=data,files={'image[]':('referencia',raw,mime)},timeout=180)
        else:resp=requests.post('https://api.openai.com/v1/images/generations',headers=headers,json=data,timeout=180)
        if not resp.ok:
            try: msg=resp.json().get('error',{}).get('message','')
            except Exception:msg=''
            raise ValueError(f'OpenAI HTTP {resp.status_code}: {msg[:300]}')
        result=resp.json();raw=base64.b64decode(result['data'][0]['b64_json'],validate=True)
        im=PIL.Image.open(io.BytesIO(raw)).convert('RGB'); im.verify() if False else None
        # Crop to YouTube 16:9 while retaining the generated center.
        w,h=im.size;wanted=w*9/16
        if h>wanted:im=im.crop((0,int((h-wanted)/2),w,int((h+wanted)/2)))
        else:
            ww=h*16/9;im=im.crop((int((w-ww)/2),0,int((w+ww)/2),h))
        im=im.resize((1280,720),PIL.Image.Resampling.LANCZOS)
        folder=DATA/'thumbs';folder.mkdir(parents=True,exist_ok=True);im.save(folder/(eid+'.png'))
        with LOCK:
            events=ledger(); next(x for x in events if x['id']==eid)['status']='concluída';write('uso.json',events)
        return {'id':eid,'url':'/api/editai/thumb?id='+eid,'usage':result.get('usage'),'estimate_usd':estimate,'actual_usd':None}
    except Exception:
        with LOCK:
            events=ledger();next(x for x in events if x['id']==eid)['status']='falhou';write('uso.json',events)
        raise

def thumb_path(id):
    if not re.fullmatch('[a-f0-9]{32}',id or ''):raise ValueError('Miniatura inválida.')
    p=DATA/'thumbs'/(id+'.png')
    if not p.is_file():raise ValueError('Miniatura não encontrada.')
    return p

def sources(source,query):
    q=str(query).strip()[:120]
    if not q:raise ValueError('Informe uma busca.')
    if source=='loc':
        r=requests.get('https://www.loc.gov/search/',params={'q':q,'fo':'json','c':12},headers={'User-Agent':'EditAI/1.0'},timeout=25);r.raise_for_status();return [{'title':x.get('title','Sem título'),'page':x.get('url',''),'thumbnail':(x.get('image_url') or [''])[0],'license':'Consulte os direitos na página do item','source':'Library of Congress'} for x in r.json().get('results',[])]
    if source in ('nasa-video','nasa-image'):
        r=requests.get('https://images-api.nasa.gov/search',params={'q':q,'media_type':('video' if source=='nasa-video' else 'image'),'page_size':12},headers={'User-Agent':'EditAI/1.0'},timeout=25);r.raise_for_status()
        results=[]
        for item in r.json().get('collection',{}).get('items',[]):
            metadata=(item.get('data') or [{}])[0]; ident=metadata.get('nasa_id','');links=item.get('links') or []
            results.append({'title':metadata.get('title','Sem título'),'page':'https://images.nasa.gov/details/'+ident,'thumbnail':links[0].get('href','') if links else '', 'license':'Confira direitos e restrições da NASA','source':'NASA'})
        return results
    if source in ('openverse-image','openverse-audio'):
        kind='images' if source.endswith('image') else 'audio';r=requests.get('https://api.openverse.org/v1/'+kind+'/',params={'q':q,'page_size':12},headers={'User-Agent':'EditAI/1.0'},timeout=25);r.raise_for_status();return [{'title':x.get('title','Sem título'),'page':x.get('foreign_landing_url',''),'thumbnail':x.get('thumbnail',''),'license':x.get('license','Não informada'),'source':x.get('source','Openverse'),'author':x.get('creator','')} for x in r.json().get('results',[])]
    raise ValueError('Fonte não reconhecida.')
