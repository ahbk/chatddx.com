<script lang="ts">
  import type { PageData } from './$types';
  import OpenAI from "openai";

  export let data: PageData;

  let client = new OpenAI({
    baseURL: data.oai.base_url,
    apiKey: data.oai.api_key,
    dangerouslyAllowBrowser: true,
    fetch,
  });


  async function run() {
    const stream = await client.chat.completions.create({
      model: 'gpt-4',
      messages: [{ role: "user", content: "Say this is a test" }],
      stream: true,
    });
    console.log(stream);

    for await (const chunk of stream) {
      console.log(chunk);
    }
  }

</script>

<h1 class="text-4xl">
  ChatDDx
  <small class="text-sm">Differentialdiagnostiskt beslutsstöd för läkare</small>
</h1>
<section>
  <label>
    Patientunderlag
    <textarea class="textarea textarea-bordered w-full"></textarea>
  </label>
  <button class="btn btn-primary" on:click={run}>Skapa beslutsstöd</button>
</section>
<section>
  <div role="tablist" class="tabs tabs-lifted">
    <a role="tab" class="tab">
      Diagnoser att utesluta
    </a>
    <a role="tab" class="tab tab-active">
      Undersökningar att planera
    </a>
    <a role="tab" class="tab">
      Komplettera patientunderlag
    </a>
  </div>
  <div class="">

  </div>
</section>
