import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '../../test/utils';
import { Production } from '../Production';

// Mock Material-UI components
vi.mock('@mui/material', () => {
  const actual = vi.importActual('../../test/mocks/mui');
  return actual;
});

// Mock Material-UI icons
vi.mock('@mui/icons-material', () => ({
  Science: () => <span>ScienceIcon</span>,
  Thermostat: () => <span>ThermostatIcon</span>,
  Biotech: () => <span>BiotechIcon</span>,
  LocalDrink: () => <span>LocalDrinkIcon</span>,
}));

describe('Production', () => {
  it('renders the production management title', () => {
    render(<Production />);
    expect(screen.getByText('Production Management')).toBeInTheDocument();
  });

  it('renders all process steps', () => {
    render(<Production />);
    expect(screen.getByText('Raw Material & Chemistry')).toBeInTheDocument();
    expect(screen.getByText('Heat Activation')).toBeInTheDocument();
    expect(screen.getByText('Fermentation')).toBeInTheDocument();
    expect(screen.getByText('Distillation')).toBeInTheDocument();
  });

  it('renders all input fields with initial values', () => {
    render(<Production />);
    expect(screen.getByLabelText('Initial pH')).toHaveValue(1.8);
    expect(screen.getByLabelText('Initial SG')).toHaveValue(1.03);
    expect(screen.getByLabelText('Target pH')).toHaveValue(5.0);
    expect(screen.getByLabelText('Target SG')).toHaveValue(1.07);
  });

  it('renders the fermentation section with current values', () => {
    render(<Production />);
    expect(screen.getByLabelText('Current ABV (%)')).toHaveValue(5.2);
    expect(screen.getByLabelText('Target ABV (%)')).toHaveValue(7.5);
    expect(screen.getByText('Daily Readings')).toBeInTheDocument();
  });

  it('renders the distillation ladder with test data', () => {
    render(<Production />);
    expect(screen.getByText('Current Test: 3')).toBeInTheDocument();
    expect(screen.getByText('Test 3')).toBeInTheDocument();
    expect(screen.getByText('Volume: 1L')).toBeInTheDocument();
    expect(screen.getByText('Expected Yield: 0.1L')).toBeInTheDocument();
  });
}); 