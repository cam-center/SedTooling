class Patterns:
    TYPE_PATTERN = "[><A-Za-z0-9_-]+(::[A-Za-z0-9_-]+)*(<( *(?R) *, *)*(?R)>)?"
    TYPE_CHARS = "[ ><A-Za-z0-9_:,-]+"
    IDENTIFIER_PATTERN = "[A-Za-z0-9_-]+"
    IDENTIFIER_REFERENCE = "#[A-Za-z0-9_-]+"
