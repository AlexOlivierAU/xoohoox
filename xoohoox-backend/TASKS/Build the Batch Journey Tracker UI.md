## Task: Build the Batch Journey Tracker UI

### Context:
We’re building a fermentation and distillation process manager for XooHooX, an R&D lab that processes fruit into distillate. Each batch progresses through five main stages:

1. Arrival
2. Chemistry Prep
3. Heat Activation
4. Fermentation
5. Distillation

We want a clean UI component that visualizes the current status of a batch as it moves through these stages, along with a log of milestone events.

### What to Build:
- Create a React component called `<BatchJourneyTimeline />`
- Render a horizontal progress tracker with 5 labeled stages
- Use color to indicate stage status:
  - ✅ Green = Completed
  - 🟡 Yellow = In Progress
  - ⬜ Gray = Not Started
- Below the tracker, display a scrollable event log (one entry per step taken)

### File Location:
Place the component here:  
`src/components/BatchJourneyTimeline.tsx`

Also create a simple page for testing:  
`src/pages/TestBatchJourney.tsx`

### Component Props:
```ts
{
  batchId: string;
  currentStage: 'arrival' | 'prep' | 'heat' | 'ferment' | 'distill';
  eventLog: {
    stage: 'arrival' | 'prep' | 'heat' | 'ferment' | 'distill';
    message: string;
    timestamp: string;
  }[];
}
```

### Design Notes:
- Use TailwindCSS for styling (assume already set up)
- Timeline should look like a connected path (e.g., with dots or steps)
- Each stage should be clickable (future expansion)
- Event log can use a simple list or table layout

### How We’ll Test It:
In `TestBatchJourney.tsx`:
- Render `<BatchJourneyTimeline />` with mock data
- Simulate a batch that is in the “Ferment” stage
- Verify that:
  - Stages before Ferment are ✅ green
  - Ferment is 🟡 yellow
  - Distill is ⬜ gray
  - Event log shows 3–4 mock entries with timestamps

### Bonus (optional):
If you have time, allow hover tooltips on each stage showing when that stage was completed (if available).
