import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import ApprovalQueue from './ApprovalQueue';

// Mock fetch
global.fetch = vi.fn();

describe('ApprovalQueue', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('fetches and displays pending users', async () => {
    const mockUsers = [
      { id: '1', full_name: 'John Doe', email: 'john@example.com', status: 'PENDING', employee_id: 'EMP001' }
    ];
    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => mockUsers,
    });
    // Second call for branches
    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => [],
    });

    render(<ApprovalQueue />);

    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument();
      expect(screen.getByText('john@example.com')).toBeInTheDocument();
    });
  });

  it('opens approval modal when clicking approve button', async () => {
    const mockUsers = [{ id: '1', full_name: 'John Doe', email: 'john@example.com', status: 'PENDING', employee_id: 'EMP001' }];
    (global.fetch as any).mockResolvedValueOnce({ ok: true, json: async () => mockUsers });
    (global.fetch as any).mockResolvedValueOnce({ ok: true, json: async () => [] });

    render(<ApprovalQueue />);

    await waitFor(() => screen.getByText('John Doe'));
    
    const approveButton = screen.getByText(/Review & Approve/i);
    fireEvent.click(approveButton);

    expect(screen.getByText(/Approve Registration/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Assign Branch/i)).toBeInTheDocument();
  });

  it('opens rejection modal when clicking reject button', async () => {
    const mockUsers = [{ id: '1', full_name: 'John Doe', email: 'john@example.com', status: 'PENDING', employee_id: 'EMP001' }];
    (global.fetch as any).mockResolvedValueOnce({ ok: true, json: async () => mockUsers });
    (global.fetch as any).mockResolvedValueOnce({ ok: true, json: async () => [] });

    render(<ApprovalQueue />);

    await waitFor(() => screen.getByText('John Doe'));
    
    const rejectButton = screen.getByLabelText(/Reject/i);
    fireEvent.click(rejectButton);

    expect(screen.getAllByText(/Reject Registration/i)[0]).toBeInTheDocument();
    expect(screen.getByLabelText(/Rejection Reason/i)).toBeInTheDocument();
  });
});