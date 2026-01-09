import { useState, useEffect } from 'react';
import { Card, Row, Col, Typography, Button, Badge, Space, Spin } from 'antd';
import {
  ApiOutlined,
  PlayCircleOutlined,
  CheckCircleOutlined,
  SyncOutlined,
  MobileOutlined,
  ToolOutlined,
  MonitorOutlined,
} from '@ant-design/icons';
import { useThemeStore } from '../../stores/themeStore';

const { Title, Text } = Typography;

interface HealthStatus {
  server: boolean;
  database: boolean;
  devices: number;
  lastCheck: string;
}

interface ServiceStatus {
  id: string;
  name: string;
  status: 'running' | 'stopped' | 'error';
  lastAction: string;
}

const DashboardContent: React.FC = () => {
  const { mode: themeMode } = useThemeStore();
  const isDark = themeMode === 'dark';

  const [loading, setLoading] = useState(true);
  const [healthStatus, setHealthStatus] = useState<HealthStatus>({
    server: false,
    database: false,
    devices: 0,
    lastCheck: '',
  });
  const [services] = useState<ServiceStatus[]>([]);
  const [checkingHealth, setCheckingHealth] = useState(false);

  useEffect(() => {
    // Initial load
    loadDashboardData();

    // Set up periodic health check
    const interval = setInterval(() => {
      checkHealthServer();
    }, 30000); // Check every 30 seconds

    return () => clearInterval(interval);
  }, []);

  const loadDashboardData = async () => {
    try {
      await checkHealthServer();
      // TODO: Load services status
      // await loadServices();
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const checkHealthServer = async () => {
    setCheckingHealth(true);
    try {
      if (!window.pywebview?.api) {
        console.error('PyWebView API not available');
        return;
      }
      const result = await window.pywebview.api.health_check_health_server();
      setHealthStatus(result);
    } catch (error) {
      console.error('Health check failed:', error);
    } finally {
      setCheckingHealth(false);
    }
  };

  const handleStartStop = async () => {
    try {
      if (!window.pywebview?.api) {
        console.error('PyWebView API not available');
        return;
      }
      const result = await window.pywebview.api.tools_start_stop();
      if (result.success) {
        // Update the global app state
        // The services array is not actually used in this implementation
        // since we simplified to a single app state
        console.log(result.message);
      }
    } catch (error) {
      console.error('Failed to toggle start/stop:', error);
    }
  };

  const getStatusColor = (status: boolean) => (status ? '#52c41a' : '#ff4d4f');
  const getServiceBadge = (status: string) => {
    switch (status) {
      case 'running':
        return <Badge status='success' text='Running' />;
      case 'stopped':
        return <Badge status='default' text='Stopped' />;
      case 'error':
        return <Badge status='error' text='Error' />;
      default:
        return <Badge status='default' text='Unknown' />;
    }
  };

  if (loading) {
    return (
      <div
        style={{
          padding: '50px',
          textAlign: 'center',
          background: isDark ? '#141414' : undefined,
        }}
      >
        <Spin size='large' />
      </div>
    );
  }

  return (
    <div>
      <Title level={2}>Dashboard</Title>

      {/* Health Status Cards */}
      <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Space direction='vertical' size='small' style={{ width: '100%' }}>
              <Text type='secondary'>Server Status</Text>
              <Space>
                <ApiOutlined style={{ color: getStatusColor(healthStatus.server) }} />
                <Text strong>{healthStatus.server ? 'Online' : 'Offline'}</Text>
              </Space>
            </Space>
          </Card>
        </Col>

        <Col xs={24} sm={12} md={6}>
          <Card>
            <Space direction='vertical' size='small' style={{ width: '100%' }}>
              <Text type='secondary'>Database</Text>
              <Space>
                <CheckCircleOutlined style={{ color: getStatusColor(healthStatus.database) }} />
                <Text strong>{healthStatus.database ? 'Connected' : 'Disconnected'}</Text>
              </Space>
            </Space>
          </Card>
        </Col>

        <Col xs={24} sm={12} md={6}>
          <Card>
            <Space direction='vertical' size='small' style={{ width: '100%' }}>
              <Text type='secondary'>Connected Devices</Text>
              <Text strong style={{ fontSize: '24px' }}>
                {healthStatus.devices}
              </Text>
            </Space>
          </Card>
        </Col>

        <Col xs={24} sm={12} md={6}>
          <Card>
            <Space direction='vertical' size='small' style={{ width: '100%' }}>
              <Text type='secondary'>Last Check</Text>
              <Text>{healthStatus.lastCheck}</Text>
              <Button
                icon={<SyncOutlined spin={checkingHealth} />}
                size='small'
                onClick={checkHealthServer}
                loading={checkingHealth}
              >
                Refresh
              </Button>
            </Space>
          </Card>
        </Col>
      </Row>

      {/* Quick Actions */}
      <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
        <Col xs={24} sm={12} md={8}>
          <Card hoverable>
            <Space>
              <MobileOutlined style={{ fontSize: '24px', color: '#1890ff' }} />
              <div>
                <Title level={5} style={{ margin: 0 }}>
                  Devices
                </Title>
                <Text type='secondary'>Manage connected devices</Text>
              </div>
            </Space>
          </Card>
        </Col>

        <Col xs={24} sm={12} md={8}>
          <Card hoverable>
            <Space>
              <ToolOutlined style={{ fontSize: '24px', color: '#52c41a' }} />
              <div>
                <Title level={5} style={{ margin: 0 }}>
                  Automation
                </Title>
                <Text type='secondary'>Configure automation scripts</Text>
              </div>
            </Space>
          </Card>
        </Col>

        <Col xs={24} sm={12} md={8}>
          <Card hoverable>
            <Space>
              <MonitorOutlined style={{ fontSize: '24px', color: '#faad14' }} />
              <div>
                <Title level={5} style={{ margin: 0 }}>
                  Monitoring
                </Title>
                <Text type='secondary'>View system logs</Text>
              </div>
            </Space>
          </Card>
        </Col>
      </Row>

      {/* Services Control */}
      <Card title='Services Control' style={{ marginBottom: '24px' }}>
        <Row gutter={[16, 16]}>
          {services.map((service) => (
            <Col xs={24} sm={12} md={8} lg={6} key={service.id}>
              <Card size='small'>
                <Space direction='vertical' style={{ width: '100%' }}>
                  <Text strong>{service.name}</Text>
                  {getServiceBadge(service.status)}
                  <Text type='secondary' style={{ fontSize: '12px' }}>
                    Last action: {service.lastAction}
                  </Text>
                  <Space>
                    <Button icon={<PlayCircleOutlined />} size='small' onClick={handleStartStop}>
                      Start/Stop
                    </Button>
                  </Space>
                </Space>
              </Card>
            </Col>
          ))}
        </Row>
      </Card>

      {/* Recent Activity */}
      <Card title='Recent Activity'>
        <Text type='secondary'>Activity logs will be displayed here...</Text>
      </Card>
    </div>
  );
};

export default DashboardContent;
