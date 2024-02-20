import type { LayoutServerLoad } from './$types';
import { redirect, error } from '@sveltejs/kit';
import { PUBLIC_API_SSR } from '$env/static/public';

export const load: LayoutServerLoad = async ({ fetch, cookies }) => {
  const response = await fetch(`${PUBLIC_API_SSR}/api/chat/clusters/mock`, {
    headers: {
      'Cookie': `sessionid=${cookies.get('sessionid')}`,
    }
  });
  let oai;
  if(response.ok) {
    oai = await response.json();
  } else if (response.status === 401) {
    redirect(307, '/admin/login/?next=/');
  } else {
    console.log(PUBLIC_API_SSR);
    error(response.status, response.statusText);
  }

  return { oai };
};
