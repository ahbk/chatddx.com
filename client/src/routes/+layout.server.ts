import type { LayoutServerLoad } from './$types';
import { redirect, error } from '@sveltejs/kit';

export const load: LayoutServerLoad = async ({ fetch, cookies }) => {
  const response = await fetch("api/chat/clusters/mock");
  let oai;
  if(response.ok) {
    oai = await response.json();
  } else if (response.status === 401) {
    redirect(307, '/admin/login/?next=/');
  } else {
    error(response.status, response.statusText);
  }

  return { oai };
};
