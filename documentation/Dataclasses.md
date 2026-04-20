# What are data classes?
data classes are regular python classes that :
    - take much less code to implement the same functionality. 
    - that is mainly used to store data.

The only special thing is:
you add a decorator *@dataclass* on top, and Python auto‑creates a bunch of boring methods for you.

Those methods are usually things like:

    __init__ (the constructor)

    __repr__ (nice string when you print it)

    __eq__ (compare two objects)

So you write less code, but get the same (or better) behavior.

[DataClass_Tutorial] (https://www.datacamp.com/tutorial/python-data-classes)

## 2. Without data classes (the old way)
Imagine you want to store info about a person: python
```
class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"Person(name={self.name!r}, age={self.age!r})"
```
You had to:

    write __init__ by hand

    write __repr__ by hand

    maybe also __eq__ if you want to compare two people

That’s a lot of boilerplate.

##  3. With data classes (the new way)
Now with dataclasses: python
```
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int
```
That’s it.

Python will automatically:

    create __init__(self, name, age)

    create a nice __repr__

    create __eq__ so you can compare two Person objects

You can use it like this: python
```
p1 = Person("Diya", 20)
p2 = Person("Diya", 20)

print(p1)          # Person(name='Diya', age=20)
print(p1 == p2)    # True
```
You didn’t write any of that logic yourself—@dataclass did it.

#### NOte:
- The *@dataclass* decorator is used to automatically add special methods to the class.

## 4. Data classes require type hints
As you might have noticed, data classes require type hints when defining fields. 

In fact, data classes allow any type from the typing module. For example, here is how to create a field that can accept Any data type:
```
from typing import Any
from dataclasses import dataclass



@dataclass
class Person:
   name: Any

```
Explaination:

    - Any is a special type hint that can be any type. It's like an escape hatch for type checking.

    - The @dataclass decorator is a built-in Python decorator that auto-generates special methods in classes, including the __init__, __repr__, and __eq__ methods.

    - The Person class is defined with a single attribute name which can be of any type, as indicated by Any.

## 5. Adding default values
You can also give fields default values: python
```
from dataclasses import dataclass

@dataclass
class Student:
    name: str
    age: int = 18   # default age

CLI:

s1 = Student("Diya")
print(s1)  # Student(name='Diya', age=18) 
```

### Note:
Keep in mind that non-default fields can’t follow default fields. For example, the below code will throw an error:
```
@dataclass
class Exercise:
   name: str = "Push-ups"
   reps: int = 10
   sets: int = 3
   weight: float  # NOT ALLOWED


ex5 = Exercise()
ex5
TypeError: non-default argument 'weight' follows default argument
```
In practice, you will rarely define defaults with *name: type = value syntax.*

Instead, you will use the field function, which allows more control of each field definition:
```
from dataclasses import field


@dataclass
class Exercise:
   name: str = field(default="Push-up")
   reps: int = field(default=10)
   sets: int = field(default=3)
   weight: float = field(default=0)


# Now, all fields have defaults
ex5 = Exercise()
ex5
Exercise(name='Push-up', reps=10, sets=3, weight=0)
```

------------------------------------------------------------------
# 3 . data class in LanGraph state schemas
In LangGraph / state schema world, a data class can be used to define state in a clean way: python
```
from dataclasses import dataclass
from typing import List
from langchain_core.messages import BaseMessage

@dataclass
class State:
    messages: List[BaseMessage]
    name: str
    age: int
```
This:

    - Clearly describes what the state contains
    - Provides an auto-generated __init__ (and other dunder methods)
    - Easy to read and maintain
    - Alternative to TypedDict for defining state

6. Mental model :
Think of a data class as:

“A neat, compact way to define a class that mostly just holds data.”

You focus on what you want to store, Python handles the how.
