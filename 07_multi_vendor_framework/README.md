# 07 Multi-Vendor Framework

This directory combines everything learned so far (Classes, Inheritance, Polymorphism, Abstract Base Classes, and Decorators) into a practical, real-world **Multi-Vendor Firewall Automation Framework**.

Instead of writing vendor-specific scripts for FortiGate, Palo Alto, or Check Point, this framework establishes a unified interface (`Firewall` ABC). Higher-level code can interact with any supported firewall vendor seamlessly through standardized method calls.

---

## 🏗️ Architecture & Component Overview

```
07_multi_vendor_framework/
├── FRAMEWORK_EVOLUTION_ROADMAP.md  # FAANG-Grade Architecture Blueprint & Task Progression Tracker
├── firewall.py                 # Abstract Base Class (Firewall) & Plugin Registration Decorator
├── fortigate.py                # FortiGate REST API Implementation
├── paloalto.py                 # Palo Alto REST API Implementation
├── logging_basic_config.py     # Centralized logging configuration
├── main.py                     # Main execution script / framework orchestrator
└── inventory.csv               # Multi-vendor lab device inventory
```

---

## 🔑 Key OOP & Architecture Concepts Implemented

### 1. Abstract Base Class (`Firewall` in `firewall.py`)
- Defines the common contract for all firewall vendors using Python's `abc.ABC` and `@abstractmethod`.
- Enforces mandatory vendor-specific implementations for:
  - `get_header()`
  - `get_addresses()`
  - `create_addresses()`
  - `get_address_group()`
- Handles shared HTTP session management (`requests.Session()`) in `create_session()` and uniform API requests via `send_request()`.

### 2. Dynamic Vendor Registration (`@register_firewall`)
- Uses a factory/registry pattern implemented via a custom Python decorator in `firewall.py`.
- Dynamically registers vendor classes into the global `FIREWALL_LIST` registry when classes (like `Fortigate`) are decorated with `@register_firewall("FortiGate")`.

### 3. Concrete Vendor Classes
- **`Fortigate` (`fortigate.py`)**: Inherits from `Firewall` and implements FortiOS REST API endpoints with Bearer token authentication (`Authorization: Bearer <key>`) for querying and creating address objects and address groups.
- **`PaloAlto` (`paloalto.py`)**: Inherits from `Firewall` and implements PAN-OS REST API calls using `X-PAN-KEY` authentication headers along with extended parameters such as `panorama_managed`.

### 4. Logging & Orchestration
- **`logging_basic_config.py`**: Provides centralized logging configuration outputting to `multivendor_fw.log`.
- **`main.py`**: Instantiates firewall vendor objects, establishes API sessions, and invokes polymorphic methods uniformly.

---

## 🚀 How to Run

1. Make sure Python 3 and `requests` are installed:
   ```bash
   pip install requests
   ```

2. Run the framework orchestrator:
   ```bash
   cd 07_multi_vendor_framework
   python main.py
   ```

3. Check generated log files:
   ```bash
   cat multivendor_fw.log
   ```

---

## 💡 Key Learnings & Next Steps
- Combining Abstract Base Classes with dynamic decorators makes adding new vendors (e.g., Check Point, Cisco ASA) straightforward without modifying core orchestrator code.
- Next step: Hooking up inventory loader (`inventory.csv`) with `FIREWALL_LIST` factory for automatic vendor instantiation and dynamic execution.
