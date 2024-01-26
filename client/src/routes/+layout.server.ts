import type { LayoutServerLoad } from './$types';
import { redirect } from '@sveltejs/kit';

export const load: LayoutServerLoad = async ({ fetch, cookies }) => {
  const response = await fetch("api/");
  if(response.ok) {
    const oai = await response.json();
    console.log(oai);
  } else {
    console.log(response.status);
    console.log(response.statusText);
    redirect(307, '/admin/login/?next=/');
  }
};
