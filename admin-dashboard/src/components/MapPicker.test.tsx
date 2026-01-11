import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
// @ts-ignore
import MapPicker from './MapPicker';

describe('MapPicker', () => {
  it('renders the map container', () => {
    const { container } = render(<MapPicker onLocationSelect={() => {}} />);
    // Check if the leaflet container is present
    const mapElement = container.querySelector('.leaflet-container');
    expect(mapElement).not.toBeNull();
  });
});
