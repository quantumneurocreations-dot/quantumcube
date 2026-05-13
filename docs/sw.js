const CACHE='qc-v256';
const NARR_CACHE='qc-narration-v3';

self.addEventListener('install', e => {
  e.waitUntil((async () => {
    try{
      const nc = await caches.open(NARR_CACHE);
      const res = await fetch('narration-manifest.json', { cache: 'no-cache' });
      if (res.ok) {
        const rows = await res.json();
        const urls = rows.filter(r => r.filename).map(r => 'Sounds/Narration/' + r.filename);
        urls.push('Sounds/Narration/welcome.mp3');
        for (let i = 0; i < urls.length; i += 8) {
          const batch = urls.slice(i, i + 8);
          await Promise.all(batch.map(u => nc.add(u).catch(()=>{})));
        }
      }
    }catch(err){}
    self.skipWaiting();
  })());
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(ks =>
      Promise.all(
        ks.filter(k => k !== CACHE && k !== NARR_CACHE && (k.startsWith('qc-v') || k.startsWith('qc-narration-')))
          .map(k => caches.delete(k))
      )
    )
  );
  self.clients.claim().then(() => {
    self.clients.matchAll({ type: 'window' }).then(clients => {
      clients.forEach(client => client.postMessage({ type: 'SW_UPDATED' }));
    });
  });
});

self.addEventListener('fetch', e => {
  const u = new URL(e.request.url);

  // Bypass SW entirely for audit tool — always serve fresh
  if (u.pathname.includes('audit-narration')) {
    return;
  }

  if (u.pathname.includes('/Sounds/Narration/')) {
    e.respondWith(
      caches.open(NARR_CACHE).then(c =>
        c.match(e.request).then(r =>
          r || fetch(e.request).then(resp => {
            // Never cache 206 Partial Content — Range requests would store a slice
            // that won't satisfy full-file fetches and can break narration playback.
            if (resp.ok && resp.status !== 206) c.put(e.request, resp.clone());
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
