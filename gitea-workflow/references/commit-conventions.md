# Commit Message Conventions

Follow conventional commits format for clear, searchable history.

## Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

## Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style (formatting, no logic change)
- **refactor**: Code refactoring
- **test**: Adding or modifying tests
- **chore**: Maintenance (dependencies, build config)
- **perf**: Performance improvements

## Scope

Optional. Indicates what part of codebase is affected:
- Module name: `feat(auth):`
- Component: `fix(user-service):`
- Area: `docs(api):`

## Subject

- Use imperative mood: "add" not "added" or "adds"
- No capital first letter
- No period at end
- Max 50 characters

## Examples

### Feature

```
feat(auth): add JWT token validation

Implement token validation middleware with:
- Expiration checking
- Signature verification
- Issuer validation

Closes #123
```

### Bug Fix

```
fix(api): handle null response from external service

Add null check and default value when external API
returns null to prevent application crashes.

Fixes #456
```

### Documentation

```
docs(readme): update installation instructions

Add section for Docker installation and clarify
dependency requirements.
```

### Refactoring

```
refactor(user-service): extract validation logic

Move validation logic to separate validators module
to improve code organization and testability.
```

### Test

```
test(auth): add integration tests for login flow

Add tests covering:
- Successful login
- Invalid credentials
- Token expiration
```

### Chore

```
chore(deps): update dependencies to latest versions

Update pytest to 8.3.0 and ruff to 0.6.0 for
latest features and bug fixes.
```

## Breaking Changes

Indicate breaking changes with `!` or in footer:

```
feat(api)!: change user endpoint response format

BREAKING CHANGE: User endpoint now returns nested
object instead of flat structure.

Before: {"id": 1, "name": "John"}
After: {"user": {"id": 1, "name": "John"}}
```

## References

Link to issues or pull requests in footer:

```
Closes #123
Fixes #456
Refs #789
```

## Best Practices

1. **One commit per logical change**
2. **Write clear, descriptive subjects**
3. **Explain why, not what** - Code shows what, commit explains why
4. **Keep commits atomic** - Each commit should be complete and functional
5. **Use body for context** - Explain motivation and implementation approach
