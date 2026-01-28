import os
import subprocess

# =========================
# Configuration
# =========================

# Folder where this script lives (and where the implX executables are)
UNIT_FOLDER = os.path.dirname(os.path.abspath(__file__))

# Units (executables in the same folder)
UNITS = [f"impl{i}" for i in range(7)]

# Register addresses
CSR_ADDR     = 0x0
COEF_ADDR    = 0x4
OUTCAP_ADDR  = 0x8

# Input buffer
MAX_BUF = 255

# =========================
# Common helper functions
# =========================
def run(unit, command):
    """Run a command for a given unit executable"""
    unit_path = os.path.join(UNIT_FOLDER, unit)
    print(f"[{unit}] {command}")
    subprocess.run([unit_path] + command.split())

def read_reg(unit, addr):
    """Read a register at a given address"""
    run(unit, f"cfg --address {hex(addr)}")

def get_csr(unit):
    """Read CSR register"""
    read_reg(unit, CSR_ADDR)

# =========================
# Control & register validation
# =========================
def basic_validation(unit):
    print("\n--- Day 2: Basic control & register validation ---")

    # Step 1: Reset
    run(unit, "com --action reset")

    # Step 2: Disable
    run(unit, "com --action disable")

    # Step 3: Read CSR while disabled
    print("Attempt CSR read while disabled:")
    get_csr(unit)

    # Step 4: Enable
    run(unit, "com --action enable")

    # Step 5: Read registers while enabled
    print("Reading registers while enabled:")
    read_reg(unit, CSR_ADDR)
    read_reg(unit, COEF_ADDR)
    read_reg(unit, OUTCAP_ADDR)

# =========================
# Filter & buffer validation
# =========================
def halt_and_enable_coeffs(unit):
    """Set CSR.HALT = 1 and enable filter & coefficients"""
    print("\n--- Halting unit and enabling coefficients ---")
    run(unit, "cfg --address 0x0 --data 0x3F")

def clear_input_buffer(unit):
    """Clear input buffer"""
    print("\n--- Clearing input buffer ---")
    run(unit, "cfg --address 0x0 --data 0x20000")

def set_bypass(unit):
    """Enable bypass mode"""
    print("\n--- Setting bypass mode ---")
    run(unit, "cfg --address 0x0 --data 0x10")

def filter_validation(unit):
    print("\n--- Day 3: Filter & buffer behavior ---")

    # Step 1: Halt and enable coefficients
    halt_and_enable_coeffs(unit)

    # Step 2: Fill input buffer (force overflow)
    print(f"\n--- Filling input buffer (max {MAX_BUF}) ---")
    for i in range(260):
        if i == MAX_BUF:
            print(f"*** Buffer should overflow at sample {i} ***")
        run(unit, f"sig --data {hex(i)}")

    # Step 3: Check CSR for buffer count / overflow
    print("\n--- Checking CSR after buffer fill ---")
    get_csr(unit)

    # Step 4: Clear input buffer
    clear_input_buffer(unit)
    get_csr(unit)

    # Step 5: Enable bypass
    set_bypass(unit)

    # Step 6: Drive samples in bypass mode
    print("\n--- Driving samples in bypass mode ---")
    for i in range(10):
        run(unit, f"sig --data {hex(i)}")

    get_csr(unit)

# =========================
# Main test loop
# =========================
for unit in UNITS:
    print(f"\n========== Validating {unit} ==========")

    basic_validation(unit)
    filter_validation(unit)

    print("\n" + "=" * 60 + "\n")
