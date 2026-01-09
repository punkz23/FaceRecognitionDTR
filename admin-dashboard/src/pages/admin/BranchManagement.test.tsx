import { render, screen, waitFor } from '@testing-library/react';
import BranchManagement from './BranchManagement';
import { vi } from 'vitest';

describe('BranchManagement', () => {
  it('fetches and displays branch list', async () => {
    const mockBranches = [
      { id: 1, name: 'Main Office', latitude: 14.5995, longitude: 120.9842, radius_meters: 150 }
    ];

    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockBranches),
    });

    render(<BranchManagement />);

    expect(screen.getByText(/Branch Configuration/i)).toBeInTheDocument();
    
    await waitFor(() => {
      expect(screen.getByText('Main Office')).toBeInTheDocument();
      expect(screen.getByText('14.5995, 120.9842')).toBeInTheDocument();
      expect(screen.getByText('150m')).toBeInTheDocument();
    });
  });
});
