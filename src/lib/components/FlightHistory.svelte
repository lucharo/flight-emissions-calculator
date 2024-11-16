<script lang="ts">
  import { slide } from 'svelte/transition';
  import type { Airport } from "$lib/types";
  import type { EmissionsResult } from "$lib/utils/emissions";
  import EmissionsResult from "./EmissionsResult.svelte";

  export let isOpen = false;
  
  interface HistoryFlight {
    id: string;
    origin: Airport;
    destination: Airport;
    isReturn: boolean;
    emissions: EmissionsResult;
    timestamp: Date;
  }

  let flightHistory: HistoryFlight[] = [];
  $: totalEmissions = flightHistory.reduce((total, flight) => total + flight.emissions.emissions, 0);

  export function addFlight(origin: Airport, destination: Airport, isReturn: boolean, emissions: EmissionsResult) {
    const flight: HistoryFlight = {
      id: crypto.randomUUID(),
      origin,
      destination,
      isReturn,
      emissions,
      timestamp: new Date()
    };
    flightHistory = [flight, ...flightHistory];
  }

  function removeFlight(id: string) {
    flightHistory = flightHistory.filter(flight => flight.id !== id);
  }

  function clearHistory() {
    flightHistory = [];
  }
</script>

{#if isOpen}
  <!-- Handle -->
  <button
    class="fixed right-[440px] top-1/2 -translate-y-1/2 transform bg-white/90 backdrop-blur-sm p-2 rounded-l-md shadow-lg hover:bg-gray-50 transition-colors z-50"
    on:click={() => isOpen = false}
    aria-label="Close history"
  >
    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 rotate-180" viewBox="0 0 20 20" fill="currentColor">
      <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd" />
    </svg>
  </button>
{/if}

<div
  class="fixed right-0 top-0 h-screen w-full md:w-[400px] bg-white/90 backdrop-blur-sm shadow-lg transform transition-transform duration-300 ease-in-out {isOpen ? 'translate-x-0' : 'translate-x-full'}"
>
  <div class="h-full flex flex-col">
    <div class="flex items-center justify-between p-4 border-b">
      <h2 class="text-lg font-semibold">Flight History</h2>
      <div class="flex items-center gap-2">
        {#if flightHistory.length > 0}
          <button
            class="text-sm text-gray-500 hover:text-gray-700"
            on:click={clearHistory}
          >
            Clear All
          </button>
        {/if}
        <button
          class="text-gray-500 hover:text-gray-700"
          on:click={() => isOpen = false}
          aria-label="Close history"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>

    <div class="flex-1 overflow-auto p-4">
      {#if flightHistory.length === 0}
        <p class="text-center text-gray-500 text-sm">No flights yet</p>
      {:else}
        <div class="space-y-4">
          {#each flightHistory as flight (flight.id)}
            <div class="bg-white rounded-lg shadow p-4">
              <div class="flex justify-between items-start">
                <div class="flex-1">
                  <div class="flex items-center gap-2">
                    <span class="text-sm font-medium">{flight.origin.city}</span>
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                    <span class="text-sm font-medium">{flight.destination.city}</span>
                  </div>
                  <div class="text-xs text-gray-500 mt-1">
                    {flight.origin.iata_code} → {flight.destination.iata_code}
                  </div>
                </div>
                <button
                  class="text-gray-400 hover:text-gray-600"
                  on:click={() => removeFlight(flight.id)}
                  aria-label="Remove flight"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                  </svg>
                </button>
              </div>
              <div class="mt-2 text-sm">
                <span class="text-gray-500">CO₂:</span>
                <span class="font-medium">{flight.emissions.emissions.toFixed(1)} kg</span>
              </div>
            </div>
          {/each}
        </div>
      {/if}
    </div>

    <div class="p-4 border-t bg-gray-50">
      {#if flightHistory.length > 0}
        <div class="flex justify-between items-center">
          <span class="text-sm text-gray-500">Total Emissions:</span>
          <span class="font-semibold">{totalEmissions.toFixed(1)} kg CO₂</span>
        </div>
      {/if}
    </div>
  </div>
</div>

<style>
  /* Custom scrollbar for the flight list */
  .overflow-auto {
    scrollbar-width: thin;
    scrollbar-color: rgba(156, 163, 175, 0.5) transparent;
  }
  
  .overflow-auto::-webkit-scrollbar {
    width: 6px;
  }
  
  .overflow-auto::-webkit-scrollbar-track {
    background: transparent;
  }
  
  .overflow-auto::-webkit-scrollbar-thumb {
    background-color: rgba(156, 163, 175, 0.5);
    border-radius: 3px;
  }
</style>
