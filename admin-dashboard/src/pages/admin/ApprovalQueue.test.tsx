import { render, screen, waitFor } from '@testing-library/react';
import ApprovalQueue from './ApprovalQueue';
import { vi } from 'vitest';

describe('ApprovalQueue', () => {
  it('fetches and displays pending users', async () => {
    const mockUsers = [
      { id: '1', full_name: 'John Doe', email: 'john@example.com', status: 'PENDING', employee_id: 'EMP001' }
    ];

    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockUsers),
    });

    render(<ApprovalQueue />);

    expect(screen.getByText(/Pending Registrations/i)).toBeInTheDocument();
    
    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument();
      expect(screen.getByText('john@example.com')).toBeInTheDocument();
    });

    expect(screen.getByRole('button', { name: /approve/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /reject/i })).toBeInTheDocument();
  });
});
