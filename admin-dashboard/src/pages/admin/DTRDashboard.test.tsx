import { render, screen, waitFor } from '@testing-library/react';
import DTRDashboard from './DTRDashboard';
import { vi } from 'vitest';

describe('DTRDashboard', () => {
  it('fetches and displays attendance logs', async () => {
    const mockLogs = [
      { 
        id: '1', 
        user_id: 'u1', 
        full_name: 'John Doe', 
        type: 'TIME_IN', 
        timestamp: '2026-01-09T08:00:00Z',
        location_verified: true,
        confidence_score: 0.95
      }
    ];

    const token = 'fake-token';
    localStorage.setItem('token', token);

    window.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockLogs),
    });

    render(<DTRDashboard />);

    expect(screen.getByText(/Attendance Monitoring/i)).toBeInTheDocument();
    
    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument();
      expect(screen.getByText('TIME_IN')).toBeInTheDocument();
    });

    expect(window.fetch).toHaveBeenCalledWith('/api/v1/attendance/history', {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      }
    });

    expect(screen.getByText(/Verified/i)).toBeInTheDocument();
  });
});
