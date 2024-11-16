<script lang="ts">
  import type { EmissionsResult } from "$lib/utils/emissions";

  export let result: EmissionsResult;
  export let isReturn: boolean;
  export let title: string = "Flight Emissions";

  // Conversion factors with explanations
  const equivalencies = {
    burger: {
      factor: 3.0, // kg CO2 per burger
      tooltip: "Based on a quarter-pound beef burger, including production and transport emissions. Varies by farming practices and location."
    },
    car: {
      factor: 0.404, // kg CO2 per mile
      tooltip: "Based on average passenger vehicle emissions (EPA data). Actual emissions vary by vehicle type and driving conditions."
    },
    train: {
      factor: 0.041, // kg CO2 per mile
      tooltip: "Based on average passenger train emissions. Varies significantly by country and power source."
    },
    household: {
      factor: (11.5 * 1000) / 365, // kg CO2 per day (11.5 tonnes per year)
      tooltip: "Based on average household emissions in developed countries. Varies significantly by country and lifestyle."
    }
  };

  const kgCO2ToBurgers = (kgCO2: number) => Math.round(kgCO2 / equivalencies.burger.factor);
  const kgCO2ToCarMiles = (kgCO2: number) => Math.round(kgCO2 / equivalencies.car.factor * 1.60934); // Convert to km
  const kgCO2ToTrainMiles = (kgCO2: number) => Math.round(kgCO2 / equivalencies.train.factor * 1.60934); // Convert to km
  const kgCO2ToHouseholdDays = (kgCO2: number) => Math.round(kgCO2 / equivalencies.household.factor);

  let showResults = true;
</script>

{#if showResults}
<div 
  class="bg-white/90 backdrop-blur-sm rounded-lg shadow-lg p-4 w-full md:max-w-md"
>
  <div class="flex items-center justify-between mb-4">
    <h2 class="text-lg font-semibold">{title}</h2>
    <div class="flex items-center gap-2">
      <span class="text-sm text-gray-600">Total CO₂:</span>
      <span class="font-semibold">{result.emissions} kg</span>
    </div>
  </div>

  <div class="space-y-3">
    <p class="text-sm font-medium">This is equivalent to:</p>
    
    <div class="grid gap-2">
      <div class="flex items-center gap-2 text-sm">
        <span class="text-xl">🍔</span>
        <span class="flex-1">{kgCO2ToBurgers(result.emissions)} beef burgers</span>
        <div class="group relative">
          <button
            type="button"
            class="w-4 h-4 text-gray-400 hover:text-gray-600 focus:outline-none"
            aria-label="Show equivalency information"
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
          <div class="invisible group-hover:visible absolute md:bottom-full md:right-0 md:mb-2 md:top-auto -top-2 -right-2 translate-x-full md:translate-x-0 w-64 p-2 bg-gray-900 text-white text-xs rounded shadow-lg z-50">
            {equivalencies.burger.tooltip}
            <div class="absolute md:bottom-[-6px] md:right-[10px] md:top-auto top-[10px] -left-[6px] w-3 h-3 bg-gray-900 md:transform md:rotate-45 rotate-[-45deg]"></div>
          </div>
        </div>
      </div>

      <div class="flex items-center gap-2 text-sm">
        <span class="text-xl">🚗</span>
        <span class="flex-1">{kgCO2ToCarMiles(result.emissions)} km driven by car</span>
        <div class="group relative">
          <button
            type="button"
            class="w-4 h-4 text-gray-400 hover:text-gray-600 focus:outline-none"
            aria-label="Show equivalency information"
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
          <div class="invisible group-hover:visible absolute md:bottom-full md:right-0 md:mb-2 md:top-auto -top-2 -right-2 translate-x-full md:translate-x-0 w-64 p-2 bg-gray-900 text-white text-xs rounded shadow-lg z-50">
            {equivalencies.car.tooltip}
            <div class="absolute md:bottom-[-6px] md:right-[10px] md:top-auto top-[10px] -left-[6px] w-3 h-3 bg-gray-900 md:transform md:rotate-45 rotate-[-45deg]"></div>
          </div>
        </div>
      </div>

      <div class="flex items-center gap-2 text-sm">
        <span class="text-xl">🚂</span>
        <span class="flex-1">{kgCO2ToTrainMiles(result.emissions)} km by train</span>
        <div class="group relative">
          <button
            type="button"
            class="w-4 h-4 text-gray-400 hover:text-gray-600 focus:outline-none"
            aria-label="Show equivalency information"
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
          <div class="invisible group-hover:visible absolute md:bottom-full md:right-0 md:mb-2 md:top-auto -top-2 -right-2 translate-x-full md:translate-x-0 w-64 p-2 bg-gray-900 text-white text-xs rounded shadow-lg z-50">
            {equivalencies.train.tooltip}
            <div class="absolute md:bottom-[-6px] md:right-[10px] md:top-auto top-[10px] -left-[6px] w-3 h-3 bg-gray-900 md:transform md:rotate-45 rotate-[-45deg]"></div>
          </div>
        </div>
      </div>

      <div class="flex items-center gap-2 text-sm">
        <span class="text-xl">🏠</span>
        <span class="flex-1">{kgCO2ToHouseholdDays(result.emissions)} days of average household emissions</span>
        <div class="group relative">
          <button
            type="button"
            class="w-4 h-4 text-gray-400 hover:text-gray-600 focus:outline-none"
            aria-label="Show equivalency information"
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
          <div class="invisible group-hover:visible absolute md:bottom-full md:right-0 md:mb-2 md:top-auto -top-2 -right-2 translate-x-full md:translate-x-0 w-64 p-2 bg-gray-900 text-white text-xs rounded shadow-lg z-50">
            {equivalencies.household.tooltip}
            <div class="absolute md:bottom-[-6px] md:right-[10px] md:top-auto top-[10px] -left-[6px] w-3 h-3 bg-gray-900 md:transform md:rotate-45 rotate-[-45deg]"></div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Mobile pull handle -->
  <div class="h-1.5 w-16 bg-gray-300 rounded-full mx-auto mt-2 md:hidden"></div>
</div>
{/if}

<style>
  /* Ensure tooltips don't get cut off */
  .group {
    overflow: visible;
  }
</style>
