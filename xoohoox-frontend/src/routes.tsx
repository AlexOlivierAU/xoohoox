import React from 'react';
import { Routes, Route, Navigate, Outlet } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import Dashboard from './pages/Dashboard';
import Production from './pages/Production';
import Analytics from './pages/Analytics';
import Reports from './pages/Reports';
import Settings from './pages/Settings';
import Login from './pages/Login';
import BatchList from './pages/BatchList';
import BatchDetails from './pages/BatchDetails';
import QualityChecks from './pages/QualityChecks';
import Home from './pages/Home';
import BatchManagement from './pages/BatchManagement';
import EquipmentMaintenance from './pages/EquipmentMaintenance';
import QualityControl from './pages/QualityControl';
import Inventory from './pages/Inventory';
import UserManagement from './pages/UserManagement';
import EnhancedBatchForm from './pages/EnhancedBatchForm';
import FarmersSuppliers from './pages/FarmersSuppliers';
import FermentationTrials from './pages/FermentationTrials';
import NewQualityCheck from './pages/NewQualityCheck';

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/" element={<MainLayout><Outlet /></MainLayout>}>
        <Route index element={<Home />} />
        <Route path="dashboard" element={<Dashboard />} />
        <Route path="production" element={<Production />} />
        <Route path="analytics" element={<Analytics />} />
        <Route path="reports" element={<Reports />} />
        <Route path="settings" element={<Settings />} />
        <Route path="batches" element={<BatchList />} />
        <Route path="batches/create" element={<EnhancedBatchForm />} />
        <Route path="batches/:batchId" element={<BatchDetails />} />
        <Route path="quality-checks" element={<QualityChecks />} />
        <Route path="quality-checks/new" element={<NewQualityCheck />} />
        <Route path="batch-management" element={<BatchManagement />} />
        <Route path="equipment-maintenance" element={<EquipmentMaintenance />} />
        <Route path="quality-control" element={<QualityControl />} />
        <Route path="inventory" element={<Inventory />} />
        <Route path="farmers-suppliers" element={<FarmersSuppliers />} />
        <Route path="fermentation-trials" element={<FermentationTrials />} />
        <Route path="users" element={<UserManagement />} />
        <Route path="enhanced-batch" element={<EnhancedBatchForm />} />
      </Route>
    </Routes>
  );
};

export default AppRoutes; 