To integrate this function, add the following into the code:
```
from rules_engine import shipping_estimates as se_rules

# Example data
dest_country = "PT"
weight = 2
dim_lwh = (20, 30, 40)

# Function call to fetch shipping estimates.
estimates = se_rules.get_shipping_estimates(dest_country, weight, weight_unit="kg", dim_lwh=dim_lwh, dim_unit="cm")
```
- Required parameters: `dest_country` and `weight`
- Optional parameters: `weight_unit`, `dim_lwh` and `dim_unit`
- `weight_unit` can be `lbs` or `kg` (default).
- `dim_unit` can be `in` or `cm` (default).

Sample output:
```
[{'Service Provider': 'FedEx',
  'Service': 'International Priority Express (IPE)',
  'Estimated Rate': 311.9,
  'Estimated Transit Time': (1, 3),
  'Other Remarks': 'All rates are exclusive of all applicable tax. For special fees and fuel surcharge, please refer to the Surcharge and Other Information page for details.',
  'Insurance': 'Yes',
  'Re Delivery': 3,
  'Home Pick Up': 'Yes'},
 {'Service Provider': 'DHL',
  'Service': 'DHL Express Worldwide',
  'Estimated Rate': 153.89,
  'Estimated Transit Time': (1, 2),
  'Other Remarks': 'Rates only for shipping Documents',
  'Insurance': 'No',
  'Re Delivery': 2,
  'Home Pick Up': 'No'},
 {'Service Provider': 'SingPost',
  'Service': 'Speedpost Economy Package',
  'Estimated Rate': 80.0,
  'Estimated Transit Time': (21, 105),
  'Other Remarks': '',
  'Insurance': 'Yes',
  'Re Delivery': 2,
  'Home Pick Up': 'Yes'}]
  ```
