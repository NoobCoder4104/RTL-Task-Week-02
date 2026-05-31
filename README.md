# Complete GitHub README.md for RTL Analysis Project

Copy and paste this entire README into your GitHub repository's `README.md` file. Fill in the `[ ]` placeholders with your actual information.

---

```markdown
# RTL Analysis Automation Pipeline

## APB & I2C Protocol Analysis with 6-Stage Python Toolchain

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-complete-brightgreen.svg)]()
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey.svg)]()

---

## 📌 Project Overview

This project implements a complete **RTL (Register Transfer Level) analysis automation pipeline** for two industry-standard bus protocols: **APB (Advanced Peripheral Bus)** and **I2C (Inter-Integrated Circuit)**.

The pipeline consists of 6 Python scripts that transform raw Verilog/SystemVerilog RTL code into structured, semantic Intermediate Representation (IR) JSON files, making it ready for downstream verification (DV) and machine learning (ML) applications.

### Why This Project Exists

| Problem | Solution |
|---------|----------|
| RTL code is hard to parse automatically | Tokenization + AST generation extracts structure |
| Raw RTL contains `include, `define, `ifdef | Preprocessing expands all macros and conditionals |
| Engineers need semantic understanding (clock, reset, data signals) | IR adds meaning (port roles, reset polarity) |
| Manual RTL analysis is time-consuming and error-prone | 6 scripts run end-to-end in seconds |

---

## 📂 Repository Structure

```
📦 RTL-Analysis-Pipeline/
│
├── 📁 rtl_files/                    # Original RTL source files
│   ├── 📁 apb_rtl/
│   │   ├── slave1.v                 # APB Slave implementation 1
│   │   └── slave2.v                 # APB Slave implementation 2
│   │
│   └── 📁 i2c_rtl/
│       ├── i2c.v                    # I2C Top Module
│       ├── i2c_master.v             # I2C Master FSM (16 states)
│       └── i2c_slave.v              # I2C Slave logic
│
├── 📁 python_scripts/               # All analysis scripts
│   ├── 01_input_normalizer.py       # Script 1: File scanner
│   ├── 02_sv_preprocessor.py        # Script 2: Macro expander
│   ├── 03_lexer_tokenizer.py        # Script 3: Token generator
│   ├── 04_parser_v0.py              # Script 4: AST builder
│   ├── 05_ir_builder.py             # Script 5: IR generator
│   └── 06_clock_reset_analyzer.py   # Script 6: Clock/Reset analyzer
│
├── 📁 outputs/                      # All generated outputs
│   ├── 📁 apb_outputs/              # APB-specific outputs
│   │   ├── *.csv                    # File manifests
│   │   ├── *.json                   # Token, AST, IR files
│   │   ├── *.md                     # Documentation logs
│   │   └── *.sv                     # Preprocessed RTL
│   │
│   └── 📁 i2c_outputs/              # I2C-specific outputs
│       └── ...
│
├── 📁 docs/                         # Documentation
│   ├── LEARNING_DOCUMENT.md         # 9-section learning document
│   ├── ISSUE_LOG.md                 # Challenges & resolutions
│   └── PRESENTATION_SLIDES.md       # Presentation content
│
├── README.md                        # This file
├── requirements.txt                 # Python dependencies
└── run_all_scripts.py               # One-command execution script
```

---

## 🚀 Quick Start Guide

### Prerequisites

| Requirement | Version | Check Command |
|-------------|---------|---------------|
| Python | 3.8+ | `python --version` |
| pip | Latest | `pip --version` |
| Git | Any | `git --version` |

### Installation (5 Minutes)

```bash
# 1. Clone the repository
git clone https://github.com/[YOUR_USERNAME]/RTL-Analysis-Pipeline.git
cd RTL-Analysis-Pipeline

# 2. Create virtual environment (recommended)
python -m venv venv

# 3. Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Verify installation
python --version
```

### Dependencies (requirements.txt)

```txt
# requirements.txt
# No external dependencies required for core scripts
# Python standard library only: os, re, json, csv, datetime, shutil
```

### Run the Complete Pipeline

```bash
# Option 1: Run all scripts for both protocols (RECOMMENDED)
python run_all_scripts.py

# Option 2: Run scripts individually for APB
cd python_scripts
python 01_input_normalizer.py
python 02_sv_preprocessor.py
python 03_lexer_tokenizer.py
python 04_parser_v0.py
python 05_ir_builder.py
python 06_clock_reset_analyzer.py

# Option 3: Run for I2C only (modify paths in scripts)
# Change RTL_FOLDER and OUTPUT_FOLDER to i2c paths
```

---

## 🔧 The 6-Script Pipeline

### Pipeline Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         RTL ANALYSIS PIPELINE                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  📁 RTL Files          🔧 Script 1          📄 CSV Manifest                 │
│  (slave1.v, i2c.v)  ──▶ input_normalizer ──▶ file_manifest.csv             │
│         │                                                                   │
│         ▼                                                                   │
│  🔧 Script 2            📄 Preprocessed     📄 Dependency Map               │
│  sv_preprocessor ──────▶ sample_preprocessed.sv                            │
│                         ──▶ preprocess_dependency_map.md                   │
│                         ──▶ preprocess_issues_log.md                       │
│         │                                                                   │
│         ▼                                                                   │
│  🔧 Script 3            📄 Token Stream     📄 Token Log                    │
│  lexer_tokenizer ──────▶ sample_token_stream.json                          │
│                         ──▶ lexer_observation_log.md                       │
│         │                                                                   │
│         ▼                                                                   │
│  🔧 Script 4            📄 AST              📄 Parser Log                   │
│  parser_v0 ────────────▶ sample_ast.json                                   │
│                         ──▶ parser_scope_v0.md                             │
│         │                                                                   │
│         ▼                                                                   │
│  🔧 Script 5            📄 IR (Semantic)    📄 Schema                       │
│  ir_builder ───────────▶ sample_base_ir.json                               │
│                         ──▶ ir_schema_v0_1.json                            │
│                         ──▶ ast_to_ir_mapping_table.md                     │
│         │                                                                   │
│         ▼                                                                   │
│  🔧 Script 6            📄 Clock/Reset     📄 Reset Graph                   │
│  clock_reset_analyzer ──▶ clock_reset_report.json                          │
│                         ──▶ clock_reset_rules_v0.md                        │
│                         ──▶ reset_graph_v0.md                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 Script Details

### Script 1: `01_input_normalizer.py`

| Aspect | Detail |
|--------|--------|
| **Purpose** | Scan RTL directory, classify files, create manifest |
| **Input** | Folder path containing `.v` / `.sv` files |
| **Output** | `*_file_manifest.csv` |
| **Key Functions** | `os.listdir()`, file classification logic |

**How it works:**
1. Recursively scans the specified RTL folder
2. Identifies all `.v` and `.sv` files
3. Classifies each file as `top_module`, `submodule`, or `unknown`
4. Generates a CSV manifest with file names, paths, and types

**Sample Output:**
```csv
file_name,file_path,is_top_module
slave1.v,C:/RTL_Project/apb_rtl/slave1.v,top_module
slave2.v,C:/RTL_Project/apb_rtl/slave2.v,top_module
```

---

### Script 2: `02_sv_preprocessor.py`

| Aspect | Detail |
|--------|--------|
| **Purpose** | Resolve `include, `define, `ifdef directives |
| **Input** | Raw RTL files |
| **Output** | `sample_preprocessed_rtl.sv`, `preprocess_dependency_map.md`, `preprocess_issues_log.md` |
| **Key Functions** | Macro expansion, conditional compilation, include resolution |

**What it handles:**

| Directive | Action | Example |
|-----------|--------|---------|
| `` `include "file.v" `` | Inserts entire file content | `include "defines.vh"` → file contents |
| `` `define WIDTH 32 `` | Creates macro | `define DATA_WIDTH 32` |
| `` `WIDTH `` | Expands to macro value | `` `DATA_WIDTH `` → `32` |
| `` `ifdef DEBUG `` | Conditional block | Keeps block if DEBUG defined |
| `` `endif `` | Ends conditional | Closes `ifdef` block |

**Before vs After Preprocessing:**

```verilog
// BEFORE (slave1.v)
`define DATA_WIDTH 32
`ifdef DEBUG_MODE
    initial $display("Debug mode");
`endif
input [`DATA_WIDTH-1:0] PWDATA;

// AFTER (preprocessed)
input [32-1:0] PWDATA;
// DEBUG_MODE block removed (not defined)
```

---

### Script 3: `03_lexer_tokenizer.py`

| Aspect | Detail |
|--------|--------|
| **Purpose** | Convert RTL code into token stream |
| **Input** | Preprocessed RTL file |
| **Output** | `sample_token_stream.json`, `lexer_observation_log.md` |
| **Key Functions** | Regex pattern matching, token classification |

**Token Categories:**

| Token Type | Regex Pattern | Examples |
|------------|---------------|----------|
| KEYWORD | `\b(module\|input\|always\|...)\b` | module, input, always, assign |
| IDENTIFIER | `[a-zA-Z_][a-zA-Z0-9_]*` | PCLK, data_in, slave1 |
| NUMBER | `\d+['bBhH][01a-f]+|\d+` | 32'hFFFF, 1'b0, 8'd255 |
| OPERATOR | `[=!<>]=|[=!<>]|&&|\|\|` | =, <=, ==, &&, \|\| |
| PUNCTUATION | `[;:,\(\)\[\]{}]` | ; , : ( ) [ ] { } |

**Sample Token Output:**
```json
[
  {"type": "KEYWORD", "value": "module", "line": 5},
  {"type": "IDENTIFIER", "value": "slave1", "line": 5},
  {"type": "KEYWORD", "value": "input", "line": 6},
  {"type": "IDENTIFIER", "value": "PCLK", "line": 6},
  {"type": "PUNCTUATION", "value": ",", "line": 6}
]
```

---

### Script 4: `04_parser_v0.py`

| Aspect | Detail |
|--------|--------|
| **Purpose** | Extract structured AST from token stream |
| **Input** | Token stream JSON |
| **Output** | `sample_ast.json`, `parser_scope_v0.md`, `unsupported_sv_patterns.md` |
| **Key Functions** | Module name extraction, port parsing, FSM detection |

**AST Structure Extracted:**

```json
{
  "protocol": "APB",
  "module_name": "slave1",
  "ports": [
    {"name": "PCLK", "direction": "input", "type": "wire"},
    {"name": "PRESETn", "direction": "input", "type": "wire"},
    {"name": "PADDR", "direction": "input", "type": "wire", "width": "7:0"},
    {"name": "PSEL", "direction": "input", "type": "wire"},
    {"name": "PENABLE", "direction": "input", "type": "wire"},
    {"name": "PWRITE", "direction": "input", "type": "wire"},
    {"name": "PWDATA", "direction": "input", "type": "wire", "width": "31:0"},
    {"name": "PRDATA", "direction": "output", "type": "reg", "width": "31:0"}
  ],
  "fsm_states": ["IDLE", "SETUP", "ACCESS"],
  "always_blocks": [
    {"type": "always_ff", "sensitivity": ["posedge", "PCLK", "negedge", "PRESETn"]}
  ]
}
```

---

### Script 5: `05_ir_builder.py`

| Aspect | Detail |
|--------|--------|
| **Purpose** | Convert AST to semantic IR with port role classification |
| **Input** | AST JSON |
| **Output** | `sample_base_ir.json`, `ir_schema_v0_1.json`, `ast_to_ir_mapping_table.md` |
| **Key Functions** | Port role classification, reset polarity detection |

**Port Role Classification Rules:**

| Role | Detection Rule | Example |
|------|----------------|---------|
| **clock** | Name contains `clk` or `clock` | PCLK, clk, sys_clock |
| **reset** | Name contains `rst` or `reset` | PRESETn, rst, reset_n |
| **address** | Name contains `addr` or `address` | PADDR, mem_addr |
| **data** | Width > 1 OR contains `data` | PWDATA, write_data[31:0] |
| **control** | PSEL, PENABLE, PWRITE, we, re | PSEL, we, enable |
| **response** | PRDATA, valid, ready, busy, ack | PRDATA, rx_valid |

**Reset Polarity Detection:**

| Signal Pattern | Polarity |
|----------------|----------|
| Ends with `_n` | `active_low` |
| Contains `_n` | `active_low` |
| No `_n` suffix | `active_high` |

**Sample IR Output:**
```json
{
  "schema_version": "0.1",
  "metadata": {
    "generated_by": "ir_builder.py",
    "protocol": "APB",
    "timestamp": "2024-01-15T10:30:00"
  },
  "module": {"name": "slave1", "type": "top"},
  "ports": [
    {"name": "PCLK", "direction": "input", "width": 1, "role": "clock"},
    {"name": "PRESETn", "direction": "input", "width": 1, "role": "reset", "polarity": "active_low"},
    {"name": "PADDR", "direction": "input", "width": 8, "role": "address"},
    {"name": "PSEL", "direction": "input", "width": 1, "role": "control"}
  ],
  "fsm": {"states": ["IDLE", "SETUP", "ACCESS"], "encoding": "localparam"},
  "reset": {"signal": "PRESETn", "polarity": "active_low", "type": "asynchronous"}
}
```

---

### Script 6: `06_clock_reset_analyzer.py`

| Aspect | Detail |
|--------|--------|
| **Purpose** | Identify clocks, resets, determine sync/async behavior |
| **Input** | IR JSON + Original RTL |
| **Output** | `clock_reset_report.json`, `clock_reset_rules_v0.md`, `reset_graph_v0.md` |
| **Key Functions** | Clock detection, reset polarity detection, async/sync classification |

**Detection Results:**

| Protocol | Clock Signal | Reset Signal | Polarity | Reset Type |
|----------|--------------|--------------|----------|------------|
| **APB** | PCLK | PRESETn | Active LOW | Asynchronous |
| **I2C** | clk | rst | Active HIGH | Asynchronous |

**How Reset Type is Detected:**

```verilog
// ASYNCHRONOUS RESET (in sensitivity list)
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        // Reset logic
    end
end

// SYNCHRONOUS RESET (inside always block)
always @(posedge clk) begin
    if (rst) begin
        // Reset logic
    end
end
```

**Sample Report Output:**
```json
{
  "protocol": "APB",
  "module": "slave1",
  "clocks": [{"name": "PCLK", "type": "primary"}],
  "resets": [
    {
      "name": "PRESETn",
      "polarity": "active_low",
      "type": "asynchronous",
      "registers_affected_count": 5
    }
  ],
  "summary": {
    "total_clocks": 1,
    "total_resets": 1,
    "async_resets": 1,
    "active_low_resets": 1
  }
}
```

---

## 📊 Protocols Analyzed

### APB (Advanced Peripheral Bus)

| Feature | Description |
|---------|-------------|
| **Type** | Parallel bus, non-pipelined |
| **FSM States** | 3 (IDLE → SETUP → ACCESS) |
| **Reset** | Active LOW (PRESETn) |
| **Clock** | PCLK |
| **Key Signals** | PSEL, PENABLE, PWRITE, PADDR, PWDATA, PRDATA |
| **Typical Use** | SoC peripheral configuration (UART, I2C, SPI, GPIO, Timers) |

**APB Transaction Flow:**
```
WRITE: IDLE → SETUP (PSEL=1) → ACCESS (PENABLE=1) → IDLE
READ:  IDLE → SETUP (PSEL=1) → ACCESS (PENABLE=1) → IDLE
```

### I2C (Inter-Integrated Circuit)

| Feature | Description |
|---------|-------------|
| **Type** | 2-wire serial, half-duplex |
| **FSM States** | 16 (IDLE → START → ADDRESS → ACK → DATA → STOP) |
| **Reset** | Active HIGH (rst) |
| **Clock** | clk (system) + SCL (generated) |
| **Key Signals** | SCL, SDA, we, re, address, write_data, read_data |
| **Typical Use** | External sensors, EEPROM, RTC, display controllers |

**I2C Transaction Flow:**
```
WRITE: START → 7-bit Address → R/W=0 → ACK → Data → ACK → STOP
READ:  START → 7-bit Address → R/W=1 → ACK → Data → NACK → STOP
```

---

## 📄 Output Files Reference

### Common Output Files (Both Protocols)

| File | Format | Description |
|------|--------|-------------|
| `*_file_manifest.csv` | CSV | List of all RTL files with classifications |
| `sample_preprocessed_rtl.sv` | Verilog | Flattened RTL with all macros expanded |
| `preprocess_dependency_map.md` | Markdown | Shows file include dependencies |
| `preprocess_issues_log.md` | Markdown | Lists warnings/errors during preprocessing |
| `sample_token_stream.json` | JSON | Complete token stream from lexer |
| `lexer_observation_log.md` | Markdown | Token statistics and observations |
| `sample_ast.json` | JSON | Abstract Syntax Tree output |
| `parser_scope_v0.md` | Markdown | Parser capabilities and limitations |
| `sample_base_ir.json` | JSON | Semantic IR with port roles |
| `ir_schema_v0_1.json` | JSON | Schema definition for IR format |
| `ast_to_ir_mapping_table.md` | Markdown | Maps AST fields to IR fields |
| `clock_reset_report.json` | JSON | Clock and reset analysis results |
| `clock_reset_rules_v0.md` | Markdown | Detection rules used |
| `reset_graph_v0.md` | Markdown | Reset dependency visualization |

### APB-Specific Outputs

```
outputs/apb_outputs/
├── apb_file_manifest.csv
├── sample_preprocessed_rtl.sv
├── preprocess_dependency_map.md
├── preprocess_issues_log.md
├── sample_token_stream.json
├── lexer_observation_log.md
├── sample_ast.json
├── parser_scope_v0.md
├── unsupported_sv_patterns.md
├── sample_base_ir.json
├── ir_schema_v0_1.json
├── ast_to_ir_mapping_table.md
├── apb_slave1_ast.json
├── apb_slave1_ir.json
├── apb_slave1_clock_reset_analysis.json
├── apb_slave2_ast.json
├── apb_slave2_ir.json
├── clock_reset_report.json
├── clock_reset_rules_v0.md
└── reset_graph_v0.md
```

### I2C-Specific Outputs

```
outputs/i2c_outputs/
├── i2c_file_manifest.csv
├── sample_preprocessed_rtl.sv
├── preprocess_dependency_map.md
├── preprocess_issues_log.md
├── sample_token_stream.json
├── lexer_observation_log.md
├── sample_ast.json
├── sample_base_ir.json
├── ir_schema_v0_1.json
├── i2c_i2c_ast.json
├── i2c_i2c_ir.json
├── i2c_i2c_token_stream.json
├── clock_reset_report.json
└── reset_graph_v0.md
```

---

## 🐛 Issue Log Summary

| # | Issue | Root Cause | Resolution | Status |
|---|-------|------------|------------|--------|
| 1 | Nested `ifdef preprocessing failed | Regex doesn't handle nested conditionals | Implemented stack-based conditional processing | ✅ |
| 2 | FSM states not detected by parser | Parser missed localparam definitions | Added pattern matching for FSM keywords | ✅ |
| 3 | I2C reset polarity detected as active_low | Script assumed all resets end with `_n` | Added conditional: `_n` = active_low, else active_high | ✅ |
| 4 | File path errors in Script 6 | Hardcoded paths didn't match user structure | Made all paths configurable at script top | ✅ |
| 5 | I2C FSM not found in top module | FSM defined in i2c_master.v, not i2c.v | Manually documented from submodule | ✅ |
| 6 | Numbers with base prefixes not recognized | Regex only matched decimal numbers | Added patterns for `'b`, `'h`, `'d`, `'o` formats | ✅ |

---

## 📈 Key Learnings

### Protocol Learnings

| Protocol | Key Takeaway |
|----------|--------------|
| **APB** | Simple 3-state FSM, active-low reset, parallel bus, non-pipelined |
| **I2C** | Complex 16-state FSM, 2-wire serial, built-in addressing, multi-master capable |

### Technical Learnings

| Concept | What I Learned |
|---------|----------------|
| **Preprocessing** | `` `include ``, `` `define ``, `` `ifdef `` must be resolved BEFORE lexing because lexers don't understand backtick directives |
| **Lexing** | Token stream is the bridge between raw text and structured analysis; each token has type, value, and line number |
| **Parsing** | AST preserves hierarchical code structure; different from token stream (flat list) |
| **IR Generation** | AST = Syntax (what the code says); IR = Semantics (what the code means) |
| **Reset Detection** | `_n` suffix = active_low; async reset in sensitivity list, sync reset inside always block |
| **Port Classification** | Roles (clock, reset, data, address, control) inferred from signal names and width |

---

## 🚦 Quick Commands Reference

```bash
# Clone and setup
git clone https://github.com/[USERNAME]/RTL-Analysis-Pipeline.git
cd RTL-Analysis-Pipeline
python -m venv venv
venv\Scripts\activate

# Run complete pipeline
python run_all_scripts.py

# Run individual scripts
cd python_scripts
python 01_input_normalizer.py
python 02_sv_preprocessor.py
python 03_lexer_tokenizer.py
python 04_parser_v0.py
python 05_ir_builder.py
python 06_clock_reset_analyzer.py

# Verify outputs
dir ../outputs/apb_outputs/
dir ../outputs/i2c_outputs/
```

---

## 📚 References

### RTL Sources
- [APB Protocol RTL](https://github.com/shubhi704/APB-Protocol)
- [I2C Protocol RTL](https://github.com/Ammar-Bin-Amir/I2C)

### Documentation
- [AMBA APB Specification](https://developer.arm.com/documentation/ihi0024/latest/)
- [I2C Bus Specification](https://www.nxp.com/docs/en/user-guide/UM10204.pdf)

### Project Resources
- [Week 2 RTL Plan](./docs/RTL_Task_2_Plan.pdf)
- [Learning Document](./docs/LEARNING_DOCUMENT.md)
- [Presentation Slides](./docs/PRESENTATION_SLIDES.md)

---

## 👤 Author

| Field | Information |
|-------|-------------|
| **Name** | [Asfaq Tannbir] |
| **Group** | Group C |
| **Protocols** | APB + I2C |
| **Duration** | Week 2 (6 days + Day 7 submission) |
| **Contact** | [tanbirchy111@gmail.com] |

---

## ✅ Project Status

| Component | Status |
|-----------|--------|
| Script 1: input_normalizer.py | ✅ Complete |
| Script 2: sv_preprocessor.py | ✅ Complete |
| Script 3: lexer_tokenizer.py | ✅ Complete |
| Script 4: parser_v0.py | ✅ Complete |
| Script 5: ir_builder.py | ✅ Complete |
| Script 6: clock_reset_analyzer.py | ✅ Complete |
| APB Analysis | ✅ Complete |
| I2C Analysis | ✅ Complete |
| Learning Document (9 sections) | ✅ Complete |
| Presentation | ✅ Complete |

---

## 📜 License

This project is for educational purposes as part of the Asmicore RTL Mentorship Programme.

---

## 🙏 Acknowledgments

- Asmicore Semiconductor for the mentorship opportunity
- RTL engineering team for guidance and feedback
- Open-source RTL contributors for APB and I2C implementations

---

**⭐ If you find this project useful, please star the repository!**
```

---
