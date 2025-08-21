import React from 'react';

// Mock Material-UI components
export const Box = ({ children, ...props }: any) => <div {...props}>{children}</div>;
export const Paper = ({ children, ...props }: any) => <div {...props}>{children}</div>;
export const Typography = ({ children, ...props }: any) => <div {...props}>{children}</div>;
export const Stepper = ({ children, ...props }: any) => <div {...props}>{children}</div>;
export const Step = ({ children, ...props }: any) => <div {...props}>{children}</div>;
export const StepLabel = ({ children, ...props }: any) => <div {...props}>{children}</div>;
export const Card = ({ children, ...props }: any) => <div {...props}>{children}</div>;
export const CardContent = ({ children, ...props }: any) => <div {...props}>{children}</div>;
export const TextField = ({ label, value, ...props }: any) => (
  <input aria-label={label} defaultValue={value} {...props} />
);
export const Button = ({ children, ...props }: any) => <button {...props}>{children}</button>;
export const Stack = ({ children, ...props }: any) => <div {...props}>{children}</div>;
export const Alert = ({ children, ...props }: any) => <div {...props}>{children}</div>;

// Mock Material-UI icons
export const ScienceIcon = () => <span>ScienceIcon</span>;
export const ThermostatIcon = () => <span>ThermostatIcon</span>;
export const BiotechIcon = () => <span>BiotechIcon</span>;
export const LocalDrinkIcon = () => <span>LocalDrinkIcon</span>; 