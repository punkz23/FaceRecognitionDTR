# Plan: Map-Based Branch Location Picker

This plan outlines the steps to implement an interactive map-based coordinate picker for branch management in the admin dashboard.

## Phase 1: Dependencies & Base Component [checkpoint: d022097]
- [x] Task: Install Leaflet and React-Leaflet (8db2154)
    - [x] Implement Feature: Install `leaflet`, `react-leaflet`, and `@types/leaflet` in the `admin-dashboard` directory.
- [x] Task: Create Map Component Skeleton (9b4cb19)
    - [x] Write Tests: Create a basic test to verify the map component renders in the DOM.
    - [x] Implement Feature: Create a `MapPicker` component that initializes a Leaflet map centered on a default location.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Dependencies & Base Component' (Protocol in workflow.md)

## Phase 2: Picker Modal & Selection Logic [checkpoint: 5acfbe7]
- [x] Task: Implement Map Selection Modal (c1f44e0)
    - [x] Write Tests: Test that clicking the "Pick from Map" button opens the dialog.
    - [x] Implement Feature: Integrate the `MapPicker` into a Shadcn/UI `Dialog`. Add a "Pick from Map" button to the `BranchForm`.
- [x] Task: Implement Center Crosshair & Coordinate Tracking (7f6f430)
    - [x] Write Tests: Verify that panning the map updates the tracked coordinates.
    - [x] Implement Feature: Add a visual crosshair overlay. Use Leaflet's `move` event to track the map's center coordinates and update a "Confirm" button's state.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Picker Modal & Selection Logic' (Protocol in workflow.md)

## Phase 3: Search & Geofence Visualization [checkpoint: d97bced]
- [x] Task: Integrate Nominatim Search (25f7c5c)
    - [x] Write Tests: Mock the Nominatim API and verify that selecting a result pans the map.
    - [x] Implement Feature: Add a search input that queries Nominatim and moves the map to the selected address.
- [x] Task: Add Dynamic Radius Circle (de84270)
    - [x] Write Tests: Verify the circle radius updates when the form's radius value changes.
    - [x] Implement Feature: Render a `L.Circle` centered on the crosshair that reactively scales with the `radius` field from the branch form.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Search & Geofence Visualization' (Protocol in workflow.md)

## Phase 4: Final Integration & UX [checkpoint: 521edbf]
- [x] Task: Finalize Coordinate Hand-back (bc1ca99)
    - [x] Write Tests: Test that clicking "Confirm" in the modal populates the main form's Lat/Long fields.
    - [x] Implement Feature: Connect the modal's "Confirm" action to the form state.
- [x] Task: Conductor - User Manual Verification 'Phase 4: Final Integration & UX' (Protocol in workflow.md) (baed7ca)
