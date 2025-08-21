import { TextField as MuiTextField, TextFieldProps as MuiTextFieldProps } from '@mui/material';
import { styled } from '@mui/material/styles';

type TextFieldProps = MuiTextFieldProps & {
  error?: boolean;
  helperText?: string;
};

const StyledTextField = styled(MuiTextField)(({ theme }) => ({
  '& .MuiOutlinedInput-root': {
    borderRadius: theme.shape.borderRadius,
    '&:hover fieldset': {
      borderColor: theme.palette.primary.main,
    },
  },
  '& .MuiInputLabel-root': {
    '&.Mui-focused': {
      color: theme.palette.primary.main,
    },
  },
}));

export const TextField = ({ error, helperText, ...props }: TextFieldProps) => {
  return (
    <StyledTextField
      {...props}
      error={error}
      helperText={helperText}
      variant="outlined"
      fullWidth
    />
  );
}; 