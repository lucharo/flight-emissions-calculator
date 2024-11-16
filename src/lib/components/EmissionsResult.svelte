<script lang="ts">
  import type { EmissionsResult } from "$lib/utils/emissions";

  export let result: EmissionsResult;
  export let isReturn: boolean;
  export let title: string = "Flight Emissions";

  // Conversion factors with explanations
  const equivalencies = {
    burger: {
      factor: 3.43, // kg CO2e per quarter-pound beef burger
      tooltip:
        "University of Michigan CSS (2024): Beef production emits 30.4 kg CO2e per kg. A quarter-pound burger (~113g) results in 3.43 kg CO2e. Source: <a href='https://css.umich.edu/sites/default/files/2024-10/Carbon%20Footprint_CSS09-05.pdf' target='_blank' rel='noopener noreferrer' class='text-blue-300 hover:text-blue-200 underline'>CSS Factsheet</a>",
    },
    car: {
      factor: 0.335, // kg CO2 per mile (converted from 0.74 lbs CO2 per mile)
      tooltip:
        "University of Michigan CSS (2024): The average passenger car emitted 0.74 lbs of CO2 per mile driven in 2022. Source: <a href='https://css.umich.edu/sites/default/files/2024-10/Carbon%20Footprint_CSS09-05.pdf' target='_blank' rel='noopener noreferrer' class='text-blue-300 hover:text-blue-200 underline'>CSS Factsheet</a>",
    },
    train: {
      factor: 0.0217, // kg CO2 per mile (converted from 35g CO2e per passenger kilometer)
      tooltip:
        "Our World in Data (2023): National rail emits around 35 grams of CO2e per passenger kilometer. Source: <a href='https://ourworldindata.org/travel-carbon-footprint' target='_blank' rel='noopener noreferrer' class='text-blue-300 hover:text-blue-200 underline'>Our World in Data</a>",
    },
    household: {
      factor: 4000 / 365, // kg CO2e per day (4 tonnes per year)
      tooltip:
        "University of Michigan CSS (2024): A typical U.S. household has a carbon footprint of 4 t CO2e/yr. Source: <a href='https://css.umich.edu/sites/default/files/2024-10/Carbon%20Footprint_CSS09-05.pdf' target='_blank' rel='noopener noreferrer' class='text-blue-300 hover:text-blue-200 underline'>CSS Factsheet</a>",
    },
  };

  const kgCO2ToBurgers = (kgCO2: number) =>
    Math.round(kgCO2 / equivalencies.burger.factor);
  const kgCO2ToCarMiles = (kgCO2: number) =>
    Math.round((kgCO2 / equivalencies.car.factor) * 1.60934); // Convert to km
  const kgCO2ToTrainMiles = (kgCO2: number) =>
    Math.round((kgCO2 / equivalencies.train.factor) * 1.60934); // Convert to km
  const kgCO2ToHouseholdDays = (kgCO2: number) =>
    Math.round(kgCO2 / equivalencies.household.factor);

  let showResults = true;
</script>

{#if showResults}
  <div
    class="w-[400px] bg-white/90 backdrop-blur-sm rounded-lg border border-border p-4 shadow-lg"
  >
    <div class="flex justify-between items-start mb-4">
      <div>
        <h3 class="text-lg font-semibold">{title}</h3>
        <p class="text-sm text-muted-foreground">
          {#if isReturn}
            Return Flight
          {:else}
            One-way Flight
          {/if}
        </p>
      </div>
      <button
        class="text-muted-foreground hover:text-foreground"
        on:click={() => (showResults = false)}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="h-4 w-4"
        >
          <path d="M18 6L6 18" />
          <path d="M6 6l12 12" />
        </svg>
      </button>
    </div>

    <div class="space-y-4">
      <div class="grid grid-cols-2 gap-4">
        <div class="text-sm">
          <span class="text-muted-foreground">Distance:</span>
          <span class="font-medium ml-1">{Math.round(result.distance)} km</span>
        </div>

        <div class="text-sm">
          <span class="text-muted-foreground">Total CO₂:</span>
          <span class="font-medium ml-1">{Math.round(result.emissions)} kg</span
          >
        </div>
      </div>

      <div class="space-y-3">
        <p class="text-sm font-medium">This is equivalent to:</p>

        <div class="grid gap-2">
          <div class="flex items-center gap-2 text-sm">
            <span class="text-xl">🍔</span>
            <span>{kgCO2ToBurgers(result.emissions)} beef burgers</span>
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
                  <circle cx="12" cy="12" r="10" />
                  <path d="M12 16v-4" />
                  <path d="M12 8h.01" />
                </svg>
              </button>
              <div
                class="invisible group-hover:visible absolute bottom-full right-0 mb-2 w-64 p-2 bg-gray-900 text-white text-xs rounded shadow-lg z-50"
              >
                {@html equivalencies.burger.tooltip}
                <div
                  class="absolute bottom-[-6px] right-[10px] w-3 h-3 bg-gray-900 transform rotate-45"
                ></div>
              </div>
            </div>
          </div>

          <div class="flex items-center gap-2 text-sm">
            <span class="text-xl">🚗</span>
            <span>{kgCO2ToCarMiles(result.emissions)} km driven by car</span>
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
                  <circle cx="12" cy="12" r="10" />
                  <path d="M12 16v-4" />
                  <path d="M12 8h.01" />
                </svg>
              </button>
              <div
                class="invisible group-hover:visible absolute bottom-full right-0 mb-2 w-64 p-2 bg-gray-900 text-white text-xs rounded shadow-lg z-50"
              >
                {@html equivalencies.car.tooltip}
                <div
                  class="absolute bottom-[-6px] right-[10px] w-3 h-3 bg-gray-900 transform rotate-45"
                ></div>
              </div>
            </div>
          </div>

          <div class="flex items-center gap-2 text-sm">
            <span class="text-xl">🚂</span>
            <span>{kgCO2ToTrainMiles(result.emissions)} km by train</span>
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
                  <circle cx="12" cy="12" r="10" />
                  <path d="M12 16v-4" />
                  <path d="M12 8h.01" />
                </svg>
              </button>
              <div
                class="invisible group-hover:visible absolute bottom-full right-0 mb-2 w-64 p-2 bg-gray-900 text-white text-xs rounded shadow-lg z-50"
              >
                {@html equivalencies.train.tooltip}
                <div
                  class="absolute bottom-[-6px] right-[10px] w-3 h-3 bg-gray-900 transform rotate-45"
                ></div>
              </div>
            </div>
          </div>

          <div class="flex items-center gap-2 text-sm">
            <span class="text-xl">🏠</span>
            <span
              >{kgCO2ToHouseholdDays(result.emissions)} days of average household
              emissions</span
            >
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
                  <circle cx="12" cy="12" r="10" />
                  <path d="M12 16v-4" />
                  <path d="M12 8h.01" />
                </svg>
              </button>
              <div
                class="invisible group-hover:visible absolute bottom-full right-0 mb-2 w-64 p-2 bg-gray-900 text-white text-xs rounded shadow-lg z-50"
              >
                {@html equivalencies.household.tooltip}
                <div
                  class="absolute bottom-[-6px] right-[10px] w-3 h-3 bg-gray-900 transform rotate-45"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="space-y-2 text-xs text-muted-foreground mt-4">
        <p>
          Aviation accounts for approximately 2.5% of global CO₂ emissions (<a
            href="https://doi.org/10.1007/s44168-022-00001-w"
            target="_blank"
            rel="noopener noreferrer"
            class="text-blue-500 hover:text-blue-600 underline"
            >Dolšak & Prakash, 2022</a
          >).
        </p>
        <p>
          Only about 11% of the global population takes a flight each year
          <a
            href="https://www.sciencedirect.com/science/article/pii/S0959378020307779"
            target="_blank"
            rel="noopener noreferrer"
            class="text-blue-500 hover:text-blue-600 underline"
            >(Gössling & Humpe, 2020)</a
          >.
        </p>
        <p>
          The average person's annual carbon budget for 1.5°C warming is 2.3
          tonnes of CO₂
          <a
            href="https://www.nature.com/articles/s41558-020-0797-x"
            target="_blank"
            rel="noopener noreferrer"
            class="text-blue-500 hover:text-blue-600 underline"
            >(Akenji et al., 2021)</a
          >.
        </p>
      </div>
    </div>
  </div>
{/if}

<style>
  /* Ensure tooltips don't get cut off */
  .group {
    overflow: visible;
  }
</style>
