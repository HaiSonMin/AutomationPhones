import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../../services/authService';
import DashboardLayout from '../../layouts/DashboardLayout';
import DashboardContent from './DashboardContent';

export default function DashboardPage() {
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
      <DashboardContent />
    </DashboardLayout>
  );
}
