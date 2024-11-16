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
  class="fixed right-0 top-0 h-screen w-[440px] bg-white/90 backdrop-blur-sm shadow-lg transform transition-transform duration-300 ease-in-out {isOpen ? 'translate-x-0' : 'translate-x-full'}"
>
  <div class="h-full flex flex-col">
    <!-- Header -->
    <div class="p-4 border-b flex justify-between items-center">
      <h2 class="text-lg font-semibold">Flight History</h2>
      <div class="flex items-center gap-3">
        {#if flightHistory.length > 0}
          <button
            class="text-sm text-red-500 hover:text-red-600"
            on:click={clearHistory}
          >
            Clear All
          </button>
        {/if}
        <button
          class="text-gray-500 hover:text-gray-700 transition-colors"
          on:click={() => isOpen = false}
          aria-label="Close history"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Flight List -->
    <div class="flex-1 overflow-auto p-4">
      {#if flightHistory.length === 0}
        <div class="text-center text-gray-500 mt-8">
          <p>No flight history yet.</p>
          <p class="text-sm mt-2">Add a flight to see it here!</p>
        </div>
      {:else}
        <div class="space-y-4">
          {#each flightHistory as flight (flight.id)}
            <div
              transition:slide
              class="bg-white rounded-lg shadow p-3 relative group"
            >
              <button
                class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity text-gray-400 hover:text-red-500"
                on:click={() => removeFlight(flight.id)}
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </button>
              <div class="text-sm">
                <div class="font-medium">{flight.origin.city} → {flight.destination.city}</div>
                <div class="text-gray-500 text-xs mt-1">
                  {flight.isReturn ? 'Return Flight' : 'One-way Flight'}
                </div>
                <div class="text-gray-500 text-xs">
                  {flight.emissions.emissions.toFixed(1)} kg CO₂
                </div>
                <div class="text-gray-400 text-xs">
                  {flight.timestamp.toLocaleDateString()}
                </div>
              </div>
            </div>
          {/each}
        </div>
      {/if}
    </div>

    <!-- Total Emissions -->
    <div class="border-t p-4">
      {#if flightHistory.length > 0}
        <EmissionsResult
          result={{ emissions: totalEmissions, distance: flightHistory.reduce((total, f) => total + f.emissions.distance, 0) }}
          isReturn={false}
          title="Total History Emissions"
        />
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
