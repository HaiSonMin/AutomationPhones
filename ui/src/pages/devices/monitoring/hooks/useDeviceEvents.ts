/**
 * useDeviceEvents - Hook for listening to device change events from Python
 *
 * Python pushes 'monitoring-devices-changed' events when devices connect,
 * disconnect, or change state. This hook handles subscribing to those events.
 *
 * Usage:
 *   useDeviceEvents((devices) => {
 *     setDevices(devices);
 *   });
 */

import { useEffect, useCallback, useRef } from 'react';
import type { Device, DevicesChangedEvent } from '../types/monitoring.types';

// =============================================================================
// TYPES
// =============================================================================

/**
 * Callback when devices change
 */
export type DevicesChangedCallback = (devices: Device[]) => void;

/**
 * Options for the hook
 */
export interface UseDeviceEventsOptions {
  /** Whether to enable event listening (default: true) */
  enabled?: boolean;

  /** Debounce delay in ms (default: 100) */
  debounceMs?: number;
}

// =============================================================================
// HOOK
// =============================================================================

/**
 * Hook to listen for device change events from Python
 *
 * Subscribes to 'monitoring-devices-changed' CustomEvent that Python
 * dispatches via window.evaluate_js().
 *
 * @param onDevicesChanged - Callback when devices change
 * @param options - Hook options
 *
 * @example
 * ```tsx
 * function DeviceList() {
 *   const [devices, setDevices] = useState<Device[]>([]);
 *
 *   // Auto-update when Python sends events
 *   useDeviceEvents(setDevices);
 *
 *   return <div>{devices.map(...)}</div>;
 * }
 * ```
 */
export function useDeviceEvents(
  onDevicesChanged: DevicesChangedCallback,
  options: UseDeviceEventsOptions = {}
): void {
  const { enabled = true, debounceMs = 100 } = options;

  // Store callback in ref to avoid re-subscribing on every render
  const callbackRef = useRef(onDevicesChanged);
  callbackRef.current = onDevicesChanged;

  // Debounce timer ref
  const timerRef = useRef<number | null>(null);

  // Event handler
  const handleDevicesChanged = useCallback(
    (event: Event) => {
      const customEvent = event as DevicesChangedEvent;
      const devices = customEvent.detail?.devices;

      if (!Array.isArray(devices)) {
        console.warn('[useDeviceEvents] Invalid event data:', customEvent.detail);
        return;
      }

      // Debounce to prevent rapid updates
      if (timerRef.current !== null) {
        window.clearTimeout(timerRef.current);
      }

      timerRef.current = window.setTimeout(() => {
        callbackRef.current(devices);
        timerRef.current = null;
      }, debounceMs);
    },
    [debounceMs]
  );

  // Subscribe to events
  useEffect(() => {
    if (!enabled) {
      return;
    }

    console.log('[useDeviceEvents] Subscribing to device events');
    window.addEventListener('monitoring-devices-changed', handleDevicesChanged);

    return () => {
      console.log('[useDeviceEvents] Unsubscribing from device events');
      window.removeEventListener('monitoring-devices-changed', handleDevicesChanged);

      // Clear any pending debounce timer
      if (timerRef.current !== null) {
        window.clearTimeout(timerRef.current);
      }
    };
  }, [enabled, handleDevicesChanged]);
}

export default useDeviceEvents;
