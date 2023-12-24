# Ideas for part 2 of Day 12

Can we solve this faster by focusing on the **contiguous group of damaged springs** numbers?

Let me explore one simple pattern here: `3,2,1`.  In the sample data, this comes with **row** `?###????????`.

To start, I'll ignore the details in that **row**, just remembering that there are 12 total **springs**.

Lets first name the smallest valid **condition record**:

```
###.##.#
```

This would be a valid **condition record** if there were 8 **springs**.

What if there were 9?

We take the above and insert a spring in one of four places:

```
.###.##.#
###..##.#
###.##..#
###.##.#.
```

Recursing on the above inserting a . at each of the above might explode, so permit me to rewrite this with variables:

```
w###x##y#z
```

To generate a sequence, all we need to do is select numbers larger than zero for `w`, `x`, `y`, and `z` which sum to the total number of springs.

Once we have a programmatic way to generate these, I suspect it will be very easy to then use the **condition record** to filter that set.

?
