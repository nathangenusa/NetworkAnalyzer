import psutil
import time

def monitor_network_activity(interval=30):
    print("Monitoring network activity for {} seconds...".format(interval))

    # Initial network stats
    initial_stats = psutil.net_io_counters(pernic=True)

    # Wait for the specified interval
    time.sleep(interval)

    # Final network stats after the interval
    final_stats = psutil.net_io_counters(pernic=True)

    # Calculate and print the network activity for each connection
    for nic, stats in final_stats.items():
        initial = initial_stats[nic]
        sent = stats.bytes_sent - initial.bytes_sent
        received = stats.bytes_recv - initial.bytes_recv
        print(f"\nNIC: {nic}")
        print(f"Bytes Sent: {sent}")
        print(f"Bytes Received: {received}")

# Main execution
if __name__ == "__main__":
    monitor_network_activity()
