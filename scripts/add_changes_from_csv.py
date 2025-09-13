import pandas as pd

all_devices_file = "all_devices_with_pid.csv"  
pid_ip_file = "pid_ip_mapping.csv"            
output_file = "all_devices_updated.csv"       

all_devices_df = pd.read_csv(all_devices_file)
pid_ip_df = pd.read_csv(pid_ip_file, header=None, names=["P-ID", "Category", "Updated_IP"])


merged_df = pd.merge(all_devices_df, pid_ip_df[["P-ID", "Updated_IP"]], how="left", on="P-ID")
merged_df["ip"] = merged_df["Updated_IP"].combine_first(merged_df["ip"])
merged_df.drop(columns=["Updated_IP"], inplace=True)
merged_df.to_csv(output_file, index=False)

print(f"IP column updated successfully. Output saved to {output_file}")