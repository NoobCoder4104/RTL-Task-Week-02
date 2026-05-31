
# RTL Analysis Pipeline for APB and I2C Communication Protocols

## 6 Python Scripts for APB & I2C Protocol Analysis

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Status](https://img.shields.io/badge/Status-Completed-brightgreen.svg)]()
[![APB](https://img.shields.io/badge/Protocol-APB-orange.svg)]()
[![I2C](https://img.shields.io/badge/Protocol-I2C-yellow.svg)]()

---

## 📌 What This Project Does

Transforms raw Verilog RTL code into structured, semantic JSON output using a 6-stage Python pipeline.

**Input:** RTL files (`slave1.v`, `slave2.v`, `i2c.v`, etc.)  
**Output:** Token streams, AST, IR, Clock/Reset analysis reports

---

## 🔧 The 6 Scripts

| # | Script | Input → Output |
|---|--------|----------------|
| 1 | `input_normalizer.py` | RTL folder → CSV manifest |
| 2 | `sv_preprocessor.py` | Raw RTL → Preprocessed RTL (macros expanded) |
| 3 | `lexer_tokenizer.py` | RTL → Token stream JSON |
| 4 | `parser_v0.py` | Token stream → AST JSON |
| 5 | `ir_builder.py` | AST → Semantic IR JSON (port roles) |
| 6 | `clock_reset_analyzer.py` | IR + RTL → Clock/Reset report |

---

## 📂 What You Need

```
📁 rtl_files/
   ├── slave1.v, slave2.v    (APB)
   └── i2c.v, i2c_master.v, i2c_slave.v   (I2C)

📁 python_scripts/
   ├── 01_input_normalizer.py
   ├── 02_sv_preprocessor.py
   ├── 03_lexer_tokenizer.py
   ├── 04_parser_v0.py
   ├── 05_ir_builder.py
   └── 06_clock_reset_analyzer.py

📁 outputs/
   ├── apb_outputs/     (all APB results)
   └── i2c_outputs/     (all I2C results)
```

---

## 🚀 Quick Start

```bash
# 1. Clone
git clone https://github.com/[YOUR_USERNAME]/RTL-Analysis-Pipeline.git
cd RTL-Analysis-Pipeline

# 2. Run any script
cd python_scripts
python 01_input_normalizer.py
python 02_sv_preprocessor.py
python 03_lexer_tokenizer.py
python 04_parser_v0.py
python 05_ir_builder.py
python 06_clock_reset_analyzer.py
```

**No external dependencies required** (uses Python standard library only)

---

## 📊 Scripts in Detail

### Script 1: `input_normalizer.py`
Scans folder, identifies top module vs submodules → `*_file_manifest.csv`

### Script 2: `sv_preprocessor.py`
Resolves `` `include ``, `` `define ``, `` `ifdef/`endif `` → `sample_preprocessed_rtl.sv`

### Script 3: `lexer_tokenizer.py`
Breaks code into tokens (KEYWORD, IDENTIFIER, NUMBER, OPERATOR) → `sample_token_stream.json`

### Script 4: `parser_v0.py`
Extracts module name, ports, FSM states from tokens → `sample_ast.json`

### Script 5: `ir_builder.py`
Adds semantic meaning (port roles: clock, reset, data, control) → `sample_base_ir.json`

**Port Role Rules:**
- `*clk*` → clock
- `*rst*` + `_n` → reset (active_low)
- `*rst*` (no `_n`) → reset (active_high)
- `*addr*` → address
- `*data*` or width>1 → data

### Script 6: `clock_reset_analyzer.py`
Detects reset polarity and type (sync/async) → `clock_reset_report.json`

**Results:**
| Protocol | Clock | Reset | Polarity | Type |
|----------|-------|-------|----------|------|
| APB | PCLK | PRESETn | Active LOW | Async |
| I2C | clk | rst | Active HIGH | Async |

---

## 📄 Key Output Files

| File | What It Contains |
|------|------------------|
| `*_file_manifest.csv` | List of all RTL files |
| `sample_preprocessed_rtl.sv` | Flattened RTL (no `include/`define) |
| `sample_token_stream.json` | All tokens with line numbers |
| `sample_ast.json` | Module structure (ports, FSM) |
| `sample_base_ir.json` | Semantic IR with port roles |
| `clock_reset_report.json` | Clock/reset analysis |

---

## 🐛 Issues Fixed

| Issue | Solution |
|-------|----------|
| Nested `ifdef failed | Stack-based processing |
| FSM states not detected | Pattern matching for localparam |
| I2C reset polarity wrong | `_n` suffix = active_low, else active_high |

---

## 📈 Protocols Analyzed

| Feature | APB | I2C |
|---------|-----|-----|
| Type | Parallel bus | 2-wire serial |
| FSM States | 3 (IDLE/SETUP/ACCESS) | 16 |
| Reset | Active LOW | Active HIGH |
| Key Signals | PSEL, PENABLE, PWRITE | SCL, SDA, we, re |

---

## 👤 Asfaq

**Group C** | APB + I2C | Week 2 RTL Task

---

## ⭐ Quick Commands

```bash
# Run everything
cd python_scripts && python 01_input_normalizer.py && python 02_sv_preprocessor.py && python 03_lexer_tokenizer.py && python 04_parser_v0.py && python 05_ir_builder.py && python 06_clock_reset_analyzer.py

# Check outputs
ls ../outputs/apb_outputs/
ls ../outputs/i2c_outputs/
```

---

