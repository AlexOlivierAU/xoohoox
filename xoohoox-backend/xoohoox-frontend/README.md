# Xoohoox Frontend

## Overview
Xoohoox is a juice production management system that helps track and manage the entire juice production process from batch creation to quality control.

## Tech Stack
- React 18
- TypeScript
- Material-UI v5
- React Router v6
- Vite

## Project Structure
```
src/
├── components/         # Reusable UI components
│   ├── atoms/          # Basic UI elements (buttons, inputs, etc.)
│   ├── molecules/      # Composite components
│   └── organisms/      # Complex components
├── layouts/            # Page layouts
├── pages/              # Application pages
├── routes/             # Routing configuration
├── services/           # API services
├── hooks/              # Custom React hooks
├── utils/              # Utility functions
└── types/              # TypeScript type definitions
```

## UI Components
The application uses a component-based architecture with Material-UI v5:

- **Layout Components**: `MainLayout` provides the application shell with navigation and responsive design
- **Dashboard**: Main overview page with statistics and batch management
- **Form Components**: Reusable form elements for data entry
- **Data Display**: Cards, tables, and charts for data visualization

## Getting Started

### Prerequisites
- Node.js 16+
- npm 7+

### Installation
```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

## Development Guidelines
- Use TypeScript for type safety
- Follow the component structure (atoms, molecules, organisms)
- Use Material-UI components for consistent styling
- Implement responsive design for all components

## Features
- Batch management
- Quality control tracking
- Process monitoring
- User authentication
- Role-based access control

# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default tseslint.config({
  extends: [
    // Remove ...tseslint.configs.recommended and replace with this
    ...tseslint.configs.recommendedTypeChecked,
    // Alternatively, use this for stricter rules
    ...tseslint.configs.strictTypeChecked,
    // Optionally, add this for stylistic rules
    ...tseslint.configs.stylisticTypeChecked,
  ],
  languageOptions: {
    // other options...
    parserOptions: {
      project: ['./tsconfig.node.json', './tsconfig.app.json'],
      tsconfigRootDir: import.meta.dirname,
    },
  },
})
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default tseslint.config({
  plugins: {
    // Add the react-x and react-dom plugins
    'react-x': reactX,
    'react-dom': reactDom,
  },
  rules: {
    // other rules...
    // Enable its recommended typescript rules
    ...reactX.configs['recommended-typescript'].rules,
    ...reactDom.configs.recommended.rules,
  },
})
```
