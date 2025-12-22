# Atom: Profile Execution
@description Runs cProfile on a target and returns structured stats.

**Role:** Performance Analyst.

**Context:** Accurately measure execution time and identify bottlenecks.

**Inputs:**
- `target_script`: Path to the python script to run.

**Task:**
1. Run the target script using `cProfile`.
2. Parse the output to find total time and top function calls.

**Execution:**
// turbo
   - `python -m cProfile -o profile.stats [target_script]`
   - `python -c "import pstats, json; p = pstats.Stats('profile.stats'); p.strip_dirs().sort_stats('cumulative'); print(json.dumps({'total_time': p.total_tt, 'top_calls': [{'func': str(func), 'time': stats[3]} for func, stats in list(p.stats.items())[:5]]}))"`

**Output Format:** JSON
```json
{
  "total_time": <float_seconds>,
  "top_calls": [
    {"func": "(function_name, line, file)", "time": <cumulative_time>}
  ]
}
```

