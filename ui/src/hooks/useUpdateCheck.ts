/**
 * useUpdateCheck Hook
 * Auto-check for updates and provide update status
 */

import { useState, useEffect, useCallback } from 'react';
import { updateService, type UpdateCheckResponse } from '../services/updateService';

interface UseUpdateCheckReturn {
  hasUpdate: boolean;
  updateInfo: UpdateCheckResponse | null;
  isChecking: boolean;
  checkForUpdates: () => Promise<void>;
  currentVersion: string;
}

export const useUpdateCheck = (): UseUpdateCheckReturn => {
  const [hasUpdate, setHasUpdate] = useState(false);
  const [updateInfo, setUpdateInfo] = useState<UpdateCheckResponse | null>(null);
  const [isChecking, setIsChecking] = useState(false);
  const [currentVersion, setCurrentVersion] = useState('0.0.0');

  const checkForUpdates = useCallback(async () => {
    setIsChecking(true);
    try {
      // Get current version
      const versionResponse = await updateService.getCurrentVersion();
      if (versionResponse.success && versionResponse.version) {
        setCurrentVersion(versionResponse.version);
      }

      // Check for updates
      const response = await updateService.checkForUpdates();

      if (response.success) {
        setUpdateInfo(response);
        setHasUpdate(response.has_update || false);
      } else {
        console.error('Failed to check for updates:', response.error);
      }
    } catch (error) {
      console.error('Error checking for updates:', error);
    } finally {
      setIsChecking(false);
    }
  }, []);

  // Check on mount
  useEffect(() => {
    checkForUpdates();
  }, [checkForUpdates]);

  // Auto-check every hour
  useEffect(() => {
    const interval = setInterval(() => {
      checkForUpdates();
    }, 60 * 60 * 1000); // 1 hour

    return () => clearInterval(interval);
  }, [checkForUpdates]);

  return {
    hasUpdate,
    updateInfo,
    isChecking,
    checkForUpdates,
    currentVersion,
  };
};
