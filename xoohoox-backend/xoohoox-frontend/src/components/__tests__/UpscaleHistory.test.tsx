import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { UpscaleHistory } from '../UpscaleHistory';

const mockUpscales = [
  {
    id: 1,
    upscale_id: 'U-042-03-5L',
    stage: 'Test 4',
    volume: 5,
    yield_amount: 0.48,
    abv_result: 8.0,
    compound_summary: 'All compounds OK',
    status: 'complete' as const,
    timestamp: '2024-04-02T10:00:00Z',
  },
  {
    id: 2,
    upscale_id: 'U-042-03-30L',
    stage: 'Test 5',
    volume: 30,
    yield_amount: null,
    abv_result: null,
    compound_summary: null,
    status: 'pending' as const,
    timestamp: '2024-04-05T10:00:00Z',
  },
];

describe('UpscaleHistory', () => {
  const mockHandlers = {
    onStartUpscale: jest.fn(),
    onRecordYield: jest.fn(),
    onInputCompound: jest.fn(),
    onMarkComplete: jest.fn(),
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders upscale history table with correct headers', () => {
    render(<UpscaleHistory upscales={[]} {...mockHandlers} />);
    
    expect(screen.getByText('Stage')).toBeInTheDocument();
    expect(screen.getByText('Volume')).toBeInTheDocument();
    expect(screen.getByText('Date')).toBeInTheDocument();
    expect(screen.getByText('Yield')).toBeInTheDocument();
    expect(screen.getByText('ABV')).toBeInTheDocument();
    expect(screen.getByText('Compound')).toBeInTheDocument();
  });

  it('displays upscale data correctly', () => {
    render(<UpscaleHistory upscales={mockUpscales} {...mockHandlers} />);
    
    // Test 4 data
    expect(screen.getByText('Test 4')).toBeInTheDocument();
    expect(screen.getByText('5L')).toBeInTheDocument();
    expect(screen.getByText('480mL')).toBeInTheDocument();
    expect(screen.getByText('8.0%')).toBeInTheDocument();
    
    // Test 5 data
    expect(screen.getByText('Test 5')).toBeInTheDocument();
    expect(screen.getByText('30L')).toBeInTheDocument();
    expect(screen.getByText('—')).toBeInTheDocument(); // null yield
  });

  it('shows correct status indicators', () => {
    render(<UpscaleHistory upscales={mockUpscales} {...mockHandlers} />);
    
    // Complete status should show checkmark
    expect(screen.getByTitle('Compounds OK')).toBeInTheDocument();
    
    // Pending status should show pending icon and be clickable
    const pendingButton = screen.getByTitle('Pending');
    expect(pendingButton).toBeInTheDocument();
  });

  it('calls onInputCompound when clicking pending icon', async () => {
    const user = userEvent.setup();
    render(<UpscaleHistory upscales={mockUpscales} {...mockHandlers} />);
    
    const pendingButton = screen.getByTitle('Pending');
    await user.click(pendingButton);
    
    expect(mockHandlers.onInputCompound).toHaveBeenCalledWith(2);
  });

  it('formats measurements correctly', () => {
    const upscaleWithSmallYield = [{
      ...mockUpscales[0],
      yield_amount: 0.048,  // Should show as 48mL
    }];
    
    render(<UpscaleHistory upscales={upscaleWithSmallYield} {...mockHandlers} />);
    expect(screen.getByText('48mL')).toBeInTheDocument();
  });
}); 