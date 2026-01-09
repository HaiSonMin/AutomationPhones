/**
 * TypeScript interfaces for Device Monitoring feature
 *
 * These types mirror the Python data structures returned by the MonitoringBridge.
 * Keep in sync with src/bridge/monitoring/monitoring.py
 */

// =============================================================================
// DEVICE STATE - Matches Python's DeviceState enum
// =============================================================================

/**
 * Possible device states
 *
 * These map to the Python DeviceState enum values:
 * - disconnected: Not connected via USB
 * - unauthorized: Connected but USB debugging not authorized
 * - offline: Connected but ADB reports offline
 * - online: Ready to stream (not currently streaming)
 * - connecting: Starting scrcpy process
 * - streaming: Actively streaming screen
 * - error: An error occurred
 */
export type DeviceState =
  | 'disconnected'
  | 'unauthorized'
  | 'offline'
  | 'online'
  | 'connecting'
  | 'streaming'
  | 'error';

// =============================================================================
// DEVICE - Main device interface
// =============================================================================

/**
 * Device information returned by the monitoring bridge
 *
 * This interface matches the Python ManagedDevice.to_dict() output.
 */
export interface Device {
  /** ADB device serial number (e.g., "abc123" or "192.168.1.1:5555") */
  device_id: string;

  /** Device model name (e.g., "SM-M205G", "Pixel 5") */
  model: string;

  /** ADB connection status */
  adb_status: 'online' | 'offline' | 'unauthorized' | 'bootloader' | 'recovery' | 'unknown';

  /** Current device state (combines ADB status and streaming state) */
  state: DeviceState;

  /** Current FPS setting (1-120) */
  fps: number;

  /** Current max size setting (0=original, 480-2048) */
  max_size: number;

  /** Whether device is currently streaming */
  is_streaming: boolean;

  /** Whether device is online (ADB status = online) */
  is_online: boolean;

  /** Whether device can be connected (online and not streaming) */
  can_connect: boolean;

  /** Error message if state is "error", null otherwise */
  error: string | null;
}

// =============================================================================
// API RESULT - Response from bridge methods
// =============================================================================

/**
 * Result from bridge API calls
 *
 * All bridge methods return this structure.
 */
export interface ApiResult {
  /** Whether the operation succeeded */
  success: boolean;

  /** Error message if failed */
  error?: string;

  /** Additional data (varies by method) */
  [key: string]: unknown;
}

/**
 * Result from connect_device
 */
export interface ConnectResult extends ApiResult {
  /** Process ID of the scrcpy process (if successful) */
  pid?: number;
}

/**
 * Result from set_fps
 */
export interface SetFpsResult extends ApiResult {
  /** The actual FPS set (may be clamped) */
  fps?: number;
}

/**
 * Result from set_size
 */
export interface SetSizeResult extends ApiResult {
  /** The actual size set */
  max_size?: number;
}

/**
 * Result from disconnect_all
 */
export interface DisconnectAllResult extends ApiResult {
  /** Number of devices disconnected */
  count?: number;
}

/**
 * Monitoring statistics
 */
export interface MonitoringStats {
  /** Total devices tracked */
  device_count: number;

  /** Devices currently streaming */
  streaming_count: number;

  /** Whether manager is active */
  is_running: boolean;
}

// =============================================================================
// EVENTS - Custom events from Python
// =============================================================================

/**
 * Event detail for 'monitoring-devices-changed' custom event
 *
 * Python pushes this event when the device list changes.
 * Listen for it with:
 *   window.addEventListener('monitoring-devices-changed', handler);
 */
export interface DevicesChangedEventDetail {
  devices: Device[];
}

/**
 * Custom event with device change data
 */
export interface DevicesChangedEvent extends CustomEvent<DevicesChangedEventDetail> {
  type: 'monitoring-devices-changed';
}

// =============================================================================
// UI STATE - For React components
// =============================================================================

/**
 * Device card props
 */
export interface DeviceCardProps {
  /** Device data */
  device: Device;

  /** Display index (1-based) */
  index: number;

  /** Callback when device state changes */
  onRefresh?: () => void;
}

/**
 * Slider change handler
 */
export type SliderChangeHandler = (value: number) => void;

/**
 * FPS preset options for quick selection
 */
export const FPS_PRESETS = [10, 15, 30, 60] as const;
export type FpsPreset = (typeof FPS_PRESETS)[number];

/**
 * Size preset options for quick selection
 */
export const SIZE_PRESETS = [
  { value: 480, label: '480p' },
  { value: 720, label: '720p' },
  { value: 800, label: '800p' },
  { value: 1080, label: '1080p' },
  { value: 1440, label: '1440p' },
] as const;

// =============================================================================
// PYWEBVIEW BRIDGE - Type definitions for monitoring API
// =============================================================================

/**
 * Monitoring bridge API available on window.pywebview.api
 *
 * These methods are prefixed with 'monitoring_' by BridgeRegistry.
 * Note: The actual Window interface augmentation is in src/types/pywebview.d.ts
 */
export interface MonitoringBridgeApi {
  // Device list
  monitoring_get_devices(): Promise<Device[]>;
  monitoring_get_device(device_id: string): Promise<Device | null>;
  monitoring_refresh_devices(): Promise<Device[]>;

  // Device control
  monitoring_connect_device(device_id: string): Promise<ConnectResult>;
  monitoring_disconnect_device(device_id: string): Promise<ApiResult>;
  monitoring_disconnect_all(): Promise<DisconnectAllResult>;

  // Settings
  monitoring_set_fps(device_id: string, fps: number): Promise<SetFpsResult>;
  monitoring_set_size(device_id: string, max_size: number): Promise<SetSizeResult>;
  monitoring_set_settings(device_id: string, fps?: number, max_size?: number): Promise<ApiResult>;

  // Stats
  monitoring_get_stats(): Promise<MonitoringStats>;
}
