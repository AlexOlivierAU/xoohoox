import { Button as MuiButton, ButtonProps as MuiButtonProps } from '@mui/material';
import { styled } from '@mui/material/styles';

export interface ButtonProps extends MuiButtonProps {
  loading?: boolean;
}

const StyledButton = styled(MuiButton)(({ theme }) => ({
  borderRadius: theme.shape.borderRadius,
  textTransform: 'none',
  fontWeight: 600,
  padding: '8px 16px',
  '&.MuiButton-contained': {
    boxShadow: 'none',
    '&:hover': {
      boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.1)',
    },
  },
}));

export const Button = ({ children, loading, ...props }: ButtonProps) => {
  return (
    <StyledButton {...props} disabled={loading || props.disabled}>
      {children}
    </StyledButton>
  );
}; 