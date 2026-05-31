# AST to IR Mapping Table - APB slave2

## Generated: 2026-05-24 16:33:00

## Overview

This document maps AST (Abstract Syntax Tree) fields to IR (Intermediate Representation) fields.

## Port Mapping

| AST Field | IR Field | Transformation |
|-----------|----------|----------------|
| `port.name` | `port.name` | Direct copy |
| `port.direction` | `port.direction` | Direct copy |
| `port.width` (string "31:0") | `port.width` (integer 32) | Converted to bit width |
| `port.type` (wire/reg) | (not in IR) | Dropped (not semantic) |
| (inferred from name) | `port.role` | **Classification rule-based** |
| (inferred from name) | `port.polarity` | **Detected from `_n` suffix** |

## Example Port Mapping

| AST | IR |
|-----|-----|
| `{"name": "PCLK", "direction": "input"}` | `{"name": "PCLK", "role": "clock"}` |
| `{"name": "PRESETn", "direction": "input"}` | `{"name": "PRESETn", "role": "reset", "polarity": "active_low"}` |
| `{"name": "PADDR", "width": "7:0"}` | `{"name": "PADDR", "role": "address", "width": 8}` |

## Classification Rules Used

| Role | Detection Rule |
|------|----------------|
| clock | Name contains `clk` or `clock` |
| reset | Name contains `rst` or `reset` |
| address | Name contains `addr` or `address` |
| data | Width > 1 OR name contains `data` |
| control | Name in `[psel, penable, pwrite, we, re]` |
| response | Name in `[prdata, pready, valid, busy]` |

## Reset Detection

| AST Always Block | IR Reset Type |
|------------------|---------------|
| `@(posedge clk or negedge rst_n)` | `asynchronous` |
| `@(posedge clk)` | `synchronous` |

## FSM State Mapping

| AST | IR |
|-----|-----|
| `localparam IDLE = 4'h0` | `fsm.states = ["IDLE", ...]` |
| `localparam SETUP = 4'h1` | |
| `localparam ACCESS = 4'h2` | |

## Why This Mapping Matters

1. **AST is syntax** - tells you WHAT the code says
2. **IR is semantics** - tells you WHAT the code MEANS
3. **Downstream tools** (DV, ML) use IR, not AST
4. **Schema-bound** ensures consistency across designs

## Validation

- IR follows schema version 0.1
- All ports classified
- Reset correctly identified
- FSM states extracted
