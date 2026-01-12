# Filters Component

## Usage

```tsx
import { Filters } from '../components';

const [filterValues, setFilterValues] = useState({});

const handleFilterChange = (key: string, value: any) => {
  setFilterValues(prev => ({ ...prev, [key]: value }));
};

const filterOptions: FilterOption[] = [
  {
    key: 'status',
    label: 'Status',
    type: 'multiSelect',
    options: [
      { label: 'Active', value: 'active' },
      { label: 'Inactive', value: 'inactive' },
      { label: 'Pending', value: 'pending' },
    ],
  },
  {
    key: 'deviceType',
    label: 'Device Type',
    type: 'select',
    options: [
      { label: 'Phone', value: 'phone' },
      { label: 'Tablet', value: 'tablet' },
    ],
  },
  {
    key: 'priceRange',
    label: 'Price Range',
    type: 'range',
    placeholder: 'Enter price range',
  },
  {
    key: 'dateRange',
    label: 'Date Range',
    type: 'dateRange',
  },
];

<Filters
  filters={filterOptions}
  onFilterChange={handleFilterChange}
  onClearAll={() => setFilterValues({})}
  title="Device Filters"
  collapsible={true}
  defaultCollapsed={false}
/>
```

## Filter Types

1. **select**: Single select dropdown
2. **multiSelect**: Multi-select dropdown with checkboxes
3. **range**: Number range input (From - To)
4. **dateRange**: Date range picker

## Props

- `filters`: Array of filter options
- `onFilterChange`: Callback function when filter value changes
- `onClearAll`: Callback function when clear all is clicked
- `title`: Section title (default: "Filters")
- `collapsible`: Whether the section can be collapsed (default: true)
- `defaultCollapsed`: Initial collapsed state (default: false)
