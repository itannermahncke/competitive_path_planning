"""
ChatGPT suggested unit tests:

__init__

✅ Grid is correct shape (size, size)

✅ Agent positions correctly placed

✅ Obstacle count ≈ floor(size * density)
(May need statistical tolerance due to randomness)

_get and _set

✅ _set() correctly assigns occupancy value

✅ _get() retrieves same value

✅ Out-of-bounds calls return None and print error

is_within_bounds

✅ (0,0) → True

✅ (size-1, size-1) → True

✅ (size, 0) → False

get_neighbors

✅ Returns 2–4 valid cells (fewer on edges/corners)

✅ Never includes out-of-bounds or obstacle cells

✅ Returns [] if surrounded by obstacles

move_agent

✅ Moves agent and clears old cell

✅ Prevents moving into obstacles or other agents

✅ Prevents moving from an empty cell

get_distance

✅ Returns 0 when same cell

✅ Returns 1 for adjacent cells

✅ Returns correct value for known grid

✅ Returns None when no path exists (blocked by obstacles)
"""
