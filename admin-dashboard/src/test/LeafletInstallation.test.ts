import { expect, test } from 'vitest';
// @ts-ignore
import L from 'leaflet';
// @ts-ignore
import { MapContainer } from 'react-leaflet';

test('leaflet and react-leaflet are installed', () => {
  expect(L).toBeDefined();
  expect(MapContainer).toBeDefined();
});
