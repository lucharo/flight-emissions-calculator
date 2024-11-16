<script lang="ts">
  import { Card } from "$lib/components/ui/card";
  import Map from "$lib/components/Map.svelte";
  import AirportSearch from "$lib/components/AirportSearch.svelte";
  import EmissionsResult from "$lib/components/EmissionsResult.svelte";
  import FlightHistory from "$lib/components/FlightHistory.svelte";
  import type { Airport } from "$lib/types";
  import { calculateFlightEmissions } from "$lib/utils/emissions";
  import type { EmissionsResult as EmissionsResultType } from "$lib/utils/emissions";

  let originCoords: [number, number] | null = null;
  let destCoords: [number, number] | null = null;
  let selectedOrigin: Airport | null = null;
  let selectedDest: Airport | null = null;
  let isReturn = false;
  let loading = false;
  let error: string | null = null;
  let result: EmissionsResultType | null = null;
  let showResults = false;
  let isHistoryOpen = false;
  let flightHistoryComponent: FlightHistory;
  let showInfoIcon = true;
  let showTooltip = false;
  let isMobileWarningVisible = false;

  function handleOriginSelect(airport: Airport) {
    error = null;
    selectedOrigin = airport;
    originCoords = [airport.latitude, airport.longitude];
  }

  function handleDestSelect(airport: Airport) {
    error = null;
    selectedDest = airport;
    destCoords = [airport.latitude, airport.longitude];
  }

  function calculateResult() {
    if (!selectedOrigin || !selectedDest) {
      error = "Please select both origin and destination airports";
      return;
    }

    if (selectedOrigin === selectedDest) {
      error = "Origin and destination cannot be the same";
      return;
    }

    error = null;
    loading = true;

    try {
      result = calculateFlightEmissions(selectedOrigin, selectedDest, isReturn);
      showResults = true;
      if (result) {
        flightHistoryComponent?.addFlight(selectedOrigin, selectedDest, isReturn, result);
      }
    } catch (e) {
      error = "Error calculating emissions. Please try again.";
      console.error(e);
    } finally {
      loading = false;
    }
  }

  function toggleHistory() {
    isHistoryOpen = !isHistoryOpen;
  }

  function toggleTooltip() {
    showTooltip = !showTooltip;
  }

  // Check screen width on mount and when resized
  function checkScreenSize() {
    isMobileWarningVisible = window.innerWidth < 768;
  }
</script>

<svelte:window on:resize={checkScreenSize}/>

{#if isMobileWarningVisible}
  <div class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
    <div class="bg-white rounded-lg p-6 max-w-md text-center">
      <h2 class="text-xl font-bold mb-4">📱 Mobile Device Detected</h2>
      <p class="mb-4">
        This application is optimized for larger screens. For the best experience, please access it on a desktop or tablet device.
      </p>
      <button
        class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        on:click={() => isMobileWarningVisible = false}
      >
        Continue Anyway
      </button>
    </div>
  </div>
{/if}

<!-- Map container with fixed position -->
<div class="fixed inset-0 z-0">
  <Map {originCoords} {destCoords} />
</div>

<!-- UI Layer -->
<div class="fixed inset-0 z-10 pointer-events-none">
  <!-- Search Panel -->
  <div class="absolute top-4 left-4 pointer-events-auto">
    <Card class="w-[400px] p-4 bg-white/90 backdrop-blur-sm relative">
      {#if showInfoIcon}
        <button
          type="button"
          on:click={toggleTooltip}
          class="absolute right-4 top-4 w-4 h-4 text-gray-400 hover:text-gray-600 focus:outline-none z-10"
          aria-label="Show airport data information"
        >
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            stroke-width="2" 
            stroke-linecap="round" 
            stroke-linejoin="round" 
            class="w-4 h-4"
          >
            <circle cx="12" cy="12" r="10"/>
            <path d="M12 16v-4"/>
            <path d="M12 8h.01"/>
          </svg>
        </button>
        
        {#if showTooltip}
          <div
            id="info-tooltip"
            class="absolute right-0 top-0 mt-12 w-80 p-4 bg-gray-900 text-white text-sm rounded shadow-lg z-50"
            role="dialog"
            aria-label="Airport data information"
          >
            <div class="flex justify-between items-start mb-2">
              <h3 class="font-medium">Airport Data Sources</h3>
              <button
                type="button"
                class="text-gray-400 hover:text-white"
                on:click={toggleTooltip}
                aria-label="Close information"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </button>
            </div>
            <p class="mb-2">
              Airport data compiled from:
            </p>
            <ul class="list-disc list-inside space-y-1 mb-2">
              <li>
                <a 
                  href="https://github.com/jpatokal/openflights/tree/master/data" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  class="text-blue-300 hover:text-blue-200 underline"
                >
                  OpenFlights Database
                </a>
              </li>
              <li>
                <a 
                  href="https://github.com/davidmegginson/ourairports-data" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  class="text-blue-300 hover:text-blue-200 underline"
                >
                  OurAirports Data
                </a>
              </li>
              <li>
                <a 
                  href="https://aci.aero/2020/05/19/aci-world-releases-2019-world-airport-traffic-report/" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  class="text-blue-300 hover:text-blue-200 underline"
                >
                  ACI Traffic Report 2019
                </a>
              </li>
            </ul>
            <p class="text-xs text-gray-400">
              Airports are ranked by importance using traffic data and other factors like international status and city significance.
            </p>
          </div>
        {/if}
      {/if}

      <div class="space-y-4">
        <AirportSearch 
          label="Origin Airport" 
          onSelect={handleOriginSelect}
          excludeAirport={selectedDest}
        />
        <AirportSearch 
          label="Destination Airport" 
          onSelect={handleDestSelect}
          excludeAirport={selectedOrigin}
        />

        <div class="flex items-center gap-2">
          <input
            type="checkbox"
            id="return"
            bind:checked={isReturn}
            class="h-4 w-4 rounded border border-input"
          />
          <label for="return" class="text-sm font-medium">Return flight</label>
        </div>

        {#if error}
          <div class="text-sm text-red-500">{error}</div>
        {/if}

        <button
          class="w-full px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors"
          on:click={calculateResult}
          disabled={loading}
        >
          {#if loading}
            Calculating...
          {:else}
            Calculate Emissions
          {/if}
        </button>
      </div>
    </Card>
  </div>

  <!-- History Toggle Button -->
  <button
    class="absolute top-4 right-4 p-2 bg-white/90 backdrop-blur-sm rounded-md shadow-lg pointer-events-auto hover:bg-gray-50 transition-colors"
    on:click={toggleHistory}
  >
    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  </button>

  <!-- Flight History Sidebar -->
  <div class="pointer-events-auto">
    <FlightHistory bind:this={flightHistoryComponent} bind:isOpen={isHistoryOpen} />
  </div>

  <!-- Current Flight Emissions -->
  {#if showResults && result && !isHistoryOpen}
    <div class="absolute bottom-4 right-6 pointer-events-auto">
      <EmissionsResult {result} {isReturn} title="Current Flight" />
    </div>
  {/if}
</div>

<!-- GitHub Link -->
<a
  href="https://github.com/lucharo/flight-emissions-calculator"
  target="_blank"
  rel="noopener noreferrer"
  class="fixed bottom-4 left-4 z-20 bg-gray-900 text-white px-2 py-2 rounded-full flex items-center gap-2 hover:bg-gray-800 transition-colors"
>
  <svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
    <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
  </svg>
</a>
