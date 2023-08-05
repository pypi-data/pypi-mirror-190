# Python to Javascript translator

## Usage

```python
import py2js

@py2js.js
def main():
    # code here
```

## Options: py2js.js

```python
func:              t.Optional[t.Callable] 
as_function:       t.Optional[bool]       
python_compatible: t.Optional[bool]       
```

## Examples

python

```python
import py2js
import typing

this = typing.Self

@py2js.js
def translated_normal():
    # assign
    a = 4

    # f-string
    console.log(f'{a} fstring')

    # class
    class Main:
        a: int
        def constructor():
            this.a = 1

        def func():
            console.log(this.a)
    
    Main().func()

    # try catch else finally
    try:
        raise SyntaxError('syntax error')
    except SyntaxError as e:
        console.log('syntax error raised')
    except:
        console.log('excepted')
    else:
        console.log('else')

    try:
        if Boolean(1):
            raise SyntaxError('syntax error')
    except:
        pass
    finally:
        console.log('finally')

    # while
    i = 10
    while i > 0:
        i -= 1
    
    # for-else
    for i in [0, 1, 2, 3]:
        if i > 2:
            break
    else:
        console.log('else')
    
    # compare
    i = 5
    if 0 < i < 9:
        console.log('true')

@py2js.js(python_compatible=True)
def translated_compatible():
    """
    class with self args
    """
    class Main:
        def __init__(self, value):
            self.a = value

        def func(self):
            console.log(self.a)
    
    Main('hello, world!').func()

with open('translated_normal.js', 'w') as f:
    f.write(translated_normal)

with open('translated_compatible.js', 'w') as f:
    f.write(translated_compatible)
```

### translated_normal.js

```javascript
// assign
let a = 4;
// f-string
console.log(`${a} fstring`);
// class
let Main = class {
    a;
    constructor() {
        this.a = 1
    };
    func() {
        console.log(this.a)
    }
    a
}
Main = new Proxy(Main, {
    apply: (clazz, thisValue, args) => new clazz(...args)
});;
Main().func();
// try catch else finally
_else: {
    try {
        throw SyntaxError(`syntax error`)
    } catch (_err) {
        if (_err instanceof SyntaxError) {
            e = _err;
            console.log(`syntax error raised`);
            break _else
        } {
            console.log(`excepted`);
            break _else
        }
    }
    console.log(`else`)
};
try {
    if (Boolean(1)) {
        throw SyntaxError(`syntax error`)
    }
} catch (_err) {
    {
        /* pass */
    }
} finally {
    console.log(`finally`)
};
// while
let i = 10;
while (i > 0) {
    i -= 1
};
// for-else
_else: {
    for (i of[0, 1, 2, 3]) {
        if (i > 2) {
            break _else
        }
    }
    console.log(`else`)
};
// compare
i = 5;
if (0 < i < 9) {
    console.log(`true`)
}
```

### translated_compatible.js

```javascript
// class with self args
let Main = class {
    constructor(...args) {
        if ('__init__' in this) this.__init__(this, ...args);
        return new Proxy(this, {
            apply: (target, self, args) => target.__call__(self, ...args),
            get: (target, prop, receiver) => {
                if (target[prop] instanceof Function) {
                    return (...args) => target[prop](target, ...args)
                } else {
                    return target[prop]
                }
            }
        })
    }
    __init__(self, value) {
        self.a = value
    };
    func(self) {
        console.log(self.a)
    }
}
Main = new Proxy(Main, {
    apply: (clazz, thisValue, args) => new clazz(...args)
});;
Main(`hello, world!`).func()
/*
hello, world!
*/
```
