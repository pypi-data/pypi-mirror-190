"""version info and check."""
# pylint: disable=C0111
__version__ = '0.2.0a0'

def mindspore_version_check():
    """
    Do the MindSpore version check for MindSpore Graph Learning. If the
    MindSpore can not be imported, it will raise ImportError. If its
    version is not compatibale with current MindSpore Graph Learning verision,
    it will print a warning.

    Raises:
        ImportError: If the MindSpore can not be imported.
    """

    ms_gl_version_match = {'0.1': '1.6.1', '0.2.0a0': '1.10.1',
                           'master': '1.10.1'}
    try:
        import mindspore as ms
    except (ImportError, ModuleNotFoundError):
        print("Can not find MindSpore in current environment. Please install "
              "MindSpore before using MindSpore Graph Learning, by following "
              "the instruction at https://www.mindspore.cn/install")
        raise

    from mindspore import log as logger
    ms_version = ms.__version__
    logger.info("Current MindSpore version is {}".format(ms_version))
    required_verision = ms_gl_version_match[__version__]
    ms_version = ms_version.split('.')[:-1]
    ms_version = [int(i) for i in ms_version]
    required_mindspore_verision = required_verision.split('.')
    required_mindspore_verision = [int(i) for i in required_mindspore_verision]
    required_length = len(required_mindspore_verision)
    ms_length = len(ms_version)
    ms_version += [0] * (required_length - ms_length)
    check_res = True
    for i, e in enumerate(required_mindspore_verision):
        if ms_version[i] < e:
            check_res = False
            break
        elif ms_version[i] > e:
            check_res = True
            break
    if not check_res:
        logger.warning("Current version of MindSpore is not compatible with MindSpore Graph Learning. "
                       "Some functions might not work or even raise error. Please install MindSpore "
                       "version == {} For more details about dependency setting, please check "
                       "the instructions at MindSpore official website https://www.mindspore.cn/install "
                       "or check the README.md at https://gitee.com/mindspore/graphlearning"
                       .format(required_verision))
        warning_countdown = 3
        for i in range(warning_countdown, 0, -1):
            logger.warning(
                f"Please pay attention to the above warning, countdown: {i}")
