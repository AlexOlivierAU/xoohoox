import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { SnackbarProvider } from 'notistack';
import { MainLayout } from './layouts/MainLayout';
import { Dashboard } from './pages/Dashboard';
import { Production } from './pages/Production';
import TestBatchJourney from './pages/TestBatchJourney';
import { TrialDetail } from './pages/TrialDetail';
import { BatchDetails } from './pages/BatchDetails';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#2196f3',
    },
    secondary: {
      main: '#f50057',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <SnackbarProvider maxSnack={3}>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<MainLayout />}>
              <Route index element={<Dashboard />} />
              <Route path="production" element={<Production />} />
              <Route path="test-batch-journey" element={<TestBatchJourney />} />
              <Route path="trials/:id" element={<TrialDetail />} />
              <Route path="batches/:id" element={<BatchDetails />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </SnackbarProvider>
    </ThemeProvider>
  );
}

export default App;
