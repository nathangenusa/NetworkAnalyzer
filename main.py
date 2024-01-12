import psutil
import time
import threading
import tkinter as tk
from tkinter import scrolledtext, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class NetworkMonitor:
    def __init__(self, root):
        self.root = root
        self.is_monitoring = False
        self.monitor_thread = None
        self.log_file_path = ""
        self.dark_mode = False
        self.setup_graph()  # Initialize the graph before setting up the GUI
        self.setup_gui()


    def setup_gui(self):
        self.root.title("Network Activity Monitor")

        # File path entry
        self.filepath_entry = tk.Entry(self.root, width=50)
        self.filepath_entry.grid(row=0, column=0, padx=10, pady=10)

        # Save Button
        save_button = tk.Button(self.root, text="Save File Path", command=self.set_file_path)
        save_button.grid(row=0, column=1, padx=10, pady=10)

        # Start and Stop Buttons
        start_button = tk.Button(self.root, text="Start Logging", command=self.start_monitoring)
        start_button.grid(row=1, column=0, padx=10, pady=10)

        stop_button = tk.Button(self.root, text="Stop Logging", command=self.stop_monitoring)
        stop_button.grid(row=1, column=1, padx=10, pady=10)

        # Text Area
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=60, height=15)
        self.text_area.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Theme Toggle Button
        self.theme_button = tk.Button(self.root, text="Toggle Theme", command=self.toggle_theme)
        self.theme_button.grid(row=3, column=0, padx=10, pady=10)

        # Configure initial theme
        self.configure_theme()

    def setup_graph(self):
        self.fig, self.ax = plt.subplots()
        self.graph = FigureCanvasTkAgg(self.fig, master=self.root)
        self.graph.get_tk_widget().grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def update_graph(self, nic_data):
        self.ax.clear()
        nics = list(nic_data.keys())
        sent_values = [data['sent'] for data in nic_data.values()]
        received_values = [data['received'] for data in nic_data.values()]

        self.ax.bar(nics, sent_values, label='Bytes Sent')
        self.ax.bar(nics, received_values, bottom=sent_values, label='Bytes Received')
        self.ax.legend()
        self.fig.canvas.draw()

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.configure_theme()

    def configure_theme(self):
        # Set colors for dark or light mode
        bg_color = "gray" if self.dark_mode else "white"  # updated color name
        fg_color = "white" if self.dark_mode else "black"

        # Apply colors to widgets
        self.root.configure(background=bg_color)
        self.filepath_entry.configure(bg=bg_color, fg=fg_color)
        self.text_area.configure(bg=bg_color, fg=fg_color)
        self.theme_button.configure(bg=bg_color, fg=fg_color)

        # Update graph colors
        self.fig.patch.set_facecolor(bg_color)
        self.ax.set_facecolor(bg_color)
        self.ax.xaxis.label.set_color(fg_color)
        self.ax.yaxis.label.set_color(fg_color)
        self.ax.tick_params(colors=fg_color)
        for spine in self.ax.spines.values():  # Update spines color
            spine.set_color(fg_color)

    def set_file_path(self):
        self.log_file_path = self.filepath_entry.get()

    def log_network_activity(self, nic, sent, received):
        if self.log_file_path:
            try:
                with open(self.log_file_path, "a") as file:
                    file.write(f"{time.ctime()}: NIC: {nic}, Bytes Sent: {sent}, Bytes Received: {received}\n")
            except Exception as e:
                print(f"Error writing to file: {e}")

    def monitor_network_activity(self):
        initial_stats = psutil.net_io_counters(pernic=True)
        nic_data = {}
        while self.is_monitoring:
            time.sleep(1)
            final_stats = psutil.net_io_counters(pernic=True)
            for nic, stats in final_stats.items():
                if nic in initial_stats:
                    initial = initial_stats[nic]
                    sent = stats.bytes_sent - initial.bytes_sent
                    received = stats.bytes_recv - initial.bytes_recv
                    log_message = f"NIC: {nic}, Bytes Sent: {sent}, Bytes Received: {received}"
                    self.text_area.insert(tk.END, f"\n{log_message}")
                    self.log_network_activity(nic, sent, received)
                    nic_data[nic] = {'sent': sent, 'received': received}
            initial_stats = final_stats

            # Update graph
            self.update_graph(nic_data)

    def start_monitoring(self):
        if not self.is_monitoring:
            self.is_monitoring = True
            self.monitor_thread = threading.Thread(target=self.monitor_network_activity, daemon=True)
            self.monitor_thread.start()

    def stop_monitoring(self):
        self.is_monitoring = False


if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkMonitor(root)
    root.mainloop()