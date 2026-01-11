import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import BranchManagement from './BranchManagement';

// Mock fetch
window.fetch = vi.fn();

describe('BranchManagement', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('fetches and displays branch list', async () => {
    const mockBranches = [
      { id: 1, name: 'Main Branch', address: '123 St', latitude: 10, longitude: 20, radius_meters: 100 }
    ];
    (window.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => mockBranches,
    });

    render(<BranchManagement />);

    expect(screen.getByText(/Branch Management/i)).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText('Main Branch')).toBeInTheDocument();
      expect(screen.getByText('123 St')).toBeInTheDocument();
    });
  });

  it('opens add branch dialog when clicking add button', async () => {
    (window.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => [],
    });

    render(<BranchManagement />);

    const addButton = screen.getByText(/Add Branch/i);
    fireEvent.click(addButton);

    expect(screen.getByText(/Add New Branch/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Address/i)).toBeInTheDocument();
  });

  it('updates form coordinates when confirming map selection', async () => {
    (window.fetch as any).mockResolvedValueOnce({ ok: true, json: async () => [] });
    render(<BranchManagement />);

    fireEvent.click(screen.getByText(/Add Branch/i));
    fireEvent.click(screen.getByText(/Pick from Map/i));

    // Note: We've verified MapPicker interaction in its own unit test.
    // In this integration test, we verify the 'Confirm Location' button
    // correctly applies the temporary state to the main form.
    
    const confirmButton = screen.getByText(/Confirm Location/i);
    fireEvent.click(confirmButton);

    // Default coordinates from Manila default in openDialog
    expect(screen.getByLabelText(/Latitude/i)).toHaveValue(14.5995);
    expect(screen.getByLabelText(/Longitude/i)).toHaveValue(120.9842);
  });
});
