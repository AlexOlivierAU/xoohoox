import api from './api';

export interface MaintenanceRecord {
  id: string;
  equipmentId: string;
  maintenanceType: 'Preventive' | 'Corrective' | 'Emergency';
  description: string;
  scheduledDate: Date;
  completedDate?: Date;
  technician: string;
  status: 'Scheduled' | 'In Progress' | 'Completed' | 'Overdue';
  notes: string;
}

export const maintenanceService = {
  // Get all maintenance records
  getAll: async () => {
    const response = await api.get<MaintenanceRecord[]>('/maintenance');
    return response.data;
  },

  // Get maintenance records for a specific equipment
  getByEquipmentId: async (equipmentId: string) => {
    const response = await api.get<MaintenanceRecord[]>(`/maintenance/equipment/${equipmentId}`);
    return response.data;
  },

  // Get a single maintenance record by ID
  getById: async (id: string) => {
    const response = await api.get<MaintenanceRecord>(`/maintenance/${id}`);
    return response.data;
  },

  // Create a new maintenance record
  create: async (record: Omit<MaintenanceRecord, 'id'>) => {
    const response = await api.post<MaintenanceRecord>('/maintenance', record);
    return response.data;
  },

  // Update a maintenance record
  update: async (id: string, record: Partial<MaintenanceRecord>) => {
    const response = await api.put<MaintenanceRecord>(`/maintenance/${id}`, record);
    return response.data;
  },

  // Delete a maintenance record
  delete: async (id: string) => {
    await api.delete(`/maintenance/${id}`);
  },

  // Update maintenance status
  updateStatus: async (id: string, status: MaintenanceRecord['status']) => {
    const response = await api.patch<MaintenanceRecord>(`/maintenance/${id}/status`, { status });
    return response.data;
  },

  // Complete maintenance
  complete: async (id: string, completedDate: Date) => {
    const response = await api.patch<MaintenanceRecord>(`/maintenance/${id}/complete`, { completedDate });
    return response.data;
  },

  // Get maintenance statistics
  getStatistics: async () => {
    const response = await api.get('/maintenance/statistics');
    return response.data;
  },
}; 