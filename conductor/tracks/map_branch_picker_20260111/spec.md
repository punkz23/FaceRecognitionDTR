# Specification: Map-Based Branch Location Picker

## Overview
Currently, administrators must manually type latitude and longitude coordinates when adding or editing branches. This feature introduces an interactive map-based picker using Leaflet to provide a more intuitive and accurate way to manage branch locations and geofences.

## Functional Requirements

### 1. Map Trigger
- Add a "Pick from Map" button next to the Latitude/Longitude coordinate fields in the Branch Management form.
- The button should open a full-screen or large modal containing the interactive map.

### 2. Interactive Map (Leaflet)
- **Map Provider:** Use Leaflet with OpenStreetMap tiles (no API key required).
- **Search Feature:** Include a search bar at the top of the map modal allowing users to search for addresses (using a free geocoding service like Nominatim).
- **Center Crosshair:** A fixed crosshair or "target" indicator should remain in the absolute center of the map view.
- **Geofence Visualization:** 
    - Display a translucent circle centered on the crosshair.
    - The circle's radius must dynamically update based on the numeric value currently entered in the "Radius" field of the branch form.

### 3. Location Selection Logic
- As the user pans and zooms the map, the coordinates corresponding to the center crosshair are tracked.
- **Confirm Selection:** A "Confirm Location" button in the modal will save the current center coordinates back to the form's Latitude and Longitude fields.
- **Initial State:** When opening the modal for an existing branch, the map should center on the current coordinates. If it's a new branch, it should default to a sensible default (e.g., the city center or current user location).

## Non-Functional Requirements
- **Performance:** Ensure the map library is lazy-loaded to keep the initial dashboard bundle small.
- **Usability:** The crosshair interaction should feel smooth and responsive.

## Acceptance Criteria
- [ ] "Pick from Map" button opens the modal.
- [ ] Map renders correctly with a center crosshair.
- [ ] Search bar successfully pans the map to searched locations.
- [ ] Radius circle visualizes the geofence size relative to the map scale.
- [ ] Clicking "Confirm" correctly populates the Latitude and Longitude inputs in the main form.
- [ ] The modal is responsive and works on desktop browsers.

## Out of Scope
- Drawing complex polygon geofences (only circular radii are supported).
- Offline map support.
- Real-time tracking of branch managers on the map.
