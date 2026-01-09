/**
 * Update Service
 * Interface with Python update bridge for version checking and updates
 */

interface UpdateCheckResponse {
  success: boolean;
  has_update?: boolean;
  current_version?: string;
  latest_version?: string;
  download_url?: string;
  changelog?: string;
  release_date?: string;
  error?: string;
}

interface VersionResponse {
  success: boolean;
  version?: string;
  build_date?: string;
  changelog?: string;
  error?: string;
}

interface UpdateInstallResponse {
  success: boolean;
  message?: string;
  error?: string;
}

class UpdateService {
  /**
   * Get current app version
   */
  async getCurrentVersion(): Promise<VersionResponse> {
    try {
      if (!window.pywebview?.api) {
        return { success: false, error: 'PyWebView API not available' };
      }

      const response = await window.pywebview.api.update_get_current_version();
      return response;
    } catch (error) {
      console.error('Error getting current version:', error);
      return { success: false, error: String(error) };
    }
  }

  /**
   * Check for updates from GitHub
   */
  async checkForUpdates(): Promise<UpdateCheckResponse> {
    try {
      if (!window.pywebview?.api) {
        return { success: false, error: 'PyWebView API not available' };
      }

      const response = await window.pywebview.api.update_check_for_updates();
      return response;
    } catch (error) {
      console.error('Error checking for updates:', error);
      return { success: false, error: String(error) };
    }
  }

  /**
   * Download and install update
   */
  async downloadAndInstall(downloadUrl: string): Promise<UpdateInstallResponse> {
    try {
      if (!window.pywebview?.api) {
        return { success: false, error: 'PyWebView API not available' };
      }

      const response = await window.pywebview.api.update_download_and_install_update(downloadUrl);
      return response;
    } catch (error) {
      console.error('Error downloading update:', error);
      return { success: false, error: String(error) };
    }
  }
}

export const updateService = new UpdateService();
export type { UpdateCheckResponse, VersionResponse, UpdateInstallResponse };
