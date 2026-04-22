const CACHE='qc-v136';
const NARR_CACHE='qc-narration-v1';
const ASSETS=['./'];

async function tell(msg){
  try{
    const clients=await self.clients.matchAll({includeUncontrolled:true,type:'window'});
    for(const c of clients) c.postMessage({__swLog:msg});
  }catch(e){}
}

self.addEventListener('install', e => {
  e.waitUntil((async () => {
    try{
      await tell('install:start');
      const c = await caches.open(CACHE);
      await tell('install:cacheOpened');
      await c.addAll(ASSETS);
      await tell('install:assetsAdded');

      const nc = await caches.open(NARR_CACHE);
      await tell('install:narrCacheOpened');

      const res = await fetch('narration-manifest.json', { cache: 'no-cache' });
      await tell('install:manifestFetch:'+res.status);

      if (res.ok) {
        const rows = await res.json();
        await tell('install:rows:'+rows.length);
        const urls = rows.filter(r => r.filename).map(r => 'Sounds/Narration/' + r.filename);
        urls.push('Sounds/Narration/welcome.mp3');
        await tell('install:urls:'+urls.length);

        let ok=0, fail=0;
        for (let i = 0; i < urls.length; i += 8) {
          const batch = urls.slice(i, i + 8);
          const results = await Promise.all(batch.map(u => nc.add(u).then(()=>'ok').catch(e=>'fail:'+e.message)));
          for(const r of results){ if(r==='ok') ok++; else fail++; }
          if(i%40===0) await tell('install:progress:'+ok+'ok/'+fail+'fail');
        }
        await tell('install:done:'+ok+'ok/'+fail+'fail');
      } else {
        await tell('install:manifestFAIL:'+res.status);
      }
    }catch(err){
      await tell('install:EXCEPTION:'+(err&&err.message?err.message:String(err)));
    }
    self.skipWaiting();
  })());
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(ks =>
      Promise.all(
        ks.filter(k => k !== CACHE && k !== NARR_CACHE && k.startsWith('qc-v'))
          .map(k => caches.delete(k))
      )
    )
  );
  self.clients.claim();
});

let _fetchCount=0, _narrFetchCount=0;
self.addEventListener('fetch', e => {
  _fetchCount++;
  const u = new URL(e.request.url);
  if (u.pathname.includes('/Sounds/Narration/')) {
    _narrFetchCount++;
    tell('fetch:narr#'+_narrFetchCount+':'+u.pathname.split('/').pop());
    e.respondWith(
      caches.open(NARR_CACHE).then(c =>
        c.match(e.request).then(r =>
          r || fetch(e.request).then(resp => {
            if (resp.ok) c.put(e.request, resp.clone());
            return resp;
          }).catch(() => new Response('', { status: 504 }))
        )
      )
    );
    return;
  }
  e.respondWith(
    caches.match(e.request).then(r => r || fetch(e.request).catch(() => caches.match('./')))
  );
});
