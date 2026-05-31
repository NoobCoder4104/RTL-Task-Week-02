# Parser Scope v0 - APB slave2

## Generated: 2026-05-24 16:15:41

## Parser Summary

| Item | Value |
|------|-------|
| Module Name | slave2 |
| Number of Ports | 3 |
| Number of Signals | 0 |
| Number of Parameters | 0 |
| FSM States Found | 0 |
| Always Blocks | 0 |
| Assign Statements | 0 |

## Ports List

| Name | Direction | Type | Width |
|------|-----------|------|-------|
| PCLK | input | wire | 1 |
| PSEL | input | wire | 1 |
| PREADY | output | reg | 1 |

## Parameters/Localparams

| Name | Value | Type |
|------|-------|------|

## FSM States Found

No FSM states detected

## Always Blocks

| Type | Sensitivity | Line |
|------|-------------|------|

## Observations

- Module parsed successfully
- 3 ports extracted
- 0 potential FSM states identified
- 0 always blocks found

## Limitations (v0)

- Width parsing simplified
- Multi-dimensional arrays not supported
- Complex expressions not fully parsed
- Package imports not handled

## Next Steps

- Pass AST to ir_builder.py
- Classify ports by role (clock, reset, data, control)
- Build semantic IR
