# Upscale Tracking Components

## UpscaleHistory

A table component that displays the history of upscale runs for a fermentation trial.

### Props
```typescript
interface Props {
  upscales: UpscaleRun[];  // List of upscale runs to display
  onStartUpscale: () => void;  // Called when starting a new upscale
  onRecordYield: (upscaleId: number) => void;  // Called when recording yield
  onInputCompound: (upscaleId: number) => void;  // Called when inputting compound data
  onMarkComplete: (upscaleId: number) => void;  // Called when marking as complete
}
```

### Features
- Displays upscale stages, volumes, dates, yields, and ABV results
- Shows compound status with visual indicators
- Formats measurements appropriately (L/mL for volume/yield)
- Handles pending and completed states

### Usage
```tsx
import { UpscaleHistory } from '../components/UpscaleHistory';

function TrialDetail() {
  return (
    <UpscaleHistory
      upscales={upscales}
      onStartUpscale={handleStartUpscale}
      onRecordYield={handleRecordYield}
      onInputCompound={handleInputCompound}
      onMarkComplete={handleMarkComplete}
    />
  );
}
```

## UpscaleResultDialog

A dialog component for recording upscale results including yield, ABV, and compound data.

### Props
```typescript
interface Props {
  open: boolean;  // Controls dialog visibility
  onClose: () => void;  // Called when dialog is closed
  onSubmit: (result: UpscaleResult) => void;  // Called with form data on submit
  upscaleStage: string;  // Current upscale stage (e.g., "Test 4")
  upscaleVolume: number;  // Current volume in Liters
}
```

### Features
- Form validation for required fields
- Numeric input with appropriate step sizes
- Multiline compound notes
- Proper unit handling for measurements

### Usage
```tsx
import { UpscaleResultDialog } from '../components/UpscaleResultDialog';

function TrialDetail() {
  const [dialogOpen, setDialogOpen] = useState(false);

  const handleSubmit = (result: UpscaleResult) => {
    // Handle result submission
    setDialogOpen(false);
  };

  return (
    <UpscaleResultDialog
      open={dialogOpen}
      onClose={() => setDialogOpen(false)}
      onSubmit={handleSubmit}
      upscaleStage="Test 4"
      upscaleVolume={5}
    />
  );
}
```

## Data Types

### UpscaleRun
```typescript
interface UpscaleRun {
  id: number;
  upscale_id: string;
  stage: string;
  volume: number;
  yield_amount: number | null;
  abv_result: number | null;
  compound_summary: string | null;
  status: 'pending' | 'complete' | 'failed';
  timestamp: string;
}
```

### UpscaleResult
```typescript
interface UpscaleResult {
  yield_amount: number;
  abv_result: number;
  compound_summary: string;
}
``` 