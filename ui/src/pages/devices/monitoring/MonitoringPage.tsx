import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { MonitoringContent } from './MonitoringContent';
import DashboardLayout from '../../../layouts/DashboardLayout';
import { authService } from '../../../services/authService';

export default function MonitoringPage() {
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
}
