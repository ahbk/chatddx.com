<script lang="ts">
  import type { PageData } from './$types';
  import OpenAI from "openai";

  export let data: PageData;

  let client = new OpenAI({
    baseURL: data.oai.diagnoses.endpoint,
    apiKey: data.oai.diagnoses.api_key,
    dangerouslyAllowBrowser: true,
    fetch,
  });

  async function run() {
    let result;
    let messages = data.oai.diagnoses.messages;
    let content = document.getElementById('user-prompt').value.trim();
    let button = document.getElementById('query-button');
    let loading = document.getElementById('query-loading');
    let response = document.getElementById('response');
    response.textContent = "";

    button.disabled = true;
    loading.classList.remove("hidden");

    messages.push({
      content,
      role: "user",
      }
    );
    try {
      result = await client.chat.completions.create({
        messages,
        model: data.oai.diagnoses.model,
        stream: data.oai.diagnoses.stream,
      });
    } catch (error) {
      console.error("Error fetching data from OpenAI:", error.message);
      button.disabled = false;
      loading.classList.add("hidden");
      return;
    }

    if (data.oai.diagnoses.stream) {
      for await (const chunk of result) {
        response.textContent = response.textContent + chunk.choices[0]?.delta?.content || "";
      }
    } else {
      response.textContent = result.choices[0].message.content || "";
    }
    button.disabled = false;
    loading.classList.add("hidden");
  }

</script>

<section class="p-4">
<h1 class="text-4xl">
  ChatDDx
  <small class="text-sm">Differentialdiagnostiskt beslutsstöd för läkare</small>
</h1>
</section>
<section class="p-4">
  <label>
    Patientunderlag
    <textarea id="user-prompt" class="textarea textarea-bordered w-full"></textarea>
  </label>
  <div class="flex py-2">
  <button id="query-button" class="btn btn-primary mr-4" on:click={run}>Generera differentialdiagnoser</button>
  <span id="query-loading" class="loading loading-ball loading-lg hidden"></span>
  </div>
</section>
<section class="p-4">
  <h2 class="text-2xl my-2">Differentialdiagnoser:</h2>
  <pre id="response" class="whitespace-pre-wrap break-words max-w-prose"></pre>
</section>
