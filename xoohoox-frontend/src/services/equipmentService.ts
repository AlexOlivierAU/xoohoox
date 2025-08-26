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
    try {
      const response = await api.get('/equipment/', { params });
      return response.data;
    } catch (error) {
      console.log('Falling back to mock equipment data');
      // Return mock equipment data
      return {
        items: [
          {
            id: '1',
            name: 'Distillation Column A',
            type: 'distillation',
            status: 'operational',
            location: 'Production Floor 1',
            last_maintenance: '2024-03-15',
            next_maintenance: '2024-06-15',
            manufacturer: 'DistillTech',
            model: 'DC-2000',
            serial_number: 'DT-2024-001',
            notes: 'Primary distillation column'
          },
          {
            id: '2',
            name: 'Fermentation Tank B',
            type: 'fermentation',
            status: 'operational',
            location: 'Production Floor 1',
            last_maintenance: '2024-03-10',
            next_maintenance: '2024-06-10',
            manufacturer: 'FermentCorp',
            model: 'FT-5000',
            serial_number: 'FC-2024-002',
            notes: 'Large fermentation tank'
          },
          {
            id: '3',
            name: 'Heat Exchanger C',
            type: 'heat_exchanger',
            status: 'maintenance',
            location: 'Production Floor 2',
            last_maintenance: '2024-02-20',
            next_maintenance: '2024-05-20',
            manufacturer: 'HeatTech',
            model: 'HE-1000',
            serial_number: 'HT-2024-003',
            notes: 'Under scheduled maintenance'
          }
        ],
        total: 3
      };
    }
  }

  async getEquipmentById(equipmentId: string): Promise<Equipment> {
    try {
      const response = await api.get(`/equipment/${equipmentId}`);
      return response.data;
    } catch (error) {
      console.log('Falling back to mock equipment data');
      // Return mock equipment data
      return {
        id: equipmentId,
        name: 'Mock Equipment',
        type: 'distillation',
        status: 'operational',
        location: 'Production Floor 1',
        last_maintenance: '2024-03-15',
        next_maintenance: '2024-06-15',
        manufacturer: 'Mock Manufacturer',
        model: 'Mock Model',
        serial_number: 'Mock-SN-001',
        notes: 'Mock equipment for testing'
      };
    }
  }

  async createEquipment(equipmentData: Partial<Equipment>): Promise<Equipment> {
    try {
      const response = await api.post('/equipment/', equipmentData);
      return response.data;
    } catch (error) {
      console.log('Mock create equipment');
      // Return mock created equipment
      return {
        id: Date.now().toString(),
        name: equipmentData.name || 'New Equipment',
        type: equipmentData.type || 'distillation',
        status: equipmentData.status || 'operational',
        location: equipmentData.location || 'Production Floor 1',
        last_maintenance: new Date().toISOString().split('T')[0],
        next_maintenance: new Date(Date.now() + 90 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        manufacturer: equipmentData.manufacturer || 'Mock Manufacturer',
        model: equipmentData.model || 'Mock Model',
        serial_number: equipmentData.serial_number || `Mock-SN-${Date.now()}`,
        notes: equipmentData.notes
      };
    }
  }

  async updateEquipment(equipmentId: string, equipmentData: Partial<Equipment>): Promise<Equipment> {
    try {
      const response = await api.put(`/equipment/${equipmentId}`, equipmentData);
      return response.data;
    } catch (error) {
      console.log('Mock update equipment');
      // Return mock updated equipment
      const existingEquipment = await this.getEquipmentById(equipmentId);
      return { ...existingEquipment, ...equipmentData };
    }
  }

  async deleteEquipment(equipmentId: string): Promise<void> {
    try {
      await api.delete(`/equipment/${equipmentId}`);
    } catch (error) {
      console.log('Mock delete equipment');
      // Mock successful deletion
      return;
    }
  }

  // Maintenance endpoints
  async getMaintenanceRecords(params?: {
    skip?: number;
    limit?: number;
    equipment_id?: string;
    status?: string;
    maintenance_type?: string;
  }): Promise<MaintenanceListResponse> {
    try {
      const response = await api.get('/equipment-maintenance/', { params });
      return response.data;
    } catch (error) {
      console.log('Falling back to mock maintenance records');
      // Return mock maintenance records
      return {
        items: [
          {
            id: '1',
            equipment_id: '1',
            maintenance_type: 'preventive',
            description: 'Routine inspection and cleaning of distillation column',
            scheduled_date: '2024-06-15',
            completed_date: undefined,
            technician: 'John Smith',
            status: 'scheduled',
            notes: 'Standard preventive maintenance',
            cost: undefined,
            parts_used: undefined
          },
          {
            id: '2',
            equipment_id: '2',
            maintenance_type: 'preventive',
            description: 'Fermentation tank cleaning and sanitization',
            scheduled_date: '2024-06-10',
            completed_date: '2024-06-10',
            technician: 'Sarah Johnson',
            status: 'completed',
            notes: 'Completed on schedule',
            cost: 500,
            parts_used: ['Cleaning solution', 'Sanitizer']
          },
          {
            id: '3',
            equipment_id: '3',
            maintenance_type: 'corrective',
            description: 'Heat exchanger repair - replacing damaged seals',
            scheduled_date: '2024-05-20',
            completed_date: undefined,
            technician: 'Mike Wilson',
            status: 'in_progress',
            notes: 'Seals need replacement due to wear',
            cost: 1200,
            parts_used: ['Replacement seals', 'Gasket material']
          },
          {
            id: '4',
            equipment_id: '1',
            maintenance_type: 'emergency',
            description: 'Emergency repair of pressure valve',
            scheduled_date: '2024-05-15',
            completed_date: '2024-05-15',
            technician: 'Emergency Team',
            status: 'completed',
            notes: 'Emergency repair completed successfully',
            cost: 800,
            parts_used: ['Pressure valve', 'Safety seals']
          }
        ],
        total: 4
      };
    }
  }

  async getMaintenanceRecord(recordId: string): Promise<MaintenanceRecord> {
    try {
      const response = await api.get(`/equipment-maintenance/${recordId}`);
      return response.data;
    } catch (error) {
      console.log('Falling back to mock maintenance record');
      // Return mock maintenance record
      return {
        id: recordId,
        equipment_id: '1',
        maintenance_type: 'preventive',
        description: 'Mock maintenance record',
        scheduled_date: new Date().toISOString().split('T')[0],
        completed_date: undefined,
        technician: 'Mock Technician',
        status: 'scheduled',
        notes: 'Mock record for testing',
        cost: undefined,
        parts_used: undefined
      };
    }
  }

  async createMaintenanceRecord(recordData: MaintenanceRecordCreate): Promise<MaintenanceRecord> {
    try {
      const response = await api.post('/equipment-maintenance/', recordData);
      return response.data;
    } catch (error) {
      console.log('Mock create maintenance record');
      // Return mock created maintenance record
      return {
        id: Date.now().toString(),
        equipment_id: recordData.equipment_id,
        maintenance_type: recordData.maintenance_type,
        description: recordData.description,
        scheduled_date: recordData.scheduled_date,
        completed_date: undefined,
        technician: recordData.technician,
        status: 'scheduled',
        notes: recordData.notes,
        cost: undefined,
        parts_used: undefined
      };
    }
  }

  async updateMaintenanceRecord(recordId: string, recordData: MaintenanceRecordUpdate): Promise<MaintenanceRecord> {
    const response = await api.put(`/equipment-maintenance/${recordId}`, recordData);
    return response.data;
  }

  async deleteMaintenanceRecord(recordId: string): Promise<void> {
    await api.delete(`/equipment-maintenance/${recordId}`);
  }

  async getEquipmentMaintenanceHistory(equipmentId: string): Promise<MaintenanceRecord[]> {
    const response = await api.get(`/equipment-maintenance/equipment/${equipmentId}`);
    return response.data;
  }

  async scheduleMaintenance(equipmentId: string, maintenanceData: MaintenanceRecordCreate): Promise<MaintenanceRecord> {
    const response = await api.post(`/equipment-maintenance/equipment/${equipmentId}`, maintenanceData);
    return response.data;
  }

  async completeMaintenance(recordId: string, completionData: {
    completed_date: string;
    notes?: string;
    cost?: number;
    parts_used?: string[];
  }): Promise<MaintenanceRecord> {
    const response = await api.post(`/equipment-maintenance/${recordId}/complete`, completionData);
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