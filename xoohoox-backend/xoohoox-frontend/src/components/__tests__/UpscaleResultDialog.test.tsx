import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { UpscaleResultDialog } from '../UpscaleResultDialog';

describe('UpscaleResultDialog', () => {
  const mockProps = {
    open: true,
    onClose: jest.fn(),
    onSubmit: jest.fn(),
    upscaleStage: 'Test 4',
    upscaleVolume: 5,
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders dialog with correct title and fields', () => {
    render(<UpscaleResultDialog {...mockProps} />);
    
    expect(screen.getByText('Record Results for Test 4 (5L)')).toBeInTheDocument();
    expect(screen.getByLabelText(/yield amount/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/abv result/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/compound notes/i)).toBeInTheDocument();
  });

  it('disables submit button when required fields are empty', () => {
    render(<UpscaleResultDialog {...mockProps} />);
    
    const submitButton = screen.getByText('Save Results');
    expect(submitButton).toBeDisabled();
  });

  it('enables submit button when required fields are filled', async () => {
    const user = userEvent.setup();
    render(<UpscaleResultDialog {...mockProps} />);
    
    const yieldInput = screen.getByLabelText(/yield amount/i);
    const abvInput = screen.getByLabelText(/abv result/i);
    
    await user.type(yieldInput, '0.48');
    await user.type(abvInput, '8.0');
    
    const submitButton = screen.getByText('Save Results');
    expect(submitButton).not.toBeDisabled();
  });

  it('submits form with correct data', async () => {
    const user = userEvent.setup();
    render(<UpscaleResultDialog {...mockProps} />);
    
    const yieldInput = screen.getByLabelText(/yield amount/i);
    const abvInput = screen.getByLabelText(/abv result/i);
    const compoundInput = screen.getByLabelText(/compound notes/i);
    
    await user.type(yieldInput, '0.48');
    await user.type(abvInput, '8.0');
    await user.type(compoundInput, 'All compounds within range');
    
    const submitButton = screen.getByText('Save Results');
    await user.click(submitButton);
    
    expect(mockProps.onSubmit).toHaveBeenCalledWith({
      yield_amount: 0.48,
      abv_result: 8.0,
      compound_summary: 'All compounds within range',
    });
  });

  it('calls onClose when cancel button is clicked', async () => {
    const user = userEvent.setup();
    render(<UpscaleResultDialog {...mockProps} />);
    
    const cancelButton = screen.getByText('Cancel');
    await user.click(cancelButton);
    
    expect(mockProps.onClose).toHaveBeenCalled();
  });

  it('validates numeric input ranges', async () => {
    const user = userEvent.setup();
    render(<UpscaleResultDialog {...mockProps} />);
    
    const yieldInput = screen.getByLabelText(/yield amount/i);
    const abvInput = screen.getByLabelText(/abv result/i);
    
    // Yield amount should not accept negative values
    await user.type(yieldInput, '-1');
    expect(yieldInput).toHaveValue(0);
    
    // ABV should not accept values over 100
    await user.type(abvInput, '101');
    expect(abvInput).toHaveValue(0);
  });
}); 