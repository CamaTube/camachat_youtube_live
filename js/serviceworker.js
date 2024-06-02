// Definizione del nome della cache
var cacheName = 'immagini-precache';

// Installazione del service worker
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(cacheName).then(function(cache) {
      // Non c'è bisogno di pre-caricare le immagini durante l'installazione
      return cache;
    })
  );
});

// Gestione delle richieste di pre-caricamento delle immagini
self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request).then(function(response) {
      // Se la risorsa è presente nella cache, restituiscila
      if (response) {
        return response;
      }

      // Altrimenti, esegui una richiesta di rete per ottenere la risorsa e memorizzarla nella cache
      return fetch(event.request).then(function(networkResponse) {
        return caches.open(cacheName).then(function(cache) {
          cache.put(event.request, networkResponse.clone());
          return networkResponse;
        });
      }).catch(function(error) {
        console.error('Errore durante il pre-caricamento delle immagini:', error);
        throw error;
      });
    })
  );
});
