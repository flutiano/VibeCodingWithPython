# Plan - 011_flappy-bird-refactored

Extract common functionality from `Bird`, `Pipe`, `Cloud`, and `Coin` into a `GameObject` base class.

## Proposed Changes

### [011_flappy-bird-refactored]

#### [MODIFY] [main.py](file:///Users/jeffzo/projects/practice/AIcoding/VibeCodingWithPython/011_flappy-bird-refactored/main.py)

- Define `GameObject` base class:
    - `__init__(self, x, y, width, height, speed=0)`: Standardizes property names.
    - `update(self)`: Provides default horizontal movement logic.
    - `is_off_screen(self)`: Provides default logic to check if an object has left the screen on the left.
- Refactor `Bird`:
    - Inherits from `GameObject`.
    - Overrides `update` to apply gravity (replaces `apply_gravity`).
- Refactor `Pipe`:
    - Inherits from `GameObject`.
    - Uses `super().update()` and syncs the bottom rect's position.
- Refactor `Cloud`:
    - Inherits from `GameObject`.
    - Uses inherited `update` and `is_off_screen`.
- Refactor `Coin`:
    - Inherits from `GameObject`.
    - Uses inherited `update` and `is_off_screen`.

## Verification Plan

### Automated Tests
- Run `python 010_flappy-bird/main.py` and verify:
    - Game launches.
    - Entities move.
    - Collision works.

### Manual Verification
- Visual check of bird physics and coin collection.