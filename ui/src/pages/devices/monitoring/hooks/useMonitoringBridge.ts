/**
 * useMonitoringBridge - Hook for communicating with Python monitoring bridge
 *
 * Provides type-safe access to monitoring API methods via pywebview.
 * Handles browser fallback when running outside pywebview.
 *
 * Usage:
 *   const bridge = useMonitoringBridge();
 *   const devices = await bridge.getDevices();
 *   await bridge.connect("abc123");
 */

import { useMemo, useCallback } from 'react';
import type {
  Device,
  ApiResult,
  ConnectResult,
  SetFpsResult,
  SetSizeResult,
  DisconnectAllResult,
  MonitoringStats,
} from '../types/monitoring.types';

// =============================================================================
// BRIDGE INTERFACE
// =============================================================================

/**
 * Interface for monitoring bridge methods
 *
 * This provides a cleaner API than using window.pywebview.api directly.
 * Method names are simplified (no 'monitoring_' prefix).
 */
export interface MonitoringBridge {
  // Device list
  getDevices: () => Promise<Device[]>;
  getDevice: (deviceId: string) => Promise<Device | null>;
  refreshDevices: () => Promise<Device[]>;

  // Device control
  connect: (deviceId: string) => Promise<ConnectResult>;
  disconnect: (deviceId: string) => Promise<ApiResult>;
  disconnectAll: () => Promise<DisconnectAllResult>;

  // Settings
  setFps: (deviceId: string, fps: number) => Promise<SetFpsResult>;
  setSize: (deviceId: string, maxSize: number) => Promise<SetSizeResult>;
  setSettings: (deviceId: string, fps?: number, maxSize?: number) => Promise<ApiResult>;

  // Stats
  getStats: () => Promise<MonitoringStats>;

  // Helper
  isAvailable: boolean;
}

// =============================================================================
// MOCK DATA - For browser testing
// =============================================================================

/**
 * Mock devices for testing in browser (without pywebview)
 */
const MOCK_DEVICES: Device[] = [
  {
    device_id: 'mock_device_1',
    model: 'SM-M205G',
    adb_status: 'online',
    state: 'online',
    fps: 30,
    max_size: 800,
    is_streaming: false,
    is_online: true,
    can_connect: true,
    error: null,
  },
  {
    device_id: 'mock_device_2',
    model: 'Pixel 5',
    adb_status: 'online',
    state: 'streaming',
    fps: 60,
    max_size: 1080,
    is_streaming: true,
    is_online: true,
    can_connect: false,
    error: null,
  },
  {
    device_id: 'mock_device_3',
    model: 'OnePlus 8',
    adb_status: 'unauthorized',
    state: 'unauthorized',
    fps: 30,
    max_size: 800,
    is_streaming: false,
    is_online: false,
    can_connect: false,
    error: null,
  },
];

// =============================================================================
// HOOK
// =============================================================================

/**
 * Hook to access monitoring bridge API
 *
 * Returns a MonitoringBridge object with type-safe methods.
 * Falls back to mock data when running in browser without pywebview.
 *
 * @returns MonitoringBridge object
 *
 * @example
 * ```tsx
 * function MyComponent() {
 *   const bridge = useMonitoringBridge();
 *   const [devices, setDevices] = useState<Device[]>([]);
 *
 *   useEffect(() => {
 *     bridge.getDevices().then(setDevices);
 *   }, []);
 *
 *   const handleConnect = async (deviceId: string) => {
 *     const result = await bridge.connect(deviceId);
 *     if (result.success) {
 *       console.log("Connected!");
 *     }
 *   };
 * }
 * ```
 */
export function useMonitoringBridge(): MonitoringBridge {
  // Check if pywebview is available
  const isAvailable = useMemo(() => {
    return typeof window !== 'undefined' && !!window.pywebview?.api;
  }, []);

  // Get API reference (may be undefined in browser)
  const api = useMemo(() => {
    return window.pywebview?.api;
  }, []);

  // =========================================================================
  // DEVICE LIST METHODS
  // =========================================================================

  const getDevices = useCallback(async (): Promise<Device[]> => {
    if (!api) {
      console.log('[MonitoringBridge] Using mock data (no pywebview)');
      return MOCK_DEVICES;
    }

    try {
      return await api.monitoring_get_devices();
    } catch (error) {
      console.error('[MonitoringBridge] getDevices error:', error);
      return [];
    }
  }, [api]);

  const getDevice = useCallback(
    async (deviceId: string): Promise<Device | null> => {
      if (!api) {
        return MOCK_DEVICES.find((d) => d.device_id === deviceId) || null;
      }

      try {
        return await api.monitoring_get_device(deviceId);
      } catch (error) {
        console.error('[MonitoringBridge] getDevice error:', error);
        return null;
      }
    },
    [api]
  );

  const refreshDevices = useCallback(async (): Promise<Device[]> => {
    if (!api) {
      return MOCK_DEVICES;
    }

    try {
      return await api.monitoring_refresh_devices();
    } catch (error) {
      console.error('[MonitoringBridge] refreshDevices error:', error);
      return [];
    }
  }, [api]);

  // =========================================================================
  // DEVICE CONTROL METHODS
  // =========================================================================

  const connect = useCallback(
    async (deviceId: string): Promise<ConnectResult> => {
      if (!api) {
        // Mock: toggle streaming state
        console.log('[MonitoringBridge] Mock connect:', deviceId);
        return { success: true, pid: 12345 };
      }

      try {
        return await api.monitoring_connect_device(deviceId);
      } catch (error) {
        console.error('[MonitoringBridge] connect error:', error);
        return { success: false, error: String(error) };
      }
    },
    [api]
  );

  const disconnect = useCallback(
    async (deviceId: string): Promise<ApiResult> => {
      if (!api) {
        console.log('[MonitoringBridge] Mock disconnect:', deviceId);
        return { success: true };
      }

      try {
        return await api.monitoring_disconnect_device(deviceId);
      } catch (error) {
        console.error('[MonitoringBridge] disconnect error:', error);
        return { success: false, error: String(error) };
      }
    },
    [api]
  );

  const disconnectAll = useCallback(async (): Promise<DisconnectAllResult> => {
    if (!api) {
      console.log('[MonitoringBridge] Mock disconnectAll');
      return { success: true, count: MOCK_DEVICES.length };
    }

    try {
      return await api.monitoring_disconnect_all();
    } catch (error) {
      console.error('[MonitoringBridge] disconnectAll error:', error);
      return { success: false, error: String(error) };
    }
  }, [api]);

  // =========================================================================
  // SETTINGS METHODS
  // =========================================================================

  const setFps = useCallback(
    async (deviceId: string, fps: number): Promise<SetFpsResult> => {
      if (!api) {
        console.log('[MonitoringBridge] Mock setFps:', deviceId, fps);
        return { success: true, fps };
      }

      try {
        return await api.monitoring_set_fps(deviceId, fps);
      } catch (error) {
        console.error('[MonitoringBridge] setFps error:', error);
        return { success: false, error: String(error) };
      }
    },
    [api]
  );

  const setSize = useCallback(
    async (deviceId: string, maxSize: number): Promise<SetSizeResult> => {
      if (!api) {
        console.log('[MonitoringBridge] Mock setSize:', deviceId, maxSize);
        return { success: true, max_size: maxSize };
      }

      try {
        return await api.monitoring_set_size(deviceId, maxSize);
      } catch (error) {
        console.error('[MonitoringBridge] setSize error:', error);
        return { success: false, error: String(error) };
      }
    },
    [api]
  );

  const setSettings = useCallback(
    async (deviceId: string, fps?: number, maxSize?: number): Promise<ApiResult> => {
      if (!api) {
        console.log('[MonitoringBridge] Mock setSettings:', deviceId, fps, maxSize);
        return { success: true };
      }

      try {
        return await api.monitoring_set_settings(deviceId, fps, maxSize);
      } catch (error) {
        console.error('[MonitoringBridge] setSettings error:', error);
        return { success: false, error: String(error) };
      }
    },
    [api]
  );

  // =========================================================================
  // STATS METHODS
  // =========================================================================

  const getStats = useCallback(async (): Promise<MonitoringStats> => {
    if (!api) {
      return {
        device_count: MOCK_DEVICES.length,
        streaming_count: MOCK_DEVICES.filter((d) => d.is_streaming).length,
        is_running: true,
      };
    }

    try {
      return await api.monitoring_get_stats();
    } catch (error) {
      console.error('[MonitoringBridge] getStats error:', error);
      return { device_count: 0, streaming_count: 0, is_running: false };
    }
  }, [api]);

  // =========================================================================
  // RETURN BRIDGE OBJECT
  // =========================================================================

  return useMemo(
    () => ({
      // Device list
      getDevices,
      getDevice,
      refreshDevices,

      // Device control
      connect,
      disconnect,
      disconnectAll,

      // Settings
      setFps,
      setSize,
      setSettings,

      // Stats
      getStats,

      // Helper
      isAvailable,
    }),
    [
      getDevices,
      getDevice,
      refreshDevices,
      connect,
      disconnect,
      disconnectAll,
      setFps,
      setSize,
      setSettings,
      getStats,
      isAvailable,
    ]
  );
}

export default useMonitoringBridge;
