#!/bin/bash

# Create React project with Vite
npm create vite@latest xoohoox-frontend -- --template react-ts

# Navigate to project directory
cd xoohoox-frontend

# Install dependencies
npm install @mui/material @emotion/react @emotion/styled @mui/icons-material
npm install @reduxjs/toolkit react-redux
npm install react-router-dom
npm install axios
npm install date-fns
npm install @tanstack/react-query
npm install @types/node --save-dev
npm install eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin --save-dev
npm install prettier eslint-config-prettier eslint-plugin-prettier --save-dev
npm install @testing-library/react @testing-library/jest-dom vitest --save-dev

# Create project structure
mkdir -p src/{assets,components/{atoms,molecules,organisms},features/{batch,quality,equipment,auth},hooks,layouts,pages,services,store,types,utils}
mkdir -p src/components/{atoms,molecules,organisms}
mkdir -p src/features/{batch,quality,equipment,auth}
mkdir -p tests/{components,features,hooks,utils}

# Create base files
touch src/types/index.ts
touch src/services/api.ts
touch src/store/index.ts
touch src/utils/helpers.ts
touch src/hooks/useAuth.ts
touch src/layouts/MainLayout.tsx
touch src/pages/{Home,Login,Dashboard,BatchList,BatchDetails,QualityChecks,EquipmentMaintenance}.tsx

# Create environment files
echo "VITE_API_URL=http://localhost:8000/api/v1" > .env.development
echo "VITE_API_URL=https://api.xoohoox.com/api/v1" > .env.production

# Create ESLint config
cat > .eslintrc.json << EOL
{
  "env": {
    "browser": true,
    "es2021": true
  },
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:react/recommended",
    "plugin:prettier/recommended"
  ],
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "ecmaFeatures": {
      "jsx": true
    },
    "ecmaVersion": 12,
    "sourceType": "module"
  },
  "plugins": ["react", "@typescript-eslint", "prettier"],
  "rules": {
    "react/react-in-jsx-scope": "off"
  },
  "settings": {
    "react": {
      "version": "detect"
    }
  }
}
EOL

# Create Prettier config
cat > .prettierrc << EOL
{
  "semi": true,
  "tabWidth": 2,
  "printWidth": 100,
  "singleQuote": true,
  "trailingComma": "es5",
  "jsxBracketSameLine": true
}
EOL

# Create Vitest config
cat > vitest.config.ts << EOL
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test/setup.ts'],
  },
});
EOL

# Create test setup file
mkdir -p src/test
cat > src/test/setup.ts << EOL
import '@testing-library/jest-dom';
EOL

# Update package.json scripts
npm pkg set scripts.lint="eslint src --ext .ts,.tsx"
npm pkg set scripts.format="prettier --write \"src/**/*.{ts,tsx}\""
npm pkg set scripts.test="vitest"
npm pkg set scripts.test:coverage="vitest run --coverage"
npm pkg set scripts.build="tsc && vite build"
npm pkg set scripts.preview="vite preview"

# Initialize Git repository
git init
git add .
git commit -m "Initial commit: Project setup with Vite, React, TypeScript, and Material-UI"

echo "Frontend project setup complete! 🎉"
echo "To start development:"
echo "1. cd xoohoox-frontend"
echo "2. npm install"
echo "3. npm run dev" 