from pythonpoet.types.import_ import Import, ImportBuilder
from pythonpoet.types import Builder, DeserializableType, Documentable
from pythonpoet.types.decorator import Decoratorable, Decorator
from pythonpoet.types.field import ClassFieldBuilder, ClassField
from pythonpoet.types.method import Method, MethodBuilder


def _generate_decorators(decorators: list[Decorator]) -> str:
    decorators_source_code = ""
    for decorator in decorators:
        decorators_source_code += decorator.deserialize()
    return decorators_source_code


def _generate_class_header(class_name: str, extends: str, comments: str) -> str:
    if len(extends) == 0:
        class_header = f"class {class_name}:\n"
    else:
        class_header = f"class {class_name}({extends}):\n"
    return f"{class_header}{comments}\n"


def _generate_class_fields(fields: list[ClassField]) -> str:
    fields_source_code = ""
    for field in fields:
        fields_source_code += field.deserialize()
    return fields_source_code


def _generate_class_methods(methods: list[Method]) -> str:
    methods_source_code = "\t"
    for method in methods:
        methods_source_code += f"{method.deserialize()}\n\t"
    return methods_source_code


class Class(DeserializableType):
    """
    Representation of a class.

    .. warning::

        You shouldn't initialize this class via the `__init__`. Use :class:`ClassBuilder` instead.

    Attributes
    ----------
    name : str
        Class' name.
    fields : list[:class:`ClassField`]
        Class' fields.
    extends : str
        Class(-es) that this class extends.
    methods : list[:class:`Method`]
        Class' methods.
    imports : list[:class:`Import`]
        Class' imports.
    decorators : list[:class:`Decorator`]
        Class' decorators.
    comments : list[str]
        Class' comments.
    """

    def __init__(
        self,
        name: str,
        extends: str,
        imports: list[Import],
        fields: list[ClassField],
        decorators: list[Decorator],
        methods: list[Method],
        comments: list[str],
    ) -> None:
        self.name = name
        self.fields = fields
        self.extends = extends
        self.methods = methods
        self.imports = imports
        self.decorators = decorators
        self.comments = comments

    def get_imports(self) -> str:
        imports = ""
        for decorator in self.decorators:
            imports += decorator.get_imports()
        for field in self.fields:
            imports += field.get_imports()
        for import_ in self.imports:
            imports += import_.to_string()
        return imports

    def deserialize(self) -> str:
        base = _generate_decorators(self.decorators) + _generate_class_header(
            self.name,
            self.extends,
            Documentable.generate_comments_source(self.comments),
        )
        if self.fields is not None and len(self.fields) > 0:
            base += _generate_class_fields(self.fields)
        if self.methods is not None and len(self.methods) > 0:
            base += _generate_class_methods(self.methods)
        return base

    def __repr__(self) -> str:
        return (
            f"<Class name={self.name}, decorators={self.decorators}, "
            f"fields={self.fields}, methods={self.methods}, "
            f"imports={self.imports}, extends={self.extends}>"
        )

    def __str__(self) -> str:
        return self.__repr__()


class ClassBuilder(Builder, Decoratorable, Documentable):
    """
    Builder for the :class:`Class`.

    Attributes
    ----------
    name : str or None, default: None
        Class' name.
    extends : list[str]
        Class(-es) that this class extends.
    methods : list[:class:`Method`]
        Class' methods.
    imports : list[:class:`Import`]
        Class' imports.
    fields : list[:class:`ClassField`]
        Class' fields.
    """

    def __init__(self) -> None:
        super(Builder, self).__init__()
        super(Decoratorable, self).__init__()
        super(Documentable, self).__init__()

        self.name: str | None = None
        self.extends: list[str] = []
        self.methods: list[Method] = []
        self.imports: list[Import] = []
        self.fields: list[ClassField] = []

    def set_name(self, name: str) -> "ClassBuilder":
        """
        Sets class' name.

        Parameters
        ----------
        name : str
            New name of the class.

        Returns
        -------
        :class:`ClassBuilder`
            Updated builder's instance.
        """
        self.name = name
        return self

    def add_field(self, builder: ClassFieldBuilder) -> "ClassBuilder":
        """
        Adds a new fields from the builder.

        Parameters
        ----------
        builder : :class:`ClassFieldBuilder`
            Builder of the field to be added.

        Returns
        -------
        :class:`ClassBuilder`
            Updated builder's instance.
        """
        self.fields.append(builder.build())
        return self

    def add_extends(self, class_: str, import_: ImportBuilder = None) -> "ClassBuilder":
        """
        Adds a new class to the list of extendable classes.

        Parameters
        ----------
        import_ : :class:`ImportBuilder`, optional, default: None
            Extendable class import.
        class_ : str
            Class to extend from.

        Returns
        -------
        :class:`ClassBuilder`
            Updated builder's instance.
        """
        self.extends.append(class_)
        if import_ is not None:
            self.imports.append(import_.build())
        return self

    def add_method(self, builder: MethodBuilder) -> "ClassBuilder":
        """
        Adds a new method to this class.

        Parameters
        ----------
        builder : :class:`MethodBuilder`
            Builder of the method to be added.

        Returns
        -------
        :class:`ClassBuilder`
            Updated builder's instance.
        """
        self.methods.append(builder.build())
        return self

    def build(self) -> Class:
        if self.name is None:
            raise ValueError("Class' name cannot be None.")

        return Class(
            self.name,
            ",".join(self.extends),
            self.imports,
            self.fields,
            self.decorators,
            self.methods,
            self.comments,
        )
