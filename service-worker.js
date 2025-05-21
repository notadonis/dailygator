const CACHE_NAME = 'daily-gator-v1';
const urlsToCache = [
  '/dailygator/',
  '/dailygator/index.html',
  '/dailygator/manifest.json',
  '/dailygator/logo.png',
  '/dailygator/icons/icon-192x192.png',
  '/dailygator/icons/icon-512x512.png'
];

// Install service worker and cache assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
  );
});

// Serve cached content when offline
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Cache hit - return response
        if (response) {
          return response;
        }

        // Clone the request
        const fetchRequest = event.request.clone();
        
        // For JSON data requests (our news feed)
        if (fetchRequest.url.includes('florida_man_stories.json')) {
          return fetch(fetchRequest).then(
            response => {
              // Check if we received a valid response
              if (!response || response.status !== 200 || response.type !== 'basic') {
                return response;
              }

              // Clone the response
              const responseToCache = response.clone();

              caches.open(CACHE_NAME)
                .then(cache => {
                  cache.put(event.request, responseToCache);
                });

              return response;
            }
          ).catch(() => {
            // If the network request fails, return the cached version
            return caches.match(event.request);
          });
        }

        // For all other requests, try the network first
        return fetch(fetchRequest).catch(() => {
          // If offline and no cache, serve index.html for navigation requests
          if (event.request.mode === 'navigate') {
            return caches.match('/dailygator/index.html');
          }
        });
      })
  );
});

// Update caches and delete old versions
self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
