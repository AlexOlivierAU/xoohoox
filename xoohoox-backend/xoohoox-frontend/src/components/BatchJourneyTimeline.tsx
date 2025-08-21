import React from 'react';
import { Box, Typography, Paper, Tooltip } from '@mui/material';
import { CheckCircle, RadioButtonUnchecked, Pending } from '@mui/icons-material';

// Define the stage types
type Stage = 'arrival' | 'prep' | 'heat' | 'ferment' | 'distill';

// Define the event log entry type
interface EventLogEntry {
  stage: Stage;
  message: string;
  timestamp: string;
}

// Define the component props
interface BatchJourneyTimelineProps {
  batchId: string;
  currentStage: Stage;
  eventLog: EventLogEntry[];
}

// Stage configuration
const stages: { id: Stage; label: string }[] = [
  { id: 'arrival', label: 'Arrival' },
  { id: 'prep', label: 'Chemistry Prep' },
  { id: 'heat', label: 'Heat Activation' },
  { id: 'ferment', label: 'Fermentation' },
  { id: 'distill', label: 'Distillation' }
];

const BatchJourneyTimeline: React.FC<BatchJourneyTimelineProps> = ({
  batchId,
  currentStage,
  eventLog
}) => {
  // Function to determine the status of a stage
  const getStageStatus = (stageId: Stage) => {
    const stageIndex = stages.findIndex(s => s.id === stageId);
    const currentStageIndex = stages.findIndex(s => s.id === currentStage);
    
    if (stageIndex < currentStageIndex) {
      return 'completed';
    } else if (stageId === currentStage) {
      return 'in-progress';
    } else {
      return 'not-started';
    }
  };

  // Function to get the completion timestamp for a stage
  const getStageCompletionTime = (stageId: Stage) => {
    const completedEvents = eventLog
      .filter(event => event.stage === stageId)
      .sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
    
    return completedEvents.length > 0 ? completedEvents[0].timestamp : null;
  };

  return (
    <Box className="w-full">
      <Typography variant="h6" className="mb-4">
        Batch Journey: {batchId}
      </Typography>
      
      {/* Timeline */}
      <Box className="flex items-center justify-between mb-8 relative">
        {/* Progress line */}
        <Box className="absolute top-1/2 left-0 right-0 h-1 bg-gray-200 -translate-y-1/2 z-0" />
        
        {stages.map((stage, index) => {
          const status = getStageStatus(stage.id);
          const completionTime = getStageCompletionTime(stage.id);
          
          return (
            <Tooltip 
              key={stage.id}
              title={completionTime ? `Completed: ${new Date(completionTime).toLocaleString()}` : 'Not completed yet'}
              placement="top"
            >
              <Box className="flex flex-col items-center z-10">
                <Box 
                  className={`
                    w-10 h-10 rounded-full flex items-center justify-center
                    ${status === 'completed' ? 'bg-green-500 text-white' : ''}
                    ${status === 'in-progress' ? 'bg-yellow-500 text-white' : ''}
                    ${status === 'not-started' ? 'bg-gray-300 text-gray-500' : ''}
                  `}
                >
                  {status === 'completed' && <CheckCircle />}
                  {status === 'in-progress' && <Pending />}
                  {status === 'not-started' && <RadioButtonUnchecked />}
                </Box>
                <Typography 
                  variant="body2" 
                  className={`mt-2 text-center ${status === 'in-progress' ? 'font-bold' : ''}`}
                >
                  {stage.label}
                </Typography>
              </Box>
            </Tooltip>
          );
        })}
      </Box>
      
      {/* Event Log */}
      <Paper className="p-4 max-h-60 overflow-y-auto">
        <Typography variant="subtitle1" className="mb-3 font-bold">
          Event Log
        </Typography>
        <Box className="space-y-2">
          {eventLog.length > 0 ? (
            eventLog.map((event, index) => (
              <Box key={index} className="border-l-2 border-gray-300 pl-3 py-1">
                <Typography variant="body2" className="text-gray-500">
                  {new Date(event.timestamp).toLocaleString()}
                </Typography>
                <Typography variant="body1">
                  <span className="font-medium">{stages.find(s => s.id === event.stage)?.label}:</span> {event.message}
                </Typography>
              </Box>
            ))
          ) : (
            <Typography variant="body2" className="text-gray-500">
              No events recorded yet.
            </Typography>
          )}
        </Box>
      </Paper>
    </Box>
  );
};

export default BatchJourneyTimeline; 