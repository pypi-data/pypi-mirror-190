# YYSUT


### plist

#### chain call

I implemented chain call of list in class `plist`.

currently, I implemented `map`, `filter`, `reduce`, `any`, `all` method.

You can use `log()` method to print the intermediate result.

```python
from yysut import plist
ans=plist(range(10)).log(lambda x:print(f"origin : {x}"))\
    .filter(lambda x: x % 2 == 0).log(lambda x:print(f"filter ans : {x}"))\
    .map(lambda x: x * 2).log(lambda x:print(f"map ans : {x}"))\
    .reduce(lambda x, y: x + y)
print(ans)
"""
origin : 0 ,1 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9
filter ans : 0 ,2 ,4 ,6 ,8
map ans : 0 ,4 ,8 ,12 ,16
40
"""
```

#### indexs

```python
from yysut import plist
ans=plist(range(100))
# get item
print(ans[2,5,7]) # [2, 5, 7]
print(ans[2:5]) # [2, 3, 4]
# set item
ans[2,5,7]=0
print(ans[:10]) # [0, 1, 0, 3, 4, 0, 6, 0, 8, 9]
```

#### groupby

```python
from yysut import plist
# 1. return dict type
ans=plist(range(10)).groupby(lambda x:x%2)
print(ans) # {0: [0, 2, 4, 6, 8], 1: [1, 3, 5, 7, 9]}
# 2. return list type
ans=plist(range(10)).groupby(lambda x:x%2,return_type="list")
print(ans) # [[0, 2, 4, 6, 8], [1, 3, 5, 7, 9]]
```

#### sort

`sort` method is same as python3 `sorted` method, it returns new list.

```python
from yysut import plist
ans=plist(range(10)).sort(lambda x:x%2)
print(ans) # [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]
```

#### parllal

The method is similar to `map` method, but it can use multi process.

! Attention: `parllal` method could not use lambda function.

```python
from yysut import plist
import time
def compute_func(x):
    time.sleep(1)
    return x**2
# parallel
t=time.time()
ans=plist(range(5)).parallel(
     # n is the number of process, -1 means all process
    compute_func,n=-1
).log(lambda x:print(x,"time:",time.time()-t))
# [0, 1, 4, 9, 16] time: 2.0206313133239746
# normal
t=time.time()
ans=plist(range(5)).map(
    compute_func
).log(lambda x:print(x,"time:",time.time()-t))
# [0, 1, 4, 9, 16] time: 5.004805564880371
```