import React from 'react';
import { Box, Typography, Container, Paper } from '@mui/material';
import BatchJourneyTimeline from '../components/BatchJourneyTimeline';

// Import the Stage type from the component
type Stage = 'arrival' | 'prep' | 'heat' | 'ferment' | 'distill';

const TestBatchJourney: React.FC = () => {
  // Mock data for testing
  const mockBatchId = 'BATCH-2024-042';
  const mockCurrentStage: Stage = 'ferment';
  
  // Mock event log with timestamps
  const mockEventLog = [
    {
      stage: 'arrival' as Stage,
      message: 'Fruit received and initial inspection completed',
      timestamp: '2024-04-15T08:30:00Z'
    },
    {
      stage: 'arrival' as Stage,
      message: 'Weight and quality assessment completed',
      timestamp: '2024-04-15T09:45:00Z'
    },
    {
      stage: 'prep' as Stage,
      message: 'Chemistry analysis started',
      timestamp: '2024-04-15T11:20:00Z'
    },
    {
      stage: 'prep' as Stage,
      message: 'pH adjustment completed',
      timestamp: '2024-04-15T14:15:00Z'
    },
    {
      stage: 'heat' as Stage,
      message: 'Heat activation process initiated',
      timestamp: '2024-04-16T10:00:00Z'
    },
    {
      stage: 'heat' as Stage,
      message: 'Temperature reached optimal level',
      timestamp: '2024-04-16T11:30:00Z'
    },
    {
      stage: 'ferment' as Stage,
      message: 'Fermentation started with selected yeast strain',
      timestamp: '2024-04-17T09:00:00Z'
    }
  ];

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        Batch Journey Tracker Test
      </Typography>
      
      <Paper sx={{ p: 4, mt: 4 }}>
        <BatchJourneyTimeline 
          batchId={mockBatchId}
          currentStage={mockCurrentStage}
          eventLog={mockEventLog}
        />
      </Paper>
      
      <Box sx={{ mt: 4 }}>
        <Typography variant="h6" gutterBottom>
          Test Notes
        </Typography>
        <Typography variant="body1" paragraph>
          This test page demonstrates the Batch Journey Tracker component with mock data.
          The batch is currently in the "Fermentation" stage, so:
        </Typography>
        <ul>
          <li>Arrival, Chemistry Prep, and Heat Activation stages should be green (completed)</li>
          <li>Fermentation stage should be yellow (in progress)</li>
          <li>Distillation stage should be gray (not started)</li>
          <li>The event log shows 7 entries with timestamps</li>
          <li>Hover over each stage to see completion timestamps (if available)</li>
        </ul>
      </Box>
    </Container>
  );
};

export default TestBatchJourney; 