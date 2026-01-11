import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
// @ts-ignore
import MapPicker from './MapPicker';

describe('MapPicker', () => {
  it('renders the map container and initial coordinates', () => {
    const { container } = render(<MapPicker onLocationSelect={() => {}} />);
    // Check if the leaflet container is present
    const mapElement = container.querySelector('.leaflet-container');
    expect(mapElement).not.toBeNull();
    
    // Check initial coordinate display
    expect(screen.getByText(/14.599500, 120.984200/)).toBeInTheDocument();
  });
});
