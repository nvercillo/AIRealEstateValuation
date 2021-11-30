def abstractmethod(func):
    """Decorator that prevents implementation."""

    def wrap(*args, **kwargs):
        raise NotImplementedError("Cannot Call Abstract Method")

    return wrap


class AbstractBaseClass:
    __abstract__ = True

    def __init__(self) -> None:
        raise Exception("Cannot Implement AbstractBaseClass")


# class A(AbstractBaseClass):
#     def __init__(self) -> None:

#         if type(self) == A.__class__:
#             raise Exception("Cannot Implement AbstractBaseClass")

#     def __initalize__(self):

#         object_methods = set(
#             {
#                 method_name
#                 for method_name in dir(self.__class__)
#                 if callable(getattr(self, method_name)) and method_name[:2] != "__"
#             }
#         )

#         abstract_object_methods = set(
#             {
#                 method_name
#                 for method_name in dir(A)
#                 if callable(getattr(self, method_name)) and method_name[:2] != "__"
#             }
#         )

#         safeprint(abstract_object_methods, object_methods)
#         for o_method in abstract_object_methods:
#             if o_method not in object_methods:
#                 raise NotImplementedError(
#                     f'Abstract method "{o_method}" not implemented'
#                 )

#     @abstractmethod
#     def deact():
#         pass

#     @abstractmethod
#     def act():
#         pass


# sclass B(A):
#     def __init__(self) -> None:
#         super().__initalize__()
#         pass

#     def act(self):
#         safeprint("SDfsdf")

#     def hehe(self):
#         pass

# def deact(self):
#     safeprint("SDfsdf")


# AbstractBaseClass()

# b = B()

# b.act()
