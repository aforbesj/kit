# TypeScript standards (browser UI only)

- `tsc --noEmit` passes in strict mode; `any` appears only at untyped library edges.
- Tests use vitest and run in seconds.
- Components take typed props and hold UI state only; data logic lives behind a typed service module.
- Deep modules: each folder exposes one `index.ts` over a substantial inside.
- Names come from `CONTEXT.md`.
- Dependencies go through `pnpm add`.
