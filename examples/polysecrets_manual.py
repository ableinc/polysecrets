from polysecrets import PolySecrets

config = dict(
        secret='rAnd0m_s3cr3t',  # default
        length=10,  # default
        interval=5,  # default = 30 (only if you're using automated)
        uuid=True,  # default
        mixcase=False,  # default
        persistence={}  # or False / default: False
    )


def manual_example():
    """
    Example of Polysecrets manually. We're creating a one time secret from the provided
    secret string.
    :return:
    """

    secret = PolySecrets(config).manual()
    print('Manual - Secret: ', secret)  # confirm secret is available


if __name__ == '__main__':
    manual_example()
