import { render, screen, waitFor } from '@testing-library/react';
import PayrollReporting from './PayrollReporting';
import { vi } from 'vitest';

describe('PayrollReporting', () => {
  it('fetches and displays payroll summary', async () => {
    const mockPayroll = [
      { id: '1', full_name: 'John Doe', total_hours: 45.5, estimated_pay: 22750 }
    ];

    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockPayroll),
    });

    render(<PayrollReporting />);

    expect(screen.getByText(/Payroll & Reporting/i)).toBeInTheDocument();
    
    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument();
      expect(screen.getByText(/45\.5/)).toBeInTheDocument();
    });

    expect(screen.getByRole('button', { name: /export csv/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /export pdf/i })).toBeInTheDocument();
  });
});
