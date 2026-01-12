import { useState } from 'react';
import { Layout, theme } from 'antd';
import Header from '../components/header/Header';
// import Footer from '../components/footer/Footer';
import Sidebar from '../components/sidebar/Sidebar';
import { useAuthStore } from '../stores/authStore';
import { useThemeStore } from '../stores/themeStore';

const { Content, Sider } = Layout;

interface DashboardLayoutProps {
  children: React.ReactNode;
}

const DashboardLayout: React.FC<DashboardLayoutProps> = ({ children }) => {
  const { user } = useAuthStore();
  const { mode: themeMode } = useThemeStore();
  const [collapsed, setCollapsed] = useState(false);
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  const isDark = themeMode === 'dark';

  return (
    <Layout style={{ minHeight: '100vh', background: isDark ? '#141414' : '#f0f2f5' }}>
      <Sider
        trigger={null}
        collapsible
        collapsed={collapsed}
        width={250}
        collapsedWidth={80}
        style={{
          background: isDark ? '#1f1f1f' : '#ffffff',
        }}
      >
        <div
          style={{
            height: '64px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            background: isDark ? 'rgba(255, 255, 255, 0.08)' : '#f8f9fa',
            borderBottom: isDark ? '1px solid rgba(255, 255, 255, 0.1)' : '1px solid #e8e8e8',
          }}
        >
          <h1
            style={{
              color: isDark ? '#fff' : '#262626',
              margin: 0,
              fontSize: collapsed ? '16px' : '20px',
            }}
          >
            {collapsed ? '📱' : '📱 Tool Socials'}
          </h1>
        </div>
        <Sidebar collapsed={collapsed} />
      </Sider>
      <Layout style={{ background: isDark ? '#141414' : '#f0f2f5' }}>
        <Header
          collapsed={collapsed}
          onToggle={() => setCollapsed(!collapsed)}
          user={
            user
              ? {
                  name: user.user_fullName || '',
                  email: user.user_email || '',
                }
              : undefined
          }
        />
        <Content
          style={{
            margin: '24px',
            padding: 24,
            minHeight: 280,
            background: colorBgContainer,
            borderRadius: borderRadiusLG,
            boxShadow: isDark
              ? '0 1px 3px rgba(0,0,0,0.4)'
              : '0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)',
          }}
        >
          {children}
        </Content>
        {/* <Footer /> */}
      </Layout>
    </Layout>
  );
};

export default DashboardLayout;
