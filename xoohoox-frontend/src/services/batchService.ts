import api from './api';

export interface Batch {
  id: string;
  batch_id: string;
  fruit_type: string;
  process_type: string;
  status: string;
  start_date: string;
  expected_completion: string;
  current_stage: string;
  progress: number;
  quantity: number;
  unit: string;
  temperature?: number;
  ph_level?: number;
  brix_level?: number;
  alcohol_content?: number;
  notes?: string;
  stages?: Array<{
    name: string;
    status: 'completed' | 'in_progress' | 'pending';
    start_date?: string;
    end_date?: string;
    duration?: number;
  }>;
  quality_checks?: Array<{
    id: string;
    check_type: string;
    result: string;
    timestamp: string;
    notes: string;
  }>;
}

export interface BatchCreate {
  batch_id?: string;
  fruit_type: string;
  process_type: string;
  quantity: number;
  unit: string;
  expected_completion: string;
  notes?: string;
}

export interface BatchUpdate {
  status?: string;
  current_stage?: string;
  progress?: number;
  temperature?: number;
  ph_level?: number;
  brix_level?: number;
  alcohol_content?: number;
  notes?: string;
}

export interface BatchListResponse {
  total: number;
  items: Batch[];
}

class BatchService {
  async getBatches(params?: {
    skip?: number;
    limit?: number;
    juice_type?: string;
    status?: string;
    start_date?: string;
    end_date?: string;
  }): Promise<BatchListResponse> {
    try {
      const response = await api.get('/batches/', { params });
      return response.data;
    } catch (error) {
      console.log('Falling back to mock data for batches');
      // Fallback to mock endpoint
      const response = await api.get('/mock/batches/', { params });
      return response.data;
    }
  }

  async getBatch(batchId: string): Promise<Batch> {
    try {
      const response = await api.get(`/batches/${batchId}`);
      return response.data;
    } catch (error) {
      console.log('Falling back to mock data for batch details');
      // Return mock data for specific batch
      const mockBatches = await this.getBatches();
      const batch = mockBatches.items.find(b => b.batch_id === batchId);
      if (batch) {
        return batch;
      }
      throw new Error('Batch not found');
    }
  }

  async createBatch(batchData: BatchCreate): Promise<Batch> {
    try {
      const response = await api.post('/batches/', batchData);
      return response.data;
    } catch (error) {
      console.log('Mock create batch - returning sample data');
      // Return mock created batch
      return {
        id: Date.now().toString(),
        batch_id: batchData.batch_id || `XHR-${new Date().toISOString().slice(0, 10).replace(/-/g, '')}-01-01-B${Math.floor(Math.random() * 1000).toString().padStart(3, '0')}`,
        fruit_type: batchData.fruit_type,
        process_type: batchData.process_type,
        status: 'active',
        start_date: new Date().toISOString(),
        expected_completion: batchData.expected_completion,
        current_stage: 'initial',
        progress: 0,
        quantity: batchData.quantity,
        unit: batchData.unit,
        notes: batchData.notes
      };
    }
  }

  async updateBatch(batchId: string, batchData: BatchUpdate): Promise<Batch> {
    try {
      const response = await api.put(`/batches/${batchId}`, batchData);
      return response.data;
    } catch (error) {
      console.log('Mock update batch');
      // Return mock updated batch
      const existingBatch = await this.getBatch(batchId);
      return { ...existingBatch, ...batchData };
    }
  }

  async deleteBatch(batchId: string): Promise<void> {
    try {
      await api.delete(`/batches/${batchId}`);
    } catch (error) {
      console.log('Mock delete batch');
      // Mock successful deletion
      return;
    }
  }

  async startBatch(batchId: string, data: { start_date: string }): Promise<Batch> {
    try {
      const response = await api.post(`/batches/${batchId}/start`, data);
      return response.data;
    } catch (error) {
      console.log('Mock start batch');
      const existingBatch = await this.getBatch(batchId);
      return { ...existingBatch, status: 'active', start_date: data.start_date };
    }
  }

  async completeBatch(batchId: string, data: { completion_date: string }): Promise<Batch> {
    try {
      const response = await api.post(`/batches/${batchId}/complete`, data);
      return response.data;
    } catch (error) {
      console.log('Mock complete batch');
      const existingBatch = await this.getBatch(batchId);
      return { ...existingBatch, status: 'completed', progress: 100 };
    }
  }

  async updateBatchStatus(batchId: string, status: string): Promise<Batch> {
    try {
      const response = await api.patch(`/batches/${batchId}/status`, { status });
      return response.data;
    } catch (error) {
      console.log('Mock update batch status');
      const existingBatch = await this.getBatch(batchId);
      return { ...existingBatch, status };
    }
  }

  async getBatchQualityChecks(batchId: string): Promise<any[]> {
    try {
      const response = await api.get(`/batches/${batchId}/quality-checks`);
      return response.data;
    } catch (error) {
      console.log('Mock quality checks');
      return [
        {
          id: '1',
          test_id: `QC-${batchId}-001`,
          batch_id: batchId,
          test_type: 'pH',
          result: 'pass',
          test_date: new Date().toISOString()
        }
      ];
    }
  }

  async addBatchQualityCheck(batchId: string, qualityCheckData: any): Promise<any> {
    try {
      const response = await api.post(`/batches/${batchId}/quality-checks`, qualityCheckData);
      return response.data;
    } catch (error) {
      console.log('Mock add quality check');
      return {
        id: Date.now().toString(),
        test_id: `QC-${batchId}-${Date.now()}`,
        batch_id: batchId,
        ...qualityCheckData,
        test_date: new Date().toISOString()
      };
    }
  }

  async reportBatchIssue(batchId: string, issueData: {
    issue_type: string;
    description: string;
    severity: string;
  }): Promise<Batch> {
    try {
      const response = await api.post(`/batches/${batchId}/issues`, issueData);
      return response.data;
    } catch (error) {
      console.log('Mock report issue');
      const existingBatch = await this.getBatch(batchId);
      return { ...existingBatch, status: 'issue_reported' };
    }
  }

  async takeCorrectiveAction(batchId: string, actionData: {
    action_type: string;
    description: string;
    expected_outcome: string;
  }): Promise<Batch> {
    try {
      const response = await api.post(`/batches/${batchId}/corrective-actions`, actionData);
      return response.data;
    } catch (error) {
      console.log('Mock corrective action');
      const existingBatch = await this.getBatch(batchId);
      return { ...existingBatch, status: 'corrective_action_taken' };
    }
  }
}

export default new BatchService(); 