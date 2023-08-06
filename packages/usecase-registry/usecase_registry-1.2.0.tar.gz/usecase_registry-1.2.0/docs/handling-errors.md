# *Handling errors*

Errors are a fact of life in software, in fact errors are part of your software and must be handled. For what I have studied, `rust` programming language has the best ***error handling*** system. Long story short, in `rust` there are two types of errors: *Recoverable and unrecoverable* erros. For a recoverable error, we most likely just want to report the problem to the client calling the failing code and let the client decide how to handle the encountered error. Unrecoverable errors are always symptoms of bugs, like trying to access a location beyond the end of an array, and so we want to immediately stop the program.

Most languages, like `python` for instance, don't distinguish between these two kinds of errors and handle both in the same way, using mechanism such as exceptions. In `rust` there are no exceptions, instead the language has a type called `Result<T, E>` for recoverable errors and the `panic!` macro that stops the system execution when the program encounters ans unrecoverable error.

!!! tip
    [Official Rust documentation about error handling](https://doc.rust-lang.org/book/ch09-00-error-handling.html)

There are some `python` libraries that provide a rust-like error handling system. I like to use [`result`](https://pypi.org/project/result/). The key with this system is that when a client calls some code, code recoverable exceptions are also embedded in the type annotation of the function, so it enforces a correct error handling of these expected error.

## Code coverage
If you're code deals with not deterministic code, `100%` coverage most likely means your code doesn't properly handle errors. Not covered code should correspond to code that will be tested with `integration tests` and code that covers the `non-happy path` in your code.

!!! tip
    [Railway oriented programming](https://blog.logrocket.com/what-is-railway-oriented-programming/)

When thinking about writing code you most likely always think about the happy path. Without considering everything can fails at any time.
