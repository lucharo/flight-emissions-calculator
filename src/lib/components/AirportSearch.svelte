<script lang="ts">
  import { Input } from "$lib/components/ui/input";
  import type { Airport } from "$lib/types";
  
  export let label: string;
  export let onSelect: (airport: Airport) => void;
  export let excludeAirport: Airport | null = null;
  
  let airports: Airport[] = [];
  let filteredAirports: Airport[] = [];
  let searchValue = "";
  let showResults = false;
  let loading = false;
  let error: string | null = null;
  let selectedIndex = -1;
  let inputElement: HTMLInputElement;
  let allAirports: Airport[] = [];
  let inputId = `airport-search-${Math.random().toString(36).slice(2, 11)}`;
  const DISPLAY_LIMIT = 50;
  
  async function loadAllAirports() {
    if (allAirports.length > 0) return;
    
    try {
      const response = await fetch('/data/airports.json');
      if (!response.ok) throw new Error('Failed to load airports data');
      allAirports = await response.json();
      // Airports are now pre-sorted by popularity from the Python script
    } catch (err) {
      console.error('Error loading airports:', err);
      error = 'Failed to load airports data';
    }
  }
  
  async function searchAirports(query: string) {
    if (!allAirports.length) {
      loading = true;
      await loadAllAirports();
      loading = false;
    }
    
    const searchLower = query.toLowerCase();
    
    // Filter airports
    filteredAirports = allAirports.filter(airport => 
      (!excludeAirport || airport.iata_code !== excludeAirport.iata_code) &&
      (!query || query.length < 2 || 
        airport.name.toLowerCase().includes(searchLower) ||
        airport.city.toLowerCase().includes(searchLower) ||
        airport.country.toLowerCase().includes(searchLower) ||
        airport.iata_code?.toLowerCase().includes(searchLower))
    );
    
    // Only show first DISPLAY_LIMIT results
    // Results are already sorted by popularity from the Python script
    airports = filteredAirports.slice(0, DISPLAY_LIMIT);
    
    showResults = query.length < 2 || airports.length > 0;
  }
  
  $: if (excludeAirport && searchValue) {
    searchAirports(searchValue);
  }
  
  function handleSelect(airport: Airport) {
    if (excludeAirport && airport.iata_code === excludeAirport.iata_code) {
      error = "Origin and destination cannot be the same";
      return;
    }
    searchValue = `${airport.city} (${airport.iata_code})`;
    showResults = false;
    selectedIndex = -1;
    onSelect(airport);
  }
  
  function handleFocus() {
    if (!searchValue) {
      searchAirports("");
    }
    showResults = true;
  }
  
  function handleBlur() {
    // Delay hiding results to allow for click events
    setTimeout(() => {
      showResults = false;
      selectedIndex = -1;
    }, 200);
  }

  function handleKeydown(event: KeyboardEvent) {
    if (!showResults || airports.length === 0) return;

    switch (event.key) {
      case 'ArrowDown':
        event.preventDefault();
        selectedIndex = (selectedIndex + 1) % airports.length;
        break;
      case 'ArrowUp':
        event.preventDefault();
        selectedIndex = selectedIndex <= 0 ? airports.length - 1 : selectedIndex - 1;
        break;
      case 'Enter':
        event.preventDefault();
        if (selectedIndex >= 0) {
          handleSelect(airports[selectedIndex]);
        } else if (airports.length > 0) {
          // If no item is selected, select the first one
          handleSelect(airports[0]);
        }
        break;
      case 'Escape':
        event.preventDefault();
        showResults = false;
        selectedIndex = -1;
        break;
    }
  }

  function handleHover(index: number) {
    selectedIndex = index;
  }

  function handleClickOutside(event: MouseEvent) {
    const tooltip = document.getElementById('info-tooltip');
    if (tooltip && !tooltip.contains(event.target as Node)) {
      showTooltip = false;
    }
  }

  $: totalAirports = allAirports.length;
  $: filteredCount = filteredAirports.length;
  $: displayCount = airports.length;
</script>

<svelte:window on:click={handleClickOutside} />

<div class="flex flex-col gap-2">
  <label 
    for={inputId}
    class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
  >
    {label}
  </label>
  
  <div class="relative">
    <div class="relative">
      <svg 
        xmlns="http://www.w3.org/2000/svg" 
        viewBox="0 0 24 24" 
        fill="none" 
        stroke="currentColor" 
        stroke-width="2" 
        stroke-linecap="round" 
        stroke-linejoin="round" 
        class="absolute left-3 top-3 h-4 w-4 text-muted-foreground"
      >
        <circle cx="11" cy="11" r="8"/>
        <path d="m21 21-4.3-4.3"/>
      </svg>

      <Input 
        bind:this={inputElement}
        id={inputId}
        type="text"
        bind:value={searchValue}
        on:input={() => searchAirports(searchValue)}
        on:focus={handleFocus}
        on:blur={handleBlur}
        on:keydown={handleKeydown}
        placeholder="Search {totalAirports || '...'} airports..."
        class="pl-9"
        aria-expanded={showResults}
        aria-controls="airport-list"
        aria-activedescendant={selectedIndex >= 0 ? `airport-${selectedIndex}` : undefined}
        role="combobox"
        autocomplete="off"
      />
      {#if loading}
        <div class="absolute right-3 top-3">
          <svg class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>
      {/if}
    </div>
    
    {#if error}
      <div class="text-sm text-red-500 mt-1" role="alert">{error}</div>
    {/if}
    
    {#if showResults && airports.length > 0}
      <div 
        id="airport-list"
        class="absolute w-full mt-1 bg-white rounded-md border shadow-lg max-h-60 overflow-auto z-50"
        role="listbox"
      >
        {#if filteredCount > DISPLAY_LIMIT}
          <div class="px-4 py-2 text-sm text-gray-500 border-b">
            Showing {displayCount} of {filteredCount} matches
          </div>
        {/if}
        {#each airports as airport, i}
          <button
            id="airport-{i}"
            class="w-full px-4 py-2 text-left hover:bg-gray-100 focus:bg-gray-100 focus:outline-none {i === selectedIndex ? 'bg-gray-100' : ''}"
            on:mousedown={() => handleSelect(airport)}
            on:mouseover={() => handleHover(i)}
            on:focus={() => handleHover(i)}
            role="option"
            aria-selected={i === selectedIndex}
          >
            <div class="flex justify-between items-center">
              <span class="font-medium">{airport.city}</span>
              <span class="text-sm text-gray-500">{airport.iata_code}</span>
            </div>
            <div class="text-sm text-gray-500">{airport.name}, {airport.country}</div>
          </button>
        {/each}
      </div>
    {/if}
  </div>
</div>
