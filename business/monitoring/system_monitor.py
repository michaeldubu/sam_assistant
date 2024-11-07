# business/monitoring/system_monitor.py
import psutil
import GPUtil
from datetime import datetime
from dataclasses import dataclass
import asyncio

@dataclass
class SystemMetrics:
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_speed: float
    gpu_usage: Optional[float]
    timestamp: datetime

class SystemMonitor:
    def __init__(self):
        self.metrics_history = []
        self.monitoring = False
        
    async def start_monitoring(self):
        """Start system monitoring"""
        self.monitoring = True
        while self.monitoring:
            metrics = self.gather_metrics()
            self.metrics_history.append(metrics)
            await asyncio.sleep(1)
            
    def gather_metrics(self) -> SystemMetrics:
        """Gather system metrics"""
        return SystemMetrics(
            cpu_usage=psutil.cpu_percent(),
            memory_usage=psutil.virtual_memory().percent,
            disk_usage=psutil.disk_usage('/').percent,
            network_speed=self.get_network_speed(),
            gpu_usage=self.get_gpu_usage(),
            timestamp=datetime.now()
        )
