import pandas as pd

all_devices_file = "all_devices_classa.csv"  
ip_pid_file = "ip_pid.csv"           
output_file = "all_devices_with_pid.csv"  
all_devices_df = pd.read_csv(all_devices_file)
ip_pid_df = pd.read_csv(ip_pid_file)

all_devices_df['ip'] = all_devices_df['ip'].astype(str)
ip_pid_df['ip'] = ip_pid_df['ip'].astype(str)  # Use 'ip' if the column is named 'ip'

# Merge the DataFrames
merged_df = pd.merge(all_devices_df, ip_pid_df[['p-id', 'ip']], how='left', left_on='ip', right_on='ip')

merged_df.to_csv(output_file, index=False)

print(f"P-ID column added successfully. Output saved to {output_file}")