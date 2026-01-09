/**
 * Global type declarations for pywebview API
 * This file provides TypeScript definitions for the Python API exposed through pywebview
 *
 * According to pywebview docs, methods are exposed as window.pywebview.api.method_name
 * Updated: Force TS refresh
 */

declare global {
  interface Window {
    pywebview: {
      api: {
        // Auth API - methods are prefixed with auth_
        auth_on_login_success: (
          token: string,
          user: any
        ) => Promise<{
          success: boolean;
          message: string;
        }>;
        auth_on_logout: () => Promise<{
          success: boolean;
          message: string;
        }>;
        auth_is_authenticated: () => Promise<{
          authenticated: boolean;
        }>;
        auth_get_token: () => Promise<{
          success: boolean;
          token: string;
        }>;
        auth_get_current_user: () => Promise<{
          success: boolean;
          user: any;
        }>;

        // Health API
        health_check_health_server: () => Promise<{
          server: boolean;
          database: boolean;
          devices: number;
          lastCheck: string;
        }>;

        // Tools API
        tools_start_stop: () => Promise<{
          success: boolean;
          message: string;
          running: boolean;
        }>;
        tools_get_app_state: () => Promise<{
          running: boolean;
        }>;

        // Update API
        update_get_current_version: () => Promise<{
          success: boolean;
          version?: string;
          build_date?: string;
          changelog?: string;
          error?: string;
        }>;
        update_check_for_updates: () => Promise<{
          success: boolean;
          has_update?: boolean;
          current_version?: string;
          latest_version?: string;
          download_url?: string;
          changelog?: string;
          release_date?: string;
          error?: string;
        }>;
        update_download_and_install_update: (downloadUrl: string) => Promise<{
          success: boolean;
          message?: string;
          error?: string;
        }>;

        // Monitoring API
        monitoring_get_devices: () => Promise<any[]>;
        monitoring_get_device: (device_id: string) => Promise<any | null>;
        monitoring_refresh_devices: () => Promise<any[]>;
        monitoring_connect_device: (device_id: string) => Promise<{
          success: boolean;
          message?: string;
          error?: string;
        }>;
        monitoring_disconnect_device: (device_id: string) => Promise<{
          success: boolean;
          message?: string;
          error?: string;
        }>;
        monitoring_disconnect_all: () => Promise<{
          success: boolean;
          message?: string;
          error?: string;
          disconnected_count?: number;
        }>;
        monitoring_set_fps: (
          device_id: string,
          fps: number
        ) => Promise<{
          success: boolean;
          message?: string;
          error?: string;
        }>;
        monitoring_set_size: (
          device_id: string,
          max_size: number
        ) => Promise<{
          success: boolean;
          message?: string;
          error?: string;
        }>;
        monitoring_set_settings: (
          device_id: string,
          fps?: number,
          max_size?: number
        ) => Promise<{
          success: boolean;
          message?: string;
          error?: string;
        }>;
        monitoring_get_stats: () => Promise<{
          total_devices: number;
          connected_devices: number;
          monitoring_active: boolean;
          total_fps: number;
          [key: string]: any;
        }>;
      };
    };
  }
}

// Ensure this is treated as a module
export {};
