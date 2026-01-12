# Overviews Component

## Usage

```tsx
import { Overviews } from '../components';

// Basic usage
<Overviews 
  data={{
    total: 100,
    active: 75,
    inactive: 25,
  }}
  title="Device Statistics"
/>

// With custom card configurations
<Overviews 
  data={{
    total: 100,
    active: 75,
    inactive: 25,
    pending: 10,
  }}
  title="Device Statistics"
  cardConfigs={{
    total: { title: 'Total Devices', color: '#1890ff', icon: <DeviceIcon /> },
    active: { title: 'Active Devices', color: '#52c41a', icon: <CheckIcon /> },
    inactive: { title: 'Inactive Devices', color: '#ff4d4f', icon: <CloseIcon /> },
    pending: { title: 'Pending Devices', color: '#faad14', icon: <ClockIcon /> },
  }}
  collapsible={true}
  defaultCollapsed={false}
/>
```

## Props

- `data`: Object with key-value pairs where key is the card identifier and value is the number to display
- `title`: Section title (default: "Statistics Overview")
- `collapsible`: Whether the section can be collapsed (default: true)
- `defaultCollapsed`: Initial collapsed state (default: false)
- `cardConfigs`: Custom configuration for each card (title, color, icon)
