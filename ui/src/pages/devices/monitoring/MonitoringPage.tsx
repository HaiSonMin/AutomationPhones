/**
 * MonitoringPage - Main page for device monitoring
 *
 * This is the entry point for the monitoring feature.
 * Wraps MonitoringContent in DashboardLayout like DashboardPage.
 */

import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../../../services/authService';
import DashboardLayout from '../../../layouts/DashboardLayout';
import MonitoringContent from './MonitoringContent';

export const MonitoringPage: React.FC = () => {
  const navigate = useNavigate();

  useEffect(() => {
    // Verify authentication on mount
    authService.checkAuth().then((isAuth) => {
      if (!isAuth) {
        navigate('/login');
      }
    });
  }, [navigate]);

  return (
    <DashboardLayout>
      <MonitoringContent />
    </DashboardLayout>
  );
};

export default MonitoringPage;
