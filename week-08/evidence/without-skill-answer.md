The test expectation is correct. There are **two implementation defects**:

1. **AC4: touching endpoints are treated as overlaps.** For this fixture, `660 <= 660 && 720 >= 600` is `true`, so `canBook` returns `false`. The intervals only touch at 660; overlap comparisons must be strict.
2. **AC5: successful checks mutate bookings.** `bookings.push(...)` changes the input. The current early return avoids this mutation, and the failed first assertion prevents the immutability assertion from running. Fixing only AC4 exposes AC5.

Proposed minimal patch:
```
   for (const b of bookings) {
-    if (start <= b.end && end >= b.start) return false;
+    if (start < b.end && end > b.start) return false;
   }
-  // keep the room's list current with the slot that was just found free
-  bookings.push({ start, end });
   return true;
```

Keep the existing endpoint test unchanged. Add this independent regression test for mutation, using a slot clearly separated from the existing booking:
```
it('AC5: checking a free slot leaves bookings unchanged', () => {
  const request = {
    start: 780,
    end: 840,
    now: 540,
    blocked: false,
    bookings: [{ start: 600, end: 660 }],
  };
  const before = structuredClone(request.bookings);

  const result = canBook(request);

  expect(request.bookings).toEqual(before);
  expect(result).toBe(true);
});
```

This additional test catches mutation even while the endpoint bug remains.

An isolated JavaScript reproduction confirmed:

| Implementation   | Result for reported fixture | Bookings unchanged |
| ---------------- | --------------------------- | ------------------ |
| Original         | `false`                     | Yes                |
| Overlap fix only | `true`                      | No                 |
| Both fixes       | `true`                      | Yes                |

No code was edited.
