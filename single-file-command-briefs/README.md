# Single-File Executive Command Brief

Portfolio artifact #5 for the Forward-Deployed AI Systems Workbench.

**HTML + local vendor assets (ECharts, jQuery, DataTables)** — zero-install executive snapshot for restricted / air-gapped environments.

## Run

```bash
open index.html
# or
python -m http.server 8765 --directory .
```

No CDN required. Layout CSS is inline; JS/CSS load only from `vendor/`.

## Layout

```
single-file-command-briefs/
  index.html
  vendor/
    echarts.min.js
    jquery.min.js
    jquery.dataTables.min.js
    jquery.dataTables.min.css
  README.md
```

## Accept

- Double-click without Node toolchain.
- Works offline after the `vendor/` folder is present (committed in-repo).
- Governance strip + KPIs + chart + alert table.
