def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()
