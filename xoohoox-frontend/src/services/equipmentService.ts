import api from './api';

export interface Equipment {
  id: string;
  name: string;
  type: string;
  status: 'operational' | 'maintenance' | 'offline' | 'error';
  location: string;
  last_maintenance: string;
  next_maintenance: string;
  manufacturer: string;
  model: string;
  serial_number: string;
  notes?: string;
}

export interface MaintenanceRecord {
  id: string;
  equipment_id: string;
  maintenance_type: 'preventive' | 'corrective' | 'emergency';
  description: string;
  scheduled_date: string;
  completed_date?: string;
  technician: string;
  status: 'scheduled' | 'in_progress' | 'completed' | 'overdue';
  notes?: string;
  cost?: number;
  parts_used?: string[];
}

export interface MaintenanceRecordCreate {
  equipment_id: string;
  maintenance_type: 'preventive' | 'corrective' | 'emergency';
  description: string;
  scheduled_date: string;
  technician: string;
  notes?: string;
}

export interface MaintenanceRecordUpdate {
  status?: 'scheduled' | 'in_progress' | 'completed' | 'overdue';
  completed_date?: string;
  notes?: string;
  cost?: number;
  parts_used?: string[];
}

export interface EquipmentListResponse {
  items: Equipment[];
  total: number;
}

export interface MaintenanceListResponse {
  items: MaintenanceRecord[];
  total: number;
}

class EquipmentService {
  // Equipment endpoints
  async getEquipment(params?: {
    skip?: number;
    limit?: number;
    status?: string;
    type?: string;
  }): Promise<EquipmentListResponse> {
    const response = await api.get('/equipment/', { params });
    return response.data;
  }

  async getEquipmentById(equipmentId: string): Promise<Equipment> {
    const response = await api.get(`/equipment/${equipmentId}`);
    return response.data;
  }

  async createEquipment(equipmentData: Partial<Equipment>): Promise<Equipment> {
    const response = await api.post('/equipment/', equipmentData);
    return response.data;
  }

  async updateEquipment(equipmentId: string, equipmentData: Partial<Equipment>): Promise<Equipment> {
    const response = await api.put(`/equipment/${equipmentId}`, equipmentData);
    return response.data;
  }

  async deleteEquipment(equipmentId: string): Promise<void> {
    await api.delete(`/equipment/${equipmentId}`);
  }

  // Maintenance endpoints
  async getMaintenanceRecords(params?: {
    skip?: number;
    limit?: number;
    equipment_id?: string;
    status?: string;
    maintenance_type?: string;
  }): Promise<MaintenanceListResponse> {
    const response = await api.get('/equipment/maintenance/', { params });
    return response.data;
  }

  async getMaintenanceRecord(recordId: string): Promise<MaintenanceRecord> {
    const response = await api.get(`/equipment/maintenance/${recordId}`);
    return response.data;
  }

  async createMaintenanceRecord(recordData: MaintenanceRecordCreate): Promise<MaintenanceRecord> {
    const response = await api.post('/equipment/maintenance/', recordData);
    return response.data;
  }

  async updateMaintenanceRecord(recordId: string, recordData: MaintenanceRecordUpdate): Promise<MaintenanceRecord> {
    const response = await api.put(`/equipment/maintenance/${recordId}`, recordData);
    return response.data;
  }

  async deleteMaintenanceRecord(recordId: string): Promise<void> {
    await api.delete(`/equipment/maintenance/${recordId}`);
  }

  async getEquipmentMaintenanceHistory(equipmentId: string): Promise<MaintenanceRecord[]> {
    const response = await api.get(`/equipment/${equipmentId}/maintenance`);
    return response.data;
  }

  async scheduleMaintenance(equipmentId: string, maintenanceData: MaintenanceRecordCreate): Promise<MaintenanceRecord> {
    const response = await api.post(`/equipment/${equipmentId}/maintenance`, maintenanceData);
    return response.data;
  }

  async completeMaintenance(recordId: string, completionData: {
    completed_date: string;
    notes?: string;
    cost?: number;
    parts_used?: string[];
  }): Promise<MaintenanceRecord> {
    const response = await api.post(`/equipment/maintenance/${recordId}/complete`, completionData);
    return response.data;
  }

  async getEquipmentTypes(): Promise<string[]> {
    const response = await api.get('/equipment/types');
    return response.data;
  }

  async getMaintenanceTypes(): Promise<string[]> {
    const response = await api.get('/equipment/maintenance/types');
    return response.data;
  }

  async getEquipmentStatus(): Promise<{ [key: string]: number }> {
    const response = await api.get('/equipment/status');
    return response.data;
  }

  async getUpcomingMaintenance(days?: number): Promise<MaintenanceRecord[]> {
    const response = await api.get('/equipment/maintenance/upcoming', { 
      params: { days: days || 30 } 
    });
    return response.data;
  }
}

export default new EquipmentService(); 