import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import ApprovalQueue from './ApprovalQueue';

// Mock fetch
window.fetch = vi.fn();

describe('ApprovalQueue', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('fetches and displays pending users', async () => {
    const mockUsers = [
      { id: '1', full_name: 'John Doe', email: 'john@example.com', status: 'PENDING', employee_id: 'EMP001' }
    ];
    (window.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => mockUsers,
    });
    // Second call for branches
    (window.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => [],
    });

    render(<ApprovalQueue />);

    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument();
      expect(screen.getByText('john@example.com')).toBeInTheDocument();
    });
  });

  it('opens review modal when clicking review button', async () => {
    const mockUsers = [{ id: '1', full_name: 'John Doe', email: 'john@example.com', status: 'PENDING', employee_id: 'EMP001' }];
    (window.fetch as any).mockResolvedValueOnce({ ok: true, json: async () => mockUsers });
    (window.fetch as any).mockResolvedValueOnce({ ok: true, json: async () => [] });

    render(<ApprovalQueue />);

    await waitFor(() => screen.getByText('John Doe'));
    
    const reviewButton = screen.getByText(/Review & Approve/i);
    fireEvent.click(reviewButton);

    expect(screen.getByText(/Review Employee Registration/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Assigned Branch/i)).toBeInTheDocument();
    expect(screen.getByText(/Approve Employee/i)).toBeInTheDocument();
    expect(screen.getByText(/Disapprove/i)).toBeInTheDocument();
  });
});