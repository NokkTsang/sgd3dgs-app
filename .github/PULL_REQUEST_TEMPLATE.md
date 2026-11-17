## Summary

What outcome does this change produce, and which issue does it address?

## Scope

- [ ] Product/editor change
- [ ] Core/schema change
- [ ] Documentation/infrastructure
- [ ] SuperSplat upstream refresh (must not contain feature work)

## Evidence

List commands, tests, metrics, screenshots, or recordings used to verify the
change.

```text
make core-check
make editor-test
```

## Data and compatibility

- Does this change Gaussian ordering, scene schema, labels, transforms, or
  stored editor projects?
- Are migrations or index maps required?
- Which source scene/checksum was used?
- Is a linked `sgd3dgs-research` issue or adapter version involved?

## Licensing and provenance

- Did the change copy third-party code into the app? If so, why is an artifact
  boundary insufficient?
- Are runtime dependency licenses recorded in `THIRD_PARTY.md`?
- Is generated content clearly distinguishable from observed content?

## Checklist

- [ ] The task fits the agreed weekly scope.
- [ ] Tests or reproducible commands are included.
- [ ] Documentation is updated.
- [ ] No private data, credentials, weights, or large scene assets are committed.
- [ ] The PR is small enough for a focused review.
- [ ] Editor changes include a screenshot or short recording when applicable.
