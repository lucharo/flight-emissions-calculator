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

  function calculateEmissions() {
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
</script>

<!-- Map container with fixed position -->
<div class="fixed inset-0 z-0">
  <Map {originCoords} {destCoords} />
</div>

<!-- UI Layer -->
<div class="fixed inset-0 z-10 pointer-events-none">
  <!-- Search Panel -->
  <div class="absolute md:top-4 md:left-4 bottom-0 left-0 right-0 md:relative pointer-events-auto">
    <Card class="w-full md:w-[400px] p-4 bg-white/90 backdrop-blur-sm relative md:rounded-lg rounded-t-lg">
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
          on:click={calculateEmissions}
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

  <!-- Flight History Button -->
  <button
    class="absolute top-4 right-4 md:block pointer-events-auto bg-white/90 backdrop-blur-sm p-2 rounded-lg hover:bg-white/100 transition-colors"
    on:click={toggleHistory}
    aria-label="Toggle flight history"
  >
    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
    </svg>
  </button>

  <!-- Flight History Sidebar -->
  <div
    class="fixed top-0 bottom-0 right-0 w-full md:w-80 bg-white/90 backdrop-blur-sm transform transition-transform duration-300 ease-in-out pointer-events-auto {isHistoryOpen ? 'translate-x-0' : 'translate-x-full'}"
  >
    <FlightHistory bind:this={flightHistoryComponent} bind:isOpen={isHistoryOpen} />
  </div>

  <!-- Current Flight Emissions -->
  {#if showResults && result && !isHistoryOpen}
    <div class="absolute bottom-4 right-6 pointer-events-auto">
      <EmissionsResult {result} {isReturn} title="Current Flight" />
    </div>
  {/if}
</div>

<style>
  :global(html) {
    overflow: hidden;
  }
</style>
