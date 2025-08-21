import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { CreateTrialForm } from '../CreateTrialForm';
import '@testing-library/jest-dom';

describe('CreateTrialForm', () => {
  const mockOnClose = jest.fn();
  const mockOnSubmit = jest.fn();
  const mockJuiceVariants = ['Apple', 'Pear', 'Grape'];
  const mockYeastStrains = ['Lalvin EC-1118', 'Red Star Premier Blanc', 'SafCider'];

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders form fields correctly', () => {
    render(
      <CreateTrialForm
        open={true}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
        juiceVariants={mockJuiceVariants}
        yeastStrains={mockYeastStrains}
      />
    );

    expect(screen.getByText('Create New Trial')).toBeInTheDocument();
    expect(screen.getByRole('combobox', { name: /juice variant/i })).toBeInTheDocument();
    expect(screen.getByRole('combobox', { name: /yeast strain/i })).toBeInTheDocument();
    expect(screen.getByRole('spinbutton', { name: /target abv/i })).toBeInTheDocument();
    expect(screen.getByRole('spinbutton', { name: /initial sg/i })).toBeInTheDocument();
    expect(screen.getByRole('textbox', { name: /notes/i })).toBeInTheDocument();
  });

  it('displays all juice variants and yeast strains in dropdowns', async () => {
    const user = userEvent.setup();
    render(
      <CreateTrialForm
        open={true}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
        juiceVariants={mockJuiceVariants}
        yeastStrains={mockYeastStrains}
      />
    );

    const juiceSelect = screen.getByRole('combobox', { name: /juice variant/i });
    await user.click(juiceSelect);
    
    mockJuiceVariants.forEach(variant => {
      expect(screen.getByText(variant)).toBeInTheDocument();
    });

    await user.click(screen.getByRole('combobox', { name: /yeast strain/i }));
    mockYeastStrains.forEach(strain => {
      expect(screen.getByText(strain)).toBeInTheDocument();
    });
  });

  it('submits form with correct data', async () => {
    const user = userEvent.setup();
    render(
      <CreateTrialForm
        open={true}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
        juiceVariants={mockJuiceVariants}
        yeastStrains={mockYeastStrains}
      />
    );

    const formData = {
      juice_variant: 'Apple',
      yeast_strain: 'Lalvin EC-1118',
      target_abv: 12,
      initial_sg: 1.050,
      notes: 'Test trial notes',
    };

    // Fill in the form
    await user.click(screen.getByRole('combobox', { name: /juice variant/i }));
    await user.click(screen.getByText(formData.juice_variant));

    await user.click(screen.getByRole('combobox', { name: /yeast strain/i }));
    await user.click(screen.getByText(formData.yeast_strain));

    await user.clear(screen.getByRole('spinbutton', { name: /target abv/i }));
    await user.type(screen.getByRole('spinbutton', { name: /target abv/i }), formData.target_abv.toString());

    await user.clear(screen.getByRole('spinbutton', { name: /initial sg/i }));
    await user.type(screen.getByRole('spinbutton', { name: /initial sg/i }), formData.initial_sg.toString());

    await user.type(screen.getByRole('textbox', { name: /notes/i }), formData.notes);

    // Submit form
    await user.click(screen.getByText('Create Trial'));

    expect(mockOnSubmit).toHaveBeenCalledWith(formData);
    expect(mockOnClose).toHaveBeenCalled();
  });

  it('disables submit button when required fields are empty', async () => {
    const user = userEvent.setup();
    render(
      <CreateTrialForm
        open={true}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
        juiceVariants={mockJuiceVariants}
        yeastStrains={mockYeastStrains}
      />
    );

    const submitButton = screen.getByText('Create Trial');
    expect(submitButton).toBeDisabled();

    // Fill in required fields
    await user.click(screen.getByRole('combobox', { name: /juice variant/i }));
    await user.click(screen.getByText('Apple'));

    // Button should still be disabled
    expect(submitButton).toBeDisabled();

    await user.click(screen.getByRole('combobox', { name: /yeast strain/i }));
    await user.click(screen.getByText('Lalvin EC-1118'));

    // Button should now be enabled
    expect(submitButton).not.toBeDisabled();
  });

  it('closes form when close button is clicked', async () => {
    const user = userEvent.setup();
    render(
      <CreateTrialForm
        open={true}
        onClose={mockOnClose}
        onSubmit={mockOnSubmit}
        juiceVariants={mockJuiceVariants}
        yeastStrains={mockYeastStrains}
      />
    );

    const closeButton = screen.getByRole('button', { name: /close dialog/i });
    await user.click(closeButton);

    expect(mockOnClose).toHaveBeenCalled();
  });
});