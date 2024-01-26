import type { HandleFetch } from '@sveltejs/kit';
import { PUBLIC_API, PUBLIC_API_SSR } from '$env/static/public';

export const handleFetch: HandleFetch = async ({ event, request, fetch }) => {
  if (request.url.startsWith(PUBLIC_API)) {
    request.headers.set('cookie', event.request.headers.get('cookie') || '');
    request = new Request(request.url.replace(PUBLIC_API, PUBLIC_API_SSR), request);
  }
  return fetch(request);
};
