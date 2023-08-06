# NOANYIO
import trio


async def foo():
    # not async
    trio.run()

    # safely awaited
    await trio.aclose_forcefully()
    await trio.open_file()
    await trio.open_ssl_over_tcp_listeners()
    await trio.open_ssl_over_tcp_stream()
    await trio.open_tcp_listeners()
    await trio.open_tcp_stream()
    await trio.open_unix_socket()
    await trio.run_process()
    await trio.serve_listeners()
    await trio.serve_ssl_over_tcp()
    await trio.serve_tcp()
    await trio.sleep()
    await trio.sleep_forever()
    await trio.sleep_until()

    # all async functions
    trio.aclose_forcefully()  # error: 4, "aclose_forcefully", "trio"
    trio.open_file()  # error: 4, "open_file", "trio"
    trio.open_ssl_over_tcp_listeners()  # error: 4, "open_ssl_over_tcp_listeners", "trio"
    trio.open_ssl_over_tcp_stream()  # error: 4, "open_ssl_over_tcp_stream", "trio"
    trio.open_tcp_listeners()  # error: 4, "open_tcp_listeners", "trio"
    trio.open_tcp_stream()  # error: 4, "open_tcp_stream", "trio"
    trio.open_unix_socket()  # error: 4, "open_unix_socket", "trio"
    trio.run_process()  # error: 4, "run_process", "trio"
    trio.serve_listeners()  # error: 4, "serve_listeners", "trio"
    trio.serve_ssl_over_tcp()  # error: 4, "serve_ssl_over_tcp", "trio"
    trio.serve_tcp()  # error: 4, "serve_tcp", "trio"
    trio.sleep()  # error: 4, "sleep", "trio"
    trio.sleep_forever()  # error: 4, "sleep_forever", "trio"
    trio.sleep_until()  # error: 4, "sleep_until", "trio"

    # safe
    async with await trio.open_file() as f:
        pass

    async with trio.open_file() as f:  # error: 15, "open_file", "trio"
        pass

    # safe in theory, but deemed sufficiently poor style that parsing
    # it isn't supported
    k = trio.open_file()  # error: 8, "open_file", "trio"
    await k

    # issue #56
    nursery = trio.open_nursery()
    await nursery.start()
    await nursery.start_foo()

    nursery.start()  # error: 4, "start", "nursery"
    None.start()
    nursery.start_soon()
    nursery.start_foo()
