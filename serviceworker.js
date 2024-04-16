// Installazione del service worker
self.addEventListener('install', (event) => {
    console.log('Service worker installato');
  });
  
  // Attivazione del service worker
  self.addEventListener('activate', (event) => {
    console.log('Service worker attivato');
  });
  
  // Gestione delle richieste di pre-caricamento
  self.addEventListener('fetch', (event) => {
    // Esegui pre-caricamento solo per le richieste di navigazione
    if (event.request.mode === 'navigate') {
      // Gestisci la richiesta di pre-caricamento
      event.respondWith(
        // Utilizza waitUntil per attendere che la promessa associata alla richiesta di pre-caricamento venga risolta
        caches.open('precache').then((cache) => {
          return cache.match(event.request).then((response) => {
            // Se la risorsa è presente nella cache, restituiscila
            if (response) {
              return response;
            }
  
            // Altrimenti, esegui una richiesta di rete per ottenere la risorsa e memorizzarla nella cache
            return fetch(event.request).then((networkResponse) => {
              cache.put(event.request, networkResponse.clone());
              return networkResponse;
            }).catch((error) => {
              // Gestisci eventuali errori di rete
              console.error('Errore durante il pre-caricamento:', error);
              throw error;
            });
          });
        })
      );
    }
  });
  