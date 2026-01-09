import { render, screen, waitFor } from '@testing-library/react';
import EmployeeManagement from './EmployeeManagement';
import { vi } from 'vitest';

describe('EmployeeManagement', () => {
  it('fetches and displays employee list', async () => {
    const mockUsers = [
      { id: '1', full_name: 'Alice Smith', email: 'alice@example.com', status: 'APPROVED', employee_id: 'EMP101' }
    ];

    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockUsers),
    });

    render(<EmployeeManagement />);

    expect(screen.getByText(/Employee Management/i)).toBeInTheDocument();
    
    await waitFor(() => {
      expect(screen.getByText('Alice Smith')).toBeInTheDocument();
      expect(screen.getByText('alice@example.com')).toBeInTheDocument();
    });

    expect(screen.getByRole('button', { name: /edit/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /enroll face/i })).toBeInTheDocument();
  });
});
