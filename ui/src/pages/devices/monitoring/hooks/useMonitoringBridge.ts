/**
 * useMonitoringBridge - Hook for frontend-backend communication
 */

import { useMemo } from 'react';
import type { Device, GlobalSettings, ApiResult, MonitoringStats } from '../types/monitoring.types';

// Mock data for browser testing
const MOCK_DEVICES: Device[] = [
  {
    device_id: 'mock-device-1',
    model: 'Mock Phone',
    adb_status: 'device',
    state: 'previewing',
    is_online: true,
    has_preview: true,
    has_window: false,
    fps: 14.5,
    error: null,
  },
];

const MOCK_SETTINGS: GlobalSettings = {
  auto_preview: true,
  preview_fps: 15,
  preview_size: 480,
  preview_quality: 70,
  max_size: 800,
  max_fps: 30,
  bitrate: 4,
};

export interface MonitoringBridge {
  getDevices: (forceRefresh?: boolean) => Promise<Device[]>;
  refreshDevices: () => Promise<Device[]>;
  getDevice: (deviceId: string) => Promise<Device | null>;
  getFrame: (deviceId: string) => Promise<string | null>;
  startPreview: (deviceId: string) => Promise<ApiResult>;
  stopPreview: (deviceId: string) => Promise<ApiResult>;
  openWindow: (deviceId: string) => Promise<ApiResult>;
  closeWindow: (deviceId: string) => Promise<ApiResult>;
  stopAll: () => Promise<ApiResult>;
  getSettings: () => Promise<GlobalSettings>;
  updateSettings: (settings: Partial<GlobalSettings>) => Promise<GlobalSettings>;
  getStats: () => Promise<MonitoringStats>;
  isAvailable: () => Promise<boolean>;
}

export function useMonitoringBridge(): MonitoringBridge {
  return useMemo(() => {
    const api = window.pywebview?.api;
    const isInApp = !!api;

    return {
      getDevices: async (forceRefresh = false) => {
        if (isInApp && api?.monitoring_get_devices) {
          // Python API doesn't support parameters yet, so we'll use refreshDevices
          if (forceRefresh) {
            return await api.monitoring_refresh_devices();
          }
          return await api.monitoring_get_devices();
        }
        return MOCK_DEVICES;
      },

      refreshDevices: async () => {
        if (isInApp && api?.monitoring_refresh_devices) {
          return await api.monitoring_refresh_devices();
        }
        return MOCK_DEVICES;
      },

      getDevice: async (deviceId: string) => {
        if (isInApp && api?.monitoring_get_device) {
          return await api.monitoring_get_device(deviceId);
        }
        return MOCK_DEVICES.find((d) => d.device_id === deviceId) || null;
      },

      getFrame: async (deviceId: string) => {
        if (isInApp && api?.monitoring_get_frame) {
          return await api.monitoring_get_frame(deviceId);
        }
        return null;
      },

      startPreview: async (deviceId: string) => {
        if (isInApp && api?.monitoring_start_preview) {
          return await api.monitoring_start_preview(deviceId);
        }
        return { success: true };
      },

      stopPreview: async (deviceId: string) => {
        if (isInApp && api?.monitoring_stop_preview) {
          return await api.monitoring_stop_preview(deviceId);
        }
        return { success: true };
      },

      openWindow: async (deviceId: string) => {
        if (isInApp && api?.monitoring_open_window) {
          return await api.monitoring_open_window(deviceId);
        }
        return { success: true };
      },

      closeWindow: async (deviceId: string) => {
        if (isInApp && api?.monitoring_close_window) {
          return await api.monitoring_close_window(deviceId);
        }
        return { success: true };
      },

      stopAll: async () => {
        if (isInApp && api?.monitoring_stop_all) {
          return await api.monitoring_stop_all();
        }
        return { success: true };
      },

      getSettings: async () => {
        if (isInApp && api?.monitoring_get_settings) {
          return await api.monitoring_get_settings();
        }
        return MOCK_SETTINGS;
      },

      updateSettings: async (settings: Partial<GlobalSettings>) => {
        if (isInApp && api?.monitoring_update_settings) {
          return await api.monitoring_update_settings(
            settings.auto_preview,
            settings.preview_fps,
            settings.preview_size,
            settings.preview_quality
          );
        }
        return MOCK_SETTINGS;
      },

      getStats: async (): Promise<MonitoringStats> => {
        if (isInApp && api?.monitoring_get_stats) {
          const stats = await api.monitoring_get_stats();
          return {
            device_count: stats.device_count ?? stats.total_devices ?? 0,
            previewing_count: stats.previewing_count ?? stats.connected_devices ?? 0,
            window_count: stats.window_count ?? 0,
            is_running: stats.is_running ?? stats.monitoring_active ?? false,
            is_available: stats.is_available ?? true,
          };
        }
        return {
          device_count: 1,
          previewing_count: 1,
          window_count: 0,
          is_running: true,
          is_available: true,
        };
      },

      isAvailable: async () => {
        if (isInApp && api?.monitoring_is_available) {
          return await api.monitoring_is_available();
        }
        return true;
      },
    };
  }, []);
}

export default useMonitoringBridge;
