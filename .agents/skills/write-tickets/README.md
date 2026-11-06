# write-tickets (Codex CLI skill)

Create reviewable, independently verifiable feature tickets with `rd.md`, `eval.md`, and a dependency-aware board. Tickets stay `draft` until explicit user approval. The board can propose *candidate* parallel groups but does not dispatch agents.

## Install

Extract `write-tickets/` to the repository's `.agents/skills/` or your user scope `~/.agents/skills/`. The installation path and syntax may vary by Codex CLI version; confirm with your installed Codex documentation. Invoke with `$write-tickets` or ask Codex to write implementation tickets.

## Default generated repository layout

```text
tickets/
  board.json             # canonical status/graph/approval metadata
  BOARD.md               # generated candidate-work board
  001-user-login/
    rd.md                # requirements
    eval.md              # acceptance checks
  002-task-board/
    rd.md
    eval.md
```

Repository conventions take precedence. The skill creates no tickets merely by being installed.

## Offline helpers (Python 3, standard library)

```sh
python path/to/write-tickets/scripts/ticket_board.py validate --root tickets
python path/to/write-tickets/scripts/ticket_board.py render --root tickets --write
python path/to/write-tickets/scripts/ticket_board.py validate --root tickets --check-rendered
python path/to/write-tickets/scripts/ticket_board.py fingerprint --root tickets --id 001-user-login
python -m unittest discover -s path/to/write-tickets/scripts -p 'test_*.py' -v
```

`fingerprint` is only a content hash. The skill may record it **after** actual user approval; the program cannot authenticate that approval. A ready ticket is not automatically eligible to launch. See `references/board-contract.md` for statuses and resource isolation.

## Verification status

Package-local tests validate parser, coverage, graph, stale approval, board overwrite protection, and dispatch planning. This is not evidence of Codex CLI activation, agent-browser execution, or skill-vs-baseline improvement.
