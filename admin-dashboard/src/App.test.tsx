import { render, screen } from '@testing-library/react';
import App from './App';

describe('App', () => {
  it('redirects to login by default', () => {
    // Clear token just in case
    localStorage.clear();
    render(<App />);
    // Expect Login Page Title
    expect(screen.getByText(/Admin Login/i)).toBeInTheDocument();
  });
});