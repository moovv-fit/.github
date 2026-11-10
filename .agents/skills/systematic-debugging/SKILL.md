---
name: systematic-debugging
description: Structured debugging methodology using reproduce-isolate-hypothesize-test-fix approach. Prevents guessing at fixes and ensures reliable bug resolution with root cause analysis.
inclusion: auto
---

# Systematic Debugging

Use this skill when debugging issues. Never guess at fixes — follow this methodology.

## The Debugging Process

```
┌────────────────────────────────────────────┐
│  1. REPRODUCE: Confirm the bug exists      │
│     ↓                                      │
│  2. ISOLATE: Narrow down the location      │
│     ↓                                      │
│  3. HYPOTHESIZE: Form theories about cause │
│     ↓                                      │
│  4. TEST: Verify or disprove hypotheses    │
│     ↓                                      │
│  5. FIX: Implement and verify the fix      │
│     ↓                                      │
│  6. PREVENT: Add test to prevent regression│
└────────────────────────────────────────────┘
```

## Step 1: REPRODUCE

Before debugging, confirm you can reproduce the issue.

### Questions to Answer
- What exact steps trigger the bug?
- What is the expected behavior?
- What is the actual behavior?
- Is it consistent or intermittent?
- What environment (OS, browser, Node version)?

### Document the Reproduction

```markdown
## Bug Report
**Steps:**
1. Navigate to /users
2. Click "Create User"
3. Fill form with email "test@example.com"
4. Click "Submit"

**Expected:** User created, redirect to /users
**Actual:** Error "Cannot read property 'id' of undefined"
**Environment:** Chrome 120, macOS, Node 20.11
**Frequency:** 100% reproducible
```

## Step 2: ISOLATE

Narrow down where the bug originates.

### Binary Search Method

If the error occurs deep in a call chain, use binary search:

```typescript
async function processOrder(orderId: string) {
  console.log('[DEBUG] Starting processOrder'); // Checkpoint 1

  const order = await fetchOrder(orderId);
  console.log('[DEBUG] After fetchOrder:', order); // Checkpoint 2

  const validated = validateOrder(order);
  console.log('[DEBUG] After validateOrder:', validated); // Checkpoint 3

  const result = await submitOrder(validated);
  console.log('[DEBUG] After submitOrder:', result); // Checkpoint 4

  return result;
}
```

Run and identify which checkpoint shows the issue.

### Isolate with Minimal Reproduction

Create the smallest code that reproduces the bug:

```typescript
// Minimal reproduction case
const result = calculateDiscount({
  price: 100,
  discount: null, // This causes the bug
});
// Error: Cannot read property 'percent' of null
```

## Step 3: HYPOTHESIZE

Form theories about the root cause. Write them down.

### Common Hypothesis Categories

**Data Issues:**
- Unexpected null/undefined
- Wrong data type
- Missing required field
- Data out of expected range

**State Issues:**
- Race condition
- Stale state
- Incorrect initialization
- State not cleaned up

**Logic Issues:**
- Off-by-one error
- Incorrect condition
- Missing case in switch/if
- Wrong operator (== vs ===)

**Environment Issues:**
- Environment variable not set
- Wrong configuration
- Missing dependency
- Version mismatch

### Example Hypotheses

```markdown
## Hypotheses for "Cannot read property 'id' of undefined"

1. The API returns null instead of user object
2. The API response structure changed
3. The user variable is shadowed somewhere
4. An async operation completes after component unmount
```

## Step 4: TEST HYPOTHESES

Test each hypothesis systematically. Start with the most likely.

### Testing Hypothesis 1: API Returns Null

```typescript
// Add logging to test hypothesis
const response = await fetch('/api/users', { method: 'POST', body });
const data = await response.json();

console.log('[DEBUG] API response status:', response.status);
console.log('[DEBUG] API response data:', JSON.stringify(data, null, 2));

// If data is null, hypothesis 1 is confirmed
```

### Testing Hypothesis 2: Response Structure Changed

```typescript
// Check actual vs expected structure
console.log('[DEBUG] Response keys:', Object.keys(data));
console.log('[DEBUG] Has user property:', 'user' in data);
console.log('[DEBUG] User type:', typeof data.user);
```

### Eliminate Hypotheses

```markdown
## Hypothesis Testing Results

1. ❌ API returns null → API returns valid response
2. ✅ Response structure changed → API now returns { data: { user: {...} }}
3. Not tested (hypothesis 2 confirmed)
4. Not tested (hypothesis 2 confirmed)

ROOT CAUSE: API response structure changed from { user } to { data: { user }}
```

## Step 5: FIX

Implement the fix based on confirmed root cause.

### Fix Guidelines

1. **Fix the root cause, not the symptom**
2. **Make the minimal change needed**
3. **Don't fix unrelated issues in the same change**
4. **Verify the fix in the same environment**

```typescript
// Before (broken)
const user = response.user;

// After (fixed)
const user = response.data?.user;
```

### Verify the Fix

1. Run the reproduction steps
2. Confirm the bug no longer occurs
3. Check for regressions in related functionality

## Step 6: PREVENT REGRESSION

Add a test that would have caught this bug.

```typescript
it('handles nested API response structure', async () => {
  // Mock the new API response structure
  mockFetch.mockResolvedValue({
    ok: true,
    json: () => Promise.resolve({
      data: { user: { id: '123', name: 'Test' } }
    }),
  });

  const user = await createUser({ email: 'test@example.com', name: 'Test' });

  expect(user.id).toBe('123');
});
```

## Debugging Tools

### Console Methods

```typescript
console.log('Simple value:', value);
console.table(arrayOfObjects);         // Tabular display
console.dir(object, { depth: null }); // Full object inspection
console.trace('Call stack here');     // Print stack trace
console.time('operation');            // Start timer
// ... operation
console.timeEnd('operation');         // End timer and print
```

### Debugger Statement

```typescript
function processData(data) {
  debugger; // Execution pauses here in DevTools
  return data.map(item => transform(item));
}
```

### Error Stack Traces

```typescript
try {
  riskyOperation();
} catch (error) {
  console.error('Error:', error.message);
  console.error('Stack:', error.stack);
  throw error; // Re-throw after logging
}
```

## Common Bug Patterns

### Null/Undefined Access

```typescript
// Bug: data might be undefined
const value = data.nested.value;

// Fix: Optional chaining
const value = data?.nested?.value;

// Fix: With default
const value = data?.nested?.value ?? defaultValue;
```

### Async/Await Issues

```typescript
// Bug: Forgot await
const result = fetchData(); // result is Promise, not data

// Fix: Add await
const result = await fetchData();
```

### Closure Over Loop Variable

```typescript
// Bug: All callbacks use final value of i
for (var i = 0; i < 10; i++) {
  setTimeout(() => console.log(i), 100); // Prints 10 ten times
}

// Fix: Use let (block scope)
for (let i = 0; i < 10; i++) {
  setTimeout(() => console.log(i), 100); // Prints 0-9
}
```

### State Mutation

```typescript
// Bug: Mutates original array
const sorted = items.sort();

// Fix: Create new array
const sorted = [...items].sort();
```

## When to Ask for Help

- After 30 minutes without progress
- When you've eliminated all hypotheses
- When the bug requires domain knowledge you lack
- When it might be a known issue (check issue trackers first)
