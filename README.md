# binomial_trees_pricing
Computing option price (put or call) of (european or american) options, using the Binomial Tree approach

The deprecated file binomial_tree_finance_bfs implements using Post order DFS to create nodes and a BFS to compute... However, it's too slow !

The current implementation uses numpy arrays to support larger number of steps more efficiently

See _tests.py for examples

## Usage
```
    time_to_expire_yrs = 2
    num_steps = 5
    vol = 0.3
    risk_free = 0.05
    price = 50
    exercise_price = 52

    option_side = 'put'
    option_type = 'american'

    option_price = compute(price=price, vol=vol, num_steps=num_steps, time_to_expire=time_to_expire_yrs,
                           exercise_price=exercise_price, option_side=option_side, risk_free=risk_free,
                           option_type=option_type)
    print(option_price)
```