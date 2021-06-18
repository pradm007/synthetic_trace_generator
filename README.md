# Synthetic Trace Generator

Create synthetic trace using regex pattern. Output would be a `.csv` file with `Timestamp` and `Event` column.

## Usage
Run
``` generator.py --regex abc+ --traceLength 1000 ```

Arguments:
1. `regex` : Enter a valid regex pattern
2. `traceLength` : Provide a valid traceLength [ No garauntees of exact length but it would be minimum of this size ]
3. `temporalPattern` : One of the following
    * Alternating
    * Response
    * Multicause
    * Multieffect
    
4. `alpbhabetlen`: Size of the alpbhabet. (max 26, min 2) [ Currently not in operational ]

## License
Apache License
