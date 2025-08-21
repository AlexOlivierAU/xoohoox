import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { FermentationTrialDetails } from '../FermentationTrialDetails';
import '@testing-library/jest-dom';

const mockTrial = {
  trial_id: 'trial-123',
  juice_variant: 'Apple',
  yeast_strain: 'Lalvin EC-1118',
  sg: 1.050,
  current_abv: 6.5,
  path_taken: null,
  status: 'active',
  daily_readings: [
    {
      date: '2024-03-20',
      sg: 1.055,
      abv: 0,
      temperature: 20,
      ph: 3.5,
      notes: 'Initial reading'
    },
    {
      date: '2024-03-21',
      sg: 1.045,
      abv: 2.5,
      temperature: 21,
      ph: 3.4,
      notes: 'Fermentation started'
    }
  ],
  start_date: '2024-03-20',
  target_abv: 12,
  notes: 'Test trial'
};

describe('FermentationTrialDetails', () => {
  const mockOnClose = jest.fn();
  const mockOnPathChange = jest.fn();
  const mockOnAddReading = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders trial details correctly', () => {
    render(
      <FermentationTrialDetails
        trial={mockTrial}
        open={true}
        onClose={mockOnClose}
        onPathChange={mockOnPathChange}
        onAddReading={mockOnAddReading}
      />
    );

    expect(screen.getByText(`Trial Details: ${mockTrial.trial_id}`)).toBeInTheDocument();
    expect(screen.getByText(mockTrial.juice_variant)).toBeInTheDocument();
    expect(screen.getByText(mockTrial.yeast_strain)).toBeInTheDocument();
    expect(screen.getByText('6.5%')).toBeInTheDocument();
  });

  it('handles path change', async () => {
    const user = userEvent.setup();
    render(
      <FermentationTrialDetails
        trial={mockTrial}
        open={true}
        onClose={mockOnClose}
        onPathChange={mockOnPathChange}
        onAddReading={mockOnAddReading}
      />
    );

    const pathSelect = screen.getByLabelText('Current Path');
    await user.click(pathSelect);
    await user.click(screen.getByText('Distillation'));

    expect(mockOnPathChange).toHaveBeenCalledWith(mockTrial.trial_id, 'distillation');
  });

  it('handles adding new reading', async () => {
    const user = userEvent.setup();
    render(
      <FermentationTrialDetails
        trial={mockTrial}
        open={true}
        onClose={mockOnClose}
        onPathChange={mockOnPathChange}
        onAddReading={mockOnAddReading}
      />
    );

    const newReading = {
      sg: 1.040,
      abv: 3.0,
      temperature: 22,
      ph: 3.3,
      notes: 'Test reading'
    };

    // Fill in the form
    await user.type(screen.getByLabelText('SG'), newReading.sg.toString());
    await user.type(screen.getByLabelText('ABV %'), newReading.abv.toString());
    await user.type(screen.getByLabelText('Temperature (°C)'), newReading.temperature.toString());
    await user.type(screen.getByLabelText('pH'), newReading.ph.toString());
    await user.type(screen.getByLabelText('Notes'), newReading.notes);

    // Submit the form
    await user.click(screen.getByText('Add Reading'));

    expect(mockOnAddReading).toHaveBeenCalledWith(mockTrial.trial_id, newReading);
  });

  it('closes dialog when close button is clicked', async () => {
    const user = userEvent.setup();
    render(
      <FermentationTrialDetails
        trial={mockTrial}
        open={true}
        onClose={mockOnClose}
        onPathChange={mockOnPathChange}
        onAddReading={mockOnAddReading}
      />
    );

    const closeButton = screen.getByRole('button', { name: /close dialog/i });
    await user.click(closeButton);

    expect(mockOnClose).toHaveBeenCalled();
  });

  it('returns null when trial is null', () => {
    const { container } = render(
      <FermentationTrialDetails
        trial={null}
        open={true}
        onClose={mockOnClose}
        onPathChange={mockOnPathChange}
        onAddReading={mockOnAddReading}
      />
    );

    expect(container.firstChild).toBeNull();
  });
}); 