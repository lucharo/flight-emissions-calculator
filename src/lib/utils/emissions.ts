import type { Airport } from "$lib/types";

// Haversine formula to calculate distance between two points
function calculateDistance(lat1: number, lon1: number, lat2: number, lon2: number): number {
  const R = 6371; // Earth's radius in kilometers
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = 
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
    Math.sin(dLon/2) * Math.sin(dLon/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  return R * c;
}

export interface EmissionsResult {
  distance: number;          // in kilometers
  emissions: number;         // in kg CO2
  emissionsPerPerson: number; // in kg CO2
  isReturn: boolean;
}

export function calculateFlightEmissions(
  origin: Airport, 
  destination: Airport, 
  isReturn: boolean = false,
  passengers: number = 1
): EmissionsResult {
  // Calculate distance
  const distance = calculateDistance(
    origin.latitude, 
    origin.longitude, 
    destination.latitude, 
    destination.longitude
  );

  // Emissions factors (kg CO2 per passenger per km)
  // These are simplified averages based on ICAO data
  let emissionsFactor: number;
  if (distance < 500) {
    // Short-haul flights have higher per-km emissions due to takeoff/landing
    emissionsFactor = 0.15;
  } else if (distance < 3000) {
    // Medium-haul flights
    emissionsFactor = 0.12;
  } else {
    // Long-haul flights are most efficient per km
    emissionsFactor = 0.11;
  }

  // Calculate total emissions
  let totalDistance = isReturn ? distance * 2 : distance;
  let totalEmissions = totalDistance * emissionsFactor * passengers;

  return {
    distance: totalDistance,
    emissions: totalEmissions,
    emissionsPerPerson: totalEmissions / passengers,
    isReturn
  };
}
