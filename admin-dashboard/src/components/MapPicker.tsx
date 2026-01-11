import { MapContainer, TileLayer, useMapEvents } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { useState } from 'react';
import L from 'leaflet';

// Fix for default marker icons in Leaflet with React
// @ts-ignore
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
});

interface MapPickerProps {
  initialCenter?: [number, number];
  initialZoom?: number;
  onLocationSelect: (lat: number, lng: number) => void;
}

export function MapEvents({ onMove }: { onMove: (lat: number, lng: number) => void }) {
  useMapEvents({
    move: (e) => {
      const center = e.target.getCenter();
      onMove(center.lat, center.lng);
    },
  });
  return null;
}

export default function MapPicker({
  initialCenter = [14.5995, 120.9842], // Manila
  initialZoom = 13,
  onLocationSelect,
}: MapPickerProps) {
  const [center, setCenter] = useState<{ lat: number; lng: number }>({
    lat: initialCenter[0],
    lng: initialCenter[1],
  });

  const handleMove = (lat: number, lng: number) => {
    setCenter({ lat, lng });
    onLocationSelect(lat, lng);
  };

  return (
    <div className="relative w-full h-[400px] border rounded-md overflow-hidden" role="presentation">
      <MapContainer
        center={initialCenter}
        zoom={initialZoom}
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <MapEvents onMove={handleMove} />
      </MapContainer>
      
      {/* Visual Crosshair Overlay */}
      <div className="absolute inset-0 pointer-events-none flex items-center justify-center z-[1000]">
        <div className="relative w-8 h-8 flex items-center justify-center">
          <div className="absolute w-full h-0.5 bg-red-500"></div>
          <div className="absolute h-full w-0.5 bg-red-500"></div>
          <div className="w-2 h-2 rounded-full border-2 border-red-500 bg-white"></div>
        </div>
      </div>
      
      {/* Coordinate Display */}
      <div className="absolute bottom-4 left-4 z-[1000] bg-white/90 px-2 py-1 rounded shadow-sm text-xs font-mono border">
        {center.lat.toFixed(6)}, {center.lng.toFixed(6)}
      </div>
    </div>
  );
}
