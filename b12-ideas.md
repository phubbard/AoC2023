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

## More thoughts...

The size of some of the upcoming permutations has me very loathe to attempt to build out the permutations in memory in advance: other AoC problems have died here.

It could be interesting to try and use the Python generator concept recursively to do this, but I'm a little loathe to go too far here in case I need to go to a metal approach like C or Cuda.

So how can I simply number these permutations?
Let me try recursive from small.

### If only 2 variables

Lets say I have 2 variables and the target sum is `N`.

The sets are:
```
1, N-1
2, N-2
3, N-3
...
N-2, 2
N-1, 1
```

Clearly N-1.
