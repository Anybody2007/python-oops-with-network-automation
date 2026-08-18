# Network & Network Security Logging Mastery Labs
## FAANG-Scale Observability & Telemetry for Network Engineers

This workbook contains 5 progressive, hands-on coding exercises designed to take your Python network automation, logging, and observability skills to Tier-1 infrastructure scale.

---

### Progress Tracker
- [ ] **Lab 1:** Multi-Vendor BGP Syslog Normalizer (Cisco IOS & Arista EOS)
- [ ] **Lab 2:** Network Credential & Secret Scrubber (DLP Filter)
- [ ] **Lab 3:** Contextual Change Tracer (`contextvars` Context Manager)
- [ ] **Lab 4:** The Canonical Network Transaction Collector (Wide Event)
- [ ] **Lab 5:** High-Speed Non-Blocking ACL / Firewall Drop Ingestion

---

## 🧪 Lab 1: Multi-Vendor BGP Syslog Normalizer

### Scenario
Your monitoring engine receives raw syslog streams from Cisco, Arista, and Juniper edge routers. Your job is to parse and normalize them into a uniform schema so the on-call team can write one unified alert rule.

### Requirements
Implement `MultiVendorSyslogNormalizer.normalize()`:
1. **Cisco IOS format:** `"%BGP-5-ADJCHANGE: neighbor <IP> <Down|Up> ..."`
   - Set `vendor="CISCO_IOS"`, extract `peer_ip`, and set `state="UP"` or `"DOWN"`.
2. **Arista EOS format:** `"%BGP-5-STATE_CHANGE: Peer <IP> state changed from <OLD> to <NEW>"`
   - Set `vendor="ARISTA_EOS"`, extract `peer_ip`, and set `state=<NEW>` in uppercase (e.g., `"ESTABLISHED"`, `"IDLE"`).
3. **Severity calculation:**
   - If `state` is `"DOWN"` or `"IDLE"`, set `severity="CRITICAL"`.
   - Otherwise, set `severity="INFO"`.
4. Output must be a dictionary with keys: `vendor`, `device`, `peer_ip`, `state`, `severity`.

### Starter Code & Test Suite (`lab1_normalizer.py`)

```python
import re
import json

class MultiVendorSyslogNormalizer:
    def normalize(self, raw_syslog: str, device_name: str) -> dict:
        """
        Parses raw syslog from Cisco or Arista and returns a normalized dictionary.
        """
        # TODO: Write your regex and extraction logic here!
        # Tip: Use re.search() to extract IP addresses and state keywords.
        pass


# ==========================================
# 🧪 TEST SUITE (DO NOT EDIT - RUN TO VERIFY)
# ==========================================
if __name__ == "__main__":
    normalizer = MultiVendorSyslogNormalizer()

    # Test 1: Cisco BGP Down
    cisco_log = "%BGP-5-ADJCHANGE: neighbor 192.168.10.1 Down Interface flap detected"
    res1 = normalizer.normalize(cisco_log, "core-rtr-01")
    assert res1 is not None, "Test 1 Failed: Returned None"
    assert res1["vendor"] == "CISCO_IOS", f"Test 1 Failed: Vendor was {res1.get('vendor')}"
    assert res1["peer_ip"] == "192.168.10.1", f"Test 1 Failed: IP was {res1.get('peer_ip')}"
    assert res1["state"] == "DOWN", f"Test 1 Failed: State was {res1.get('state')}"
    assert res1["severity"] == "CRITICAL", f"Test 1 Failed: Severity was {res1.get('severity')}"
    print("✅ Test 1 (Cisco BGP Down) Passed!")

    # Test 2: Arista BGP Up
    arista_log = "%BGP-5-STATE_CHANGE: Peer 10.0.50.2 state changed from OpenConfirm to Established"
    res2 = normalizer.normalize(arista_log, "leaf-sw-04")
    assert res2["vendor"] == "ARISTA_EOS", f"Test 2 Failed: Vendor was {res2.get('vendor')}"
    assert res2["peer_ip"] == "10.0.50.2", f"Test 2 Failed: IP was {res2.get('peer_ip')}"
    assert res2["state"] == "ESTABLISHED", f"Test 2 Failed: State was {res2.get('state')}"
    assert res2["severity"] == "INFO", f"Test 2 Failed: Severity was {res2.get('severity')}"
    print("✅ Test 2 (Arista BGP Established) Passed!")

    print("\n🎉 ALL TESTS PASSED FOR LAB 1!")
```

---

## 🧪 Lab 2: Network Credential & Secret Scrubber (DLP)

### Scenario
During network config audits and automated pushes, automation scripts print CLI outputs. You must create a custom Python `logging.Filter` that intercepts log records and redacts credentials before they are printed or stored.

### Requirements
Implement `NetworkSecretScrubber.filter()` using regex replacements:
1. **SNMP Community:** `snmp-server community <SECRET> <ro|rw>` $\rightarrow$ replace `<SECRET>` with `[REDACTED_SNMP]`.
2. **BGP MD5 Password:** `neighbor <IP> password <SECRET>` $\rightarrow$ replace `<SECRET>` with `[REDACTED_BGP_KEY]`.
3. **Cisco Secret/Password:** `enable secret <SECRET>` or `enable password <SECRET>` $\rightarrow$ replace `<SECRET>` with `[REDACTED_SECRET]`.

### Starter Code & Test Suite (`lab2_scrubber.py`)

```python
import logging
import re
import io

class NetworkSecretScrubber(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        """
        Intercepts record.msg and redacts secrets before logging.
        """
        if isinstance(record.msg, str):
            # TODO: Implement regex scrubbing for SNMP, BGP password, and Enable secret
            # Example: record.msg = re.sub(..., record.msg)
            pass
            
        return True  # Must return True so the log continues through the pipeline


# ==========================================
# 🧪 TEST SUITE (DO NOT EDIT - RUN TO VERIFY)
# ==========================================
if __name__ == "__main__":
    log_capture = io.StringIO()
    handler = logging.StreamHandler(log_capture)
    handler.setFormatter(logging.Formatter("%(message)s"))
    handler.addFilter(NetworkSecretScrubber())

    logger = logging.getLogger("test_net_scrubber")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    logger.info("Executing: snmp-server community MyCompanyRO2026 ro 10")
    logger.info("Executing: neighbor 10.254.1.1 password SuperSecretBgpMD5Key!")
    logger.info("Executing: enable secret 5 $1$mERr$hx5rVt7rPNoS4wqbXKX7m0")

    output = log_capture.getvalue()
    print("Captured Output:\n", output)

    assert "MyCompanyRO2026" not in output, "❌ Test Failed: SNMP secret was leaked!"
    assert "[REDACTED_SNMP]" in output, "❌ Test Failed: Missing [REDACTED_SNMP] tag"

    assert "SuperSecretBgpMD5Key!" not in output, "❌ Test Failed: BGP MD5 key was leaked!"
    assert "[REDACTED_BGP_KEY]" in output, "❌ Test Failed: Missing [REDACTED_BGP_KEY] tag"

    assert "$1$mERr$hx5rVt7rPNoS4wqbXKX7m0" not in output, "❌ Test Failed: Enable hash was leaked!"
    assert "[REDACTED_SECRET]" in output, "❌ Test Failed: Missing [REDACTED_SECRET] tag"

    print("🎉 ALL TESTS PASSED FOR LAB 2!")
```

---

## 🧪 Lab 3: Contextual Change Tracer (`change_id` & `device_hostname`)

### Scenario
When executing automation across 20 routers concurrently, logs get mixed up in the console. You must build a context manager using Python's `contextvars` so that any function called within a network change block automatically logs with the correct `change_id` and `target_device`.

### Requirements
1. Use `contextvars.ContextVar` to store `current_change_id` and `current_device`.
2. Implement `NetworkChangeContext` as a Python context manager (`__enter__` and `__exit__`).
3. Implement `ContextualJSONFormatter` to output JSON lines with keys: `"change_id"`, `"device"`, `"level"`, `"message"`.

### Starter Code & Test Suite (`lab3_context_tracer.py`)

```python
import logging
import contextvars
import json
import io

# TODO: Define your ContextVar variables here
# change_var = contextvars.ContextVar(...)
# device_var = contextvars.ContextVar(...)

class NetworkChangeContext:
    def __init__(self, change_id: str, device_name: str):
        self.change_id = change_id
        self.device_name = device_name
        self.tokens = []

    def __enter__(self):
        # TODO: Set the context variables and save tokens to restore on exit
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO: Reset the context variables using the saved tokens
        pass


class ContextualJSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        # TODO: Build a dict with change_id, device, level, and message, returning json.dumps()
        pass


# ==========================================
# 🧪 TEST SUITE (DO NOT EDIT - RUN TO VERIFY)
# ==========================================
if __name__ == "__main__":
    log_capture = io.StringIO()
    handler = logging.StreamHandler(log_capture)
    handler.setFormatter(ContextualJSONFormatter())

    logger = logging.getLogger("test_context_logger")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    def push_interface_config(vlan_id: int):
        # Notice this function does NOT accept change_id or device as arguments!
        logger.info(f"Setting access vlan to {vlan_id}")

    # Execute change 1
    with NetworkChangeContext(change_id="CHG-1001", device_name="spine01.region1"):
        push_interface_config(vlan_id=200)

    # Execute change 2
    with NetworkChangeContext(change_id="CHG-1002", device_name="border02.region2"):
        push_interface_config(vlan_id=300)

    raw_lines = [line.strip() for line in log_capture.getvalue().strip().split("\n")]
    assert len(raw_lines) == 2, f"Expected 2 lines, got {len(raw_lines)}. Output: {log_capture.getvalue()}"
    
    entry1 = json.loads(raw_lines[0])
    assert entry1["change_id"] == "CHG-1001", f"Test Failed: Expected CHG-1001, got {entry1.get('change_id')}"
    assert entry1["device"] == "spine01.region1", f"Test Failed: Expected spine01.region1, got {entry1.get('device')}"
    assert "Setting access vlan to 200" in entry1["message"]

    entry2 = json.loads(raw_lines[1])
    assert entry2["change_id"] == "CHG-1002", f"Test Failed: Expected CHG-1002, got {entry2.get('change_id')}"
    assert entry2["device"] == "border02.region2", f"Test Failed: Expected border02.region2, got {entry2.get('device')}"
    assert "Setting access vlan to 300" in entry2["message"]

    print("🎉 ALL TESTS PASSED FOR LAB 3!")
```

---

## 🧪 Lab 4: Canonical Network Change Transaction (Wide Event)

### Scenario
Instead of spewing 50 lines of logs during an automated ACL/BGP deployment, build a recorder that tracks pre-checks, post-checks, diff lines, and execution time, outputting a **single structured summary event** upon completion.

### Requirements
Implement `NetworkChangeRecorder`:
1. `record_pre_check(name: str, passed: bool)`: Adds to `pre_checks` dictionary (`"PASS"` or `"FAIL"`).
2. `record_post_check(name: str, passed: bool)`: Adds to `post_checks` dictionary (`"PASS"` or `"FAIL"`).
3. `complete(status: str, diff_lines: int, rollback: bool = False) -> dict`:
   - Calculates `execution_time_sec` (float rounded to 2 decimals).
   - Returns the complete dictionary matching the schema tested below.

### Starter Code & Test Suite (`lab4_canonical_event.py`)

```python
import time
import json
from datetime import datetime, timezone

class NetworkChangeRecorder:
    def __init__(self, change_id: str, device: str, target_os: str):
        self.change_id = change_id
        self.device = device
        self.target_os = target_os
        self.start_time = time.time()
        # TODO: Initialize internal state data structures

    def record_pre_check(self, check_name: str, passed: bool):
        # TODO: Record pre-check status
        pass

    def record_post_check(self, check_name: str, passed: bool):
        # TODO: Record post-check status
        pass

    def complete(self, status: str, diff_lines: int, rollback: bool = False) -> dict:
        # TODO: Calculate execution time and return final wide event dictionary
        pass


# ==========================================
# 🧪 TEST SUITE (DO NOT EDIT - RUN TO VERIFY)
# ==========================================
if __name__ == "__main__":
    tx = NetworkChangeRecorder(
        change_id="CHG-7740",
        device="edge-rtr-01",
        target_os="cisco_iosxr"
    )
    tx.record_pre_check("bgp_established", passed=True)
    tx.record_pre_check("optics_rx_power_normal", passed=False)
    
    time.sleep(0.05)  # simulate work
    
    tx.record_post_check("ping_gateway", passed=True)
    event = tx.complete(status="SUCCESS", diff_lines=8, rollback=False)

    assert event["change_id"] == "CHG-7740"
    assert event["device"] == "edge-rtr-01"
    assert event["target_os"] == "cisco_iosxr"
    assert event["pre_checks"]["bgp_established"] == "PASS"
    assert event["pre_checks"]["optics_rx_power_normal"] == "FAIL"
    assert event["post_checks"]["ping_gateway"] == "PASS"
    assert event["diff_lines"] == 8
    assert event["rollback"] is False
    assert event["execution_time_sec"] >= 0.05

    print("Canonical Wide Event Output:\n", json.dumps(event, indent=2))
    print("\n🎉 ALL TESTS PASSED FOR LAB 4!")
```

---

## 🧪 Lab 5: High-Speed Async ACL Drop Ingestion

### Scenario
During a volumetric network attack, a perimeter firewall can generate 10,000+ ACL deny events per second. You must implement a non-blocking queue collector with a background thread that batches and flushes events to avoid stalling the application.

### Requirements
Implement `FastSecurityDropCollector`:
1. `log_drop(src_ip, dst_ip, dst_port, protocol, rule_name)`:
   - Uses `queue.Queue.put_nowait()` so calling threads never block.
   - If the queue is full, catches `queue.Full`, increments `dropped_count`, and continues.
2. Background thread drains events from the queue into batches of size `batch_size` (or on timeout) and invokes `_flush_callback(batch)`.
3. `stop()` cleanly flushes remaining events and shuts down the thread.

### Starter Code & Test Suite (`lab5_async_drop_collector.py`)

```python
import queue
import threading
import time

class FastSecurityDropCollector:
    def __init__(self, batch_size: int = 5, max_queue_size: int = 100):
        self.batch_size = batch_size
        self.queue = queue.Queue(maxsize=max_queue_size)
        self.dropped_count = 0
        self.flushed_batches = []
        self.running = True
        
        # TODO: Start background worker thread
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()

    def log_drop(self, src_ip: str, dst_ip: str, dst_port: int, protocol: str, rule_name: str):
        # TODO: Implement non-blocking queue put and handle queue.Full
        pass

    def _worker(self):
        # TODO: Loop while self.running, drain queue into batches of self.batch_size,
        # and call self.flushed_batches.append(batch)
        pass

    def stop(self):
        # TODO: Signal worker to finish and join thread
        self.running = False
        self.worker_thread.join()


# ==========================================
# 🧪 TEST SUITE (DO NOT EDIT - RUN TO VERIFY)
# ==========================================
if __name__ == "__main__":
    collector = FastSecurityDropCollector(batch_size=3, max_queue_size=10)

    # Log 5 drops rapidly
    for i in range(5):
        collector.log_drop(
            src_ip=f"198.51.100.{i}",
            dst_ip="10.0.0.1",
            dst_port=443,
            protocol="TCP",
            rule_name="DEFAULT-DENY-ACL"
        )
    
    time.sleep(0.2)
    collector.stop()

    total_logged = sum(len(b) for b in collector.flushed_batches)
    assert total_logged == 5, f"Expected 5 logged events, got {total_logged}"
    print(f"✅ Successfully collected and batch-flushed {total_logged} events!")
    print("\n🎉 ALL TESTS PASSED FOR LAB 5!")
```
