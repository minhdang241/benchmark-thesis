"""
Background resource monitor — samples CPU and memory at regular intervals
during inference. Runs in a separate thread.
"""

import threading
import time
import psutil


class ResourceMonitor:
    """Monitors CPU utilisation, memory usage, and optionally network bytes
    for a specific process (by PID) or system-wide."""

    def __init__(self, interval: float = 0.5):
        self.interval = interval
        self._stop_event = threading.Event()
        self._thread = None

        self.cpu_samples = []       # system-wide CPU % per sample
        self.mem_samples_mb = []    # RSS of target process in MB
        self.net_rx_bytes = []      # cumulative RX bytes snapshots
        self.net_tx_bytes = []      # cumulative TX bytes snapshots
        self._pid = None

    # ----------------------------------------------------------
    # Sampling loop
    # ----------------------------------------------------------
    def _sample_loop(self):
        process = psutil.Process(self._pid) if self._pid else None
        # Prime the per-interval CPU measurement
        psutil.cpu_percent(interval=None)

        while not self._stop_event.is_set():
            time.sleep(self.interval)

            # CPU (system-wide, non-blocking — uses delta since last call)
            self.cpu_samples.append(psutil.cpu_percent(interval=None))

            # Memory — RSS of target process
            if process:
                try:
                    rss_mb = process.memory_info().rss / (1024 * 1024)
                    self.mem_samples_mb.append(rss_mb)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            # Network — system-wide cumulative bytes
            net = psutil.net_io_counters()
            self.net_rx_bytes.append(net.bytes_recv)
            self.net_tx_bytes.append(net.bytes_sent)

    # ----------------------------------------------------------
    # Public interface
    # ----------------------------------------------------------
    def start(self, pid: int = None):
        """Begin sampling. Optionally track a specific PID for memory."""
        self._pid = pid
        self.cpu_samples.clear()
        self.mem_samples_mb.clear()
        self.net_rx_bytes.clear()
        self.net_tx_bytes.clear()
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._sample_loop, daemon=True)
        self._thread.start()

    def stop(self) -> dict:
        """Stop sampling and return aggregated metrics."""
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=5)

        result = {
            "avg_cpu_pct": 0.0,
            "max_cpu_pct": 0.0,
            "peak_mem_mb": 0.0,
            "avg_mem_mb": 0.0,
            "net_rx_mb": 0.0,
            "net_tx_mb": 0.0,
        }

        if self.cpu_samples:
            result["avg_cpu_pct"] = round(sum(self.cpu_samples) / len(self.cpu_samples), 2)
            result["max_cpu_pct"] = round(max(self.cpu_samples), 2)

        if self.mem_samples_mb:
            result["peak_mem_mb"] = round(max(self.mem_samples_mb), 2)
            result["avg_mem_mb"] = round(sum(self.mem_samples_mb) / len(self.mem_samples_mb), 2)

        if len(self.net_rx_bytes) >= 2:
            result["net_rx_mb"] = round((self.net_rx_bytes[-1] - self.net_rx_bytes[0]) / (1024 * 1024), 4)
            result["net_tx_mb"] = round((self.net_tx_bytes[-1] - self.net_tx_bytes[0]) / (1024 * 1024), 4)

        return result
