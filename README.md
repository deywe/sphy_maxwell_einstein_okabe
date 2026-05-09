# SPHY Unified Field - Real-Time SHA256 Validator

**Dataset Access:** [Download sphy_dataset.parquet](https://drive.google.com/file/d/1Csh_GFyvCWbvkCJu-qeqYkCgcLauzqqy/view?usp=drive_link)

## Overview

The **SPHY Real-Time Validator** is a high-performance visualization tool designed to audit and verify the geometric states of the **Sovereign Phase (SΦ)** model. Unlike traditional physics simulators that rely on numerical approximations, this tool operates on an **Immutability-First** principle. It renders a pre-computed dataset where every single frame of the unified field is cryptographically signed using the SHA-256 algorithm.

## Key Features

* **Cryptographic Auditing:** For every frame loaded, the system re-calculates the SHA-256 hash of the raw geometric data (vertices, time, and flexibility parameters) and compares it against the recorded signature in the Parquet dataset.
* **Zero-Drift Visualization:** Ensures that the rendered 3D manifold is exactly what was calculated during the simulation phase, preventing any "hallucinations" or rendering errors.
* **High-Speed I/O:** Utilizes the Apache Parquet format for optimized data retrieval, allowing the Ursina Engine to maintain high frame rates even during real-time validation.
* **Interactive Manifold Exploration:** Full mouse-driven interactivity (Zoom, Rotate, Pan) enabled via the `EditorCamera`, allowing researchers to inspect the coupling between the $g$ vector and the electromagnetic phase.

## Validation Logic

The core of the S(Φ):OK status is the **Immutability Check**:

1. The frame is pulled from the `.parquet` file.
2. The JSON object is reconstructed with `sort_keys=True` to ensure deterministic serialization.
3. A SHA-256 hash is generated.
4. If `Calculated_Hash == Stored_Hash`, the UI displays **S(Φ):OK**, confirming that the geometry has not been tampered with or corrupted.

## Requirements

To run this validator on a sovereign workstation (optimized for Pop!_OS / Linux with NVIDIA), you will need:

* **Python 3.10+**
* **Ursina Engine:** 3D Visualization and real-time rendering.
* **Pandas & PyArrow:** High-speed Parquet data handling.
* **NumPy:** Linear algebra and coordinate mapping.
* **Hardware:** NVIDIA GPU (Recommended) with `__NV_PRIME_RENDER_OFFLOAD` for maximum performance.

### Installation

```bash
pip install ursina pandas pyarrow numpy

```

## How to Run

1. Ensure your `sphy_dataset.parquet` is in the same directory as the script.
2. Execute the script:

```bash
python3 sphy_validator.py

```

---

**Signed by,**

**Deywe Okabe**

*Harpia Quantum Deeptech*

*Belém, Amazon Region - 2026*

> "The code is the law; the hash is the truth."
