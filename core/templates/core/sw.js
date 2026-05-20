const CACHE_NAME = 'scifiverse-v1';

// Evento di installazione
self.addEventListener('install', (event) => {
    console.log('[Service Worker] Installato');
    self.skipWaiting();
});

// Evento di attivazione
self.addEventListener('activate', (event) => {
    console.log('[Service Worker] Attivato');
    event.waitUntil(clients.claim());
});

// Strategia Network First (Cerca sempre la rete, se fallisce gestisce l'errore)
self.addEventListener('fetch', (event) => {
    event.respondWith(
        fetch(event.request).catch(() => {
            return new Response("Sei offline. Connettiti a internet per esplorare Scifiverse.");
        })
    );
});