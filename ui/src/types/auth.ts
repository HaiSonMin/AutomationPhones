export interface PyWebViewAPI {
  // Auth Bridge - Python saves token to keyring
  on_login_success: (token: string, user: User) => Promise<BridgeResponse>;
  on_logout: () => Promise<BridgeResponse>;
  get_token: () => Promise<TokenResponse>;
  get_current_user: () => Promise<UserResponse>;
  is_authenticated: () => Promise<AuthResponse>;
}

export interface BridgeResponse {
  success: boolean;
  message?: string;
  error?: string;
}

export interface TokenResponse {
  success: boolean;
  token: string | null;
}

export interface UserResponse {
  success: boolean;
  user: User | null;
}

export interface AuthResponse {
  success: boolean;
  authenticated: boolean;
}

export interface User {
  id: string;
  user_fullName: string;
  user_email: string;
  user_userName: string;
  [key: string]: any;
}
