# Clock/Reset Detection Rules v0

**Protocol:** APB
**Module:** slave2
**Generated:** 2026-05-23 01:08:37

## Clocks Found

- `PCLK` (source: port)

## Resets Found


## Detection Rules

| Rule | Pattern |
|------|---------|
| Clock | Name contains 'clk' or 'clock' |
| Reset (active low) | Name ends with '_n' |
| Reset (active high) | Name contains 'rst' without '_n' |
| Async Reset | In sensitivity list: `@(posedge clk or negedge rst_n)` |
| Sync Reset | Inside always block: `if (rst) ...` |
